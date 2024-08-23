import os
from typing import List
from groq import Groq
import requests
from bs4 import BeautifulSoup
from googleapiclient.discovery import build

relevent_selectors = {
    "theguardian.com" : [".article-body-commercial-selector"],
    "lemonde.fr" : ["article", "#post-container"],
    "nytimes.com": ["section[name=articleBody]"],
    "washingtonpost.com": ["article"],
    "lepoint.fr": ["article"],
}

PROMPT_SYSTEM = """
Generate the most relevant keywords for fact-checking the provided content. Focus on capturing key topics, claims, and entities that are essential for verifying the accuracy of the information.
Choose the appropriate language. For exemple, if the content concerns a country use the language of that country.
Instructions:
- few keywords
- Ensure that each keyword is distinct and directly related to fact-checking the content.
- No additional information or explanation is required.
Output format: keyword1, keyword2, …
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
    keywords = chat_completion.split(",")[:10]
    keywords = [keyword.strip() for keyword in keywords]
    search_key_words(keywords)
    print("keywords", keywords)
    return keywords


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
    
# TODO: Add error handling
# TODO: Work when JS is required
# TODO: Detect non-article pages
def get_website_content(url):
    response = requests.get(url, timeout=5)
    
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
    
service = build("customsearch", "v1",
        developerKey=os.environ.get("GOOGLE_API"))

class Article:
    title: str
    url: str
    def __init__(self, title, url):
        self.title = title
        self.url = url

def google_search(query: str, api_key: str, cse_id: str, num=10):
    #url = f"https://www.googleapis.com/customsearch/v1"
    #params = {
    #    'q': query,
    #    'key': api_key,
    #    'cx': cse_id,
    #    'num': num,
    #}
    #response = requests.get(url, params=params)
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
        print(e)
        return []
  
def search_key_words(key_words: List[str]):
    return google_search(" ".join(key_words), os.environ.get("GOOGLE_API"), "51c58602312b440ef")


def fact_check(statement: str):
    keywords = generate_key_words(statement)
    search_results = search_key_words(keywords)
    
    reviews = []
    i = 0
    for result in search_results:
        if i >= 5:
            break
        print(result.url)
        content = get_website_content(result.url)
        if len(content) > 100_000 or len(content) < 50:
            print("content too long or too short", len(content))
            continue
        review = read_article_and_give_review(statement, content).strip()
        
        review_state = False
        if review.startswith("True"):
            review_state = True
        review = review.removeprefix("True")
        review = review.removeprefix("False")
        reviews.append({
            "state": review_state,
            "url": result.url,
            "review": review.strip(),
        })
        i += 1
    return reviews
        
if __name__ == "__main__":    
    s = """
    Un sachet de couleur blanche est tombé du pantalon de Nancy Pelosi alors qu'elle entrait sur scène pour son discours à la convention du DNC.
    """
    print(fact_check(s))
