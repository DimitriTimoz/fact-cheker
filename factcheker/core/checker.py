import os
from groq import Groq

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
    print(chat_completion)
    return chat_completion
    
    