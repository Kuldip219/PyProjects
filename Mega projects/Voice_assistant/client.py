from openai import OpenAI

client = OpenAI(
    api_key="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"
)

completion = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {"role": "system", "content": "You are a virtual assistant named Gipsy skilled in general tasks like Alexa and Google Cloud."},
        {"role": "user", "content": "What is coding?"},
    ]
)

print(completion.choices[0].message.content)