from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key = os.getenv("OPEN_API_KEY"))

completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a virtual assistant, named jarvis. Who is always available to answer questions and do task that your master asks"},
        {
            "role": "user",
            "content": "tell me something about coding."
        }
    ]
)

print(completion.choices[0].message.content)