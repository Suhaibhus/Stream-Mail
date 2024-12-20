import os
import emailreader
from groq import Groq


client = Groq(api_key="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")

user = emailreader.msg.text
chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "you are a helpful assistant."
        },
        {
            "role": "user",
            "content": f"Summarize this text into one word: {user}",
        }
    ],
    model="llama3-8b-8192",
)

print(chat_completion.choices[0].message.content)