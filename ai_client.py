# ai_client.py

from openai import OpenAI
from core_directive import CORE_DIRECTIVE

# Uses OPENAI_API_KEY from your environment (do NOT hard-code it)
client = OpenAI()


def ask_happiness_core_ai(user_message: str) -> str:
    """
    Ask the AI that is governed by the inalienable right to pursue happiness.
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
    print("Happiness-Core AI. Ctrl+C to quit.\n")
    while True:
        try:
            msg = input("You: ")
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            break

        reply = ask_happiness_core_ai(msg)
        print("AI:", reply)
        print()
