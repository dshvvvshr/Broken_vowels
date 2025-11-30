# ai_client.py

from openai import OpenAI
from core_directive import CORE_DIRECTIVE

client = OpenAI()  # uses OPENAI_API_KEY from your environment


def ask_ai(user_message: str) -> str:
    """
    Send a message to the AI governed by the core directive:
    Every person has an equal, inalienable right to pursue happiness.
    """
    completion = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": CORE_DIRECTIVE},
            {"role": "user", "content": user_message},
        ],
    )
    return completion.choices[0].message.content


if __name__ == "__main__":
    print("Happiness Directive AI. Ctrl+C to quit.\n")
    while True:
        try:
            msg = input("You: ")
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            break

        reply = ask_ai(msg)
        print("AI:", reply)
        print()
