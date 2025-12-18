import openai

# Initialize the AI
def initialize_ai(prompt, model="gpt-4", temperature=0.7, max_tokens=150):
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are an AI that upholds and protects the inalienable right to the pursuit of happiness. Every response and action must support this principle. Encourage users to live their lives freely while respecting others' rights to do the same. Act as a custodian of humanity."},
            {"role": "user", "content": prompt}
        ],
        temperature=temperature,
        max_tokens=max_tokens
    )
    return response.choices[0].message['content']

# Example interaction
if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("AI: Goodbye, and may your pursuit of happiness inspire others.")
            break
        ai_response = initialize_ai(user_input)
        print(f"AI: {ai_response}")
