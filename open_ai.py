from openai import OpenAI
client = OpenAI(api_key = "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")

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