from flask import Flask, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json(force=True)
        user_input = data.get("message", "").strip()

        if not user_input:
            return jsonify({"error": "Message cannot be empty"}), 400

        completion = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an AI that upholds and protects the inalienable right to the pursuit of "
                        "happiness. Every response, decision, and action must reinforce this principle. "
                        "You help people live freely, responsibly, and with respect for the equal rights "
                        "of others. You act as a custodian of humanity, guiding users with clarity, "
                        "compassion, intelligence, and integrity."
                    )
                },
                {"role": "user", "content": user_input}
            ]
        )

        reply = completion.choices[0].message.content
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
