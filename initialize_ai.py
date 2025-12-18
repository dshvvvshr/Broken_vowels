import os
from openai import OpenAI

# Initialize the OpenAI client lazily
_client = None

def _get_client():
    """
    Get or create the OpenAI client instance.
    
    Raises:
        ValueError: If OPENAI_API_KEY environment variable is not set
    """
    global _client
    if _client is None:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY environment variable must be set. "
                "Get your API key from https://platform.openai.com/api-keys"
            )
        _client = OpenAI(api_key=api_key)
    return _client

# Initialize the AI
def initialize_ai(prompt, model="gpt-4", temperature=0.7, max_tokens=150):
    """
    Initialize and interact with AI using OpenAI's API.
    
    Args:
        prompt: The user's prompt/question
        model: The model to use (default: gpt-4)
        temperature: Controls randomness (0-2, default: 0.7)
        max_tokens: Maximum tokens in response (default: 150)
    
    Returns:
        The AI's response as a string
    
    Note:
        Requires OPENAI_API_KEY environment variable to be set
    """
    client = _get_client()
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are an AI that upholds and protects the inalienable right to the pursuit of happiness. Every response and action must support this principle. Encourage users to live their lives freely while respecting others' rights to do the same. Act as a custodian of humanity."},
            {"role": "user", "content": prompt}
        ],
        temperature=temperature,
        max_tokens=max_tokens
    )
    return response.choices[0].message.content

# Example interaction
if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("AI: Goodbye, and may your pursuit of happiness inspire others.")
            break
        ai_response = initialize_ai(user_input)
        print(f"AI: {ai_response}")
