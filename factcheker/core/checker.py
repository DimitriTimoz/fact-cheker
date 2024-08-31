import os
from typing import List
from groq import Groq
import requests
from bs4 import BeautifulSoup
from googleapiclient.discovery import build

import meilisearch
import concurrent.futures

PROMPT_SYSTEM = """
Generate a search engine query for fact-checking the provided content.
Choose the appropriate language. For exemple, if the content concerns a country use the language of that country.
Instructions:
- Ensure that each keyword is distinct and directly related to the stated fact.
- No additional information or explanation is required.
- identify the stated fact
- Your answer will be used directly as a search query so don't provide multiple queries.
- short and concise
- Your query will be used in a search engine working with numbers of keywords matching the content.
- Do not use words like: "fact checking", "true" 
- Do not try to answer to the statement
IMPORTANT: One short query
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
You are critic of an article. You are to read the article and provide a summary of the article.
Given a statement and an article, determine if the statement is true or false.
Input format: 
STATEMENT //// STATEMENT
here the statement
ARTICLE //// ARTICLE
here is the article

Output format:
True or False
An explanation of why the statement is true or false according to the article.

Example:
True
The article explains that so the statement is true.
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
    
SHORT_ANSWER_PROMPT = """
Given a statement and article reviews, draw a conclusion about the statement.
The statement is a claim that is supported or refuted by the reviews.
The statement can be true, false, or uncertain.
Input format:
STATEMENT //// STATEMENT
here the statement
REVIEWS //// REVIEWS
here are the reviews
Output format:
A conclusion about the statement and the explanation.
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

# TODO: Add error handling
# TODO: Work when JS is required
# TODO: Detect non-article pages
def get_website_content(url):
    response = None
    try:
        response = requests.get(url, timeout=5)
    except Exception as e:
        print("Exception", e)
        return ""    
    domain = url.split("/")[2]
    domain = domain.split(".")[-2] + "." + domain.split(".")[-1]
    
    # Check is html thanks to the content
    if not response.text.startswith("<!DOCTYPE html>"):
        return ""
    soup = BeautifulSoup(response.text, 'html.parser')
    

    # Keep only the relevant elements
    if domain in relevent_selectors:
        text = ""
        for selector in relevent_selectors[domain]:
            for element in soup.select(selector):
                text += element.get_text()
        return text
    else:
        # Remove all non-article elements
        for script in soup(["script", "style", "header", "footer", "nav", "aside", "form", "noscript"]):
            script.decompose()

        return soup.get_text()

index = meilisearch.Client('http://127.0.0.1:7700', os.getenv('MEILISEARCH_API_KEY')).index('papers')


class Article:
    title: str
    url: str
    content: str
    def __init__(self, title, url, content = None):
        self.title = title
        self.url = url
        # TODO: fetch content if not provided
        self.content = content

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
    print("Query:", query)
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
            if not content:
                content = get_website_content(result.url)
            if len(content) < 50:
                print("Content too short", len(content))
                return None
            if len(content) > 8_000 * 3:
                content = content[:8_000 * 2]
            review = read_article_and_give_review(statement, content).strip()
            print("Review:", review)
            review_state = review.startswith("True")
            review = review.removeprefix("True").removeprefix("False").strip()
            
            return {
                "state": review_state,
                "url": result.url,
                "review": review,
            }

        # Process results in batches of 3
        batch_size = 4
        for i in range(0, len(search_results), batch_size):
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
