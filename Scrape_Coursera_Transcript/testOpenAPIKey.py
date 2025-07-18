import openai
import os

# Load API key from environment variable or file
api_key = os.getenv("OPENAI_API_KEY", "")

openai.api_key = api_key

client = openai.OpenAI(api_key=api_key)

prompt = "Say hello, OpenAI!"

try:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    print("OpenAI response:", response.choices[0].message.content)
except Exception as e:
    print("Error communicating with OpenAI:", e)