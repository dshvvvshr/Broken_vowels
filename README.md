# Happiness Directive AI

An AI application built on the core directive of upholding the inalienable right to the pursuit of happiness.

## Core Directive

This AI operates under the principle that:
- Everyone has the right to pursue happiness
- No one is forced to participate
- Everyone has a choice
- No one infringes upon another's pursuit intentionally
- Unintentional conflicts are resolved cooperatively

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set your OpenAI API key:
```bash
export OPENAI_API_KEY="your_api_key_here"
```

3. Run the application:
```bash
python app.py
```

Output:
```
 * Serving Flask app 'app'
 * Running on http://127.0.0.1:5000 (Press CTRL+C to quit)
```

## Usage

Send a POST request to the `/ask` endpoint:

```bash
curl -X POST http://localhost:5000/ask \
  -H "Content-Type: application/json" \
  -d '{"message":"Hello!"}'
```

Response:
```json
{"reply": "Hello!"}
```
