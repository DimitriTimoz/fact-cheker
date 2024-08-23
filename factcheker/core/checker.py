import os
from groq import Groq
import requests
from bs4 import BeautifulSoup

relevent_selectors = {
    "theguardian.com" : [".article-body-commercial-selector"],
    "lemonde.fr" : ["article", "#post-container"],
    "nytimes.com": ["section[name=articleBody]"],
    "washingtonpost.com": ["article"],
}

PROMPT_SYSTEM = """
Generate key words to find against the given content.
Maximum number of key words: 10
No extra information is needed.
Format: key1, key2, key3, ...
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
        model="mixtral-8x7b",
    )
    
    chat_completion = chat_completion.choices[0].message.content
    return chat_completion
    
# TODO: Add error handling
# TODO: Work when JS is required
# TODO: Detect non-article pages
def get_website_content(url):
    response = requests.get(url)
    
    domain = url.split("/")[2]
    domain = domain.split(".")[-2] + "." + domain.split(".")[-1]
    
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
    
def google_search(query, api_key, cse_id, num=10):
    url = f"https://www.googleapis.com/customsearch/v1"
    params = {
        'q': query,
        'key': api_key,
        'cx': cse_id,
        'num': num,
    }
    response = requests.get(url, params=params)
    return response.json()
  
def search_key_words(key_words):
    
    print(google_search(" ".join(key_words), os.environ.get("GOOGLE_API"), "51c58602312b440ef"))


s = """
l'incursion de l'Ukraine dans Koursk en Russie est l'opération la plus injustifiée, en termes de coût, de l'histoire du 21ème siècle.
"""

a = """

"""
print(get_website_content("https://www.washingtonpost.com/politics/2024/08/23/kamala-harris-gaza-stance-palestinians-dnc/"))
