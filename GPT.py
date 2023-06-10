import openai
import os

with open('data/GPTapi.txt', 'r') as f:
    openai.api_key = f.read().strip()
    
def generate_response(prompt):
    completions = openai.Completion.create(
        engine="gpt-3.5-turbo",
        prompt=prompt,
        max_tokens=2048,
        n=1,
        temperature=0.7,
    )
    message = completions.choices[0].text.strip()
    return message
    
while True:
    user_input = input("You: ")
    if user_input.lower() in ["bye", "goodbye", "exit"]:
        print("Bot: Goodbye!")
        break
    prompt = f"User: {user_input}\nAI:"
    response = generate_response(prompt)
    print(f"Bot: {response}")