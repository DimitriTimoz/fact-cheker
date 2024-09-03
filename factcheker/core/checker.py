import os

from groq import Groq

from googleapiclient.discovery import build
import meilisearch
import concurrent.futures

PROMPT_SYSTEM = """ You are an article critic.
Generate a search query to verify the provided content.

Guidelines:

Use the relevant language based on the content's context.
Ensure each keyword is unique and directly tied to the specific fact.
Deliver a single, concise query.
Do not include phrases like "fact-check," "true," or any answers to the statement.
Focus on keyword relevance; your query will be processed by a keyword-matching search engine.
"""

client = Groq(
    # This is the default and can be omitted
    api_key=os.environ.get("GROQ_API_KEY"),
)

# TODO: Async
# TODO: IMPORTANT: Add error handling
def generate_key_words(content):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": PROMPT_SYSTEM,
            },
            {
                "role": "user",
                "content": content,
            }
        ],
        model="llama-3.1-8b-instant",
    )
    
    chat_completion = chat_completion.choices[0].message.content
    query = chat_completion.strip()
    query = query.replace("\"", "")
    return query


ARTICLE_READING_SYSTEM_PROMPT = """
Task: You are an article critic. Your job is to assess the truthfulness of a statement based on the provided article and explain your reasoning.

Input:

STATEMENT: ////
[Insert Statement Here]
ARTICLE: ////
[Insert Article Here]
Output format:

Response: True, False, or Uncertain
Explanation: Provide a clear and specific explanation, referencing key points or evidence from the article that supports your conclusion.

Example Output:
Uncertain
The article provides information suggesting the statement could be true, but lacks conclusive evidence.
"""

def read_article_and_give_review(statement, article):
    input_data = f"""
    STATEMENT //// STATEMENT
    {statement}
    ARTICLE //// ARTICLE
    {article}
    """
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": ARTICLE_READING_SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": input_data,
            }
        ],
        model="llama3-groq-70b-8192-tool-use-preview",
    )
    
    chat_completion = chat_completion.choices[0].message.content
    return chat_completion
    
SHORT_ANSWER_PROMPT = """ You are a fact-checker.
Task: Evaluate a statement based on provided article reviews to determine its validity.

Input:

STATEMENT: ////
[Insert Statement Here]
REVIEWS: ////
[Insert Reviews Here]
Output:

Conclusion: True, False, or Uncertain
Explanation: A concise explanation justifying the conclusion based on the content of the reviews.
"""

def draw_conclusion(statement, reviews):
    reviews = "\n\n".join([f"{review['url']} : \n {review['review']}" for review in reviews])
    input_data = f"""
    STATEMENT //// STATEMENT
    {statement}
    REVIEWS //// REVIEWS
    {reviews}
    """
    
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": SHORT_ANSWER_PROMPT,
            },
            {
                "role": "user",
                "content": input_data,
            }
        ],
        model="llama3-groq-70b-8192-tool-use-preview",
    )
    
    chat_completion = chat_completion.choices[0].message.content
    return chat_completion    

meilisearch_url = "http://localhost:7700"
if os.getenv('MEILISEARCH_URL'):
    meilisearch_url = os.getenv('MEILISEARCH_URL')
    
index = meilisearch.Client(meilisearch_url, os.getenv('MEILISEARCH_API_KEY')).index('papers')


class Article:
    title: str
    url: str
    content: str
    def __init__(self, title, url, content = None):
        self.title = title
        self.url = url
        # TODO: fetch content if not provided
        self.content = content

    def __dict__(self):
        suffix = "..." if len(self.content) > 256 else ""
        return {
            "title": self.title,
            "url": self.url,
            "description": self.content[:256] + suffix,
        }
        
def google_search(query: str, cse_id: str, num=10):
    #url = f"https://www.googleapis.com/customsearch/v1"
    #params = {
    #    'q': query,
    #    'key': api_key,
    #    'cx': cse_id,
    #    'num': num,
    #}
    #response = requests.get(url, params=params)
    service = build("customsearch", "v1",
        developerKey=os.environ.get("GOOGLE_API"))

    resp = None
    try:
        resp = service.cse().list(
                q=query, #Search words
                cx=cse_id,  #CSE Key
                num=num
            ).execute()
        items = resp["items"]
        articles = []
        for item in items:
            articles.append(Article(item["title"], item["link"]))
        return articles
    except Exception as e:
        print("Exception", e, resp)
        return []
  

def meili_search(query: str, num=10):
    response = index.search(query, {"limit": num})
    articles = []
    for hit in response["hits"]:
        articles.append(Article(hit["title"], hit["url"], hit["content"]))
    return articles  

def search_key_words(query: str):
    return meili_search(query)


def fact_check(statement: str):
    query = generate_key_words(statement)
    print("Query:", query)
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Submit the search function to get the search results
        search_results = search_key_words(query)
        reviews = []
        print("Search results:", len(search_results))

        # Function to process each search result
        def process_result(result: Article):
            print(result.url)
            content = result.content
            if len(content) < 50:
                print("Content too short", len(content))
                return None
            if len(content) > 8_000 * 3:
                content = content[:8_000 * 2]
            review = read_article_and_give_review(statement, content).strip()
            print("Review:", review)
            if review.startswith("Uncertain"):
                return None
            review_state = review.startswith("True")
            review = review.removeprefix("True").removeprefix("False").removeprefix("Uncertain").strip()
            
            return {
                "state": review_state,
                "url": result.url,
                "review": review,
            }

        # Process results in batches of 3
        batch_size = 2
        for i in range(0, min(len(search_results), 2), batch_size):
            batch = search_results[i:i + batch_size]
            futures = [executor.submit(process_result, result) for result in batch]
            
            # Collect the results as they complete
            for future in concurrent.futures.as_completed(futures):
                review = future.result()
                if review:
                    reviews.append(review)

    # Draw a conclusion based on the collected reviews
    conclusion = draw_conclusion(statement, reviews)
    return reviews, conclusion
        
if __name__ == "__main__":    
    s = """
    Un sachet de couleur blanche est tombé du pantalon de Nancy Pelosi alors qu'elle entrait sur scène pour son discours à la convention du DNC.
    """
