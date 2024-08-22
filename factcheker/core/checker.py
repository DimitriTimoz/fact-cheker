import os
from groq import Groq
import requests

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


    