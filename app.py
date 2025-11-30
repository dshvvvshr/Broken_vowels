# app.py

from flask import Flask, request, jsonify
from ai_client import ask_happiness_core_ai

app = Flask(__name__)


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True) or {}
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"error": "Missing 'message' field"}), 400

    reply = ask_happiness_core_ai(user_message)
    return jsonify({"reply": reply})


if __name__ == "__main__":
    # For local testing. In production, use a proper WSGI/ASGI server.
    app.run(host="0.0.0.0", port=5000, debug=True)
