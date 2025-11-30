# Broken_vowels
Building something sans-learning any code period.

## Chat Completions API Server

This project provides an OpenAI-compatible chat completions API server that wraps all incoming requests with a Core Directive.

### Features

- OpenAI-compatible `/v1/chat/completions` endpoint
- All requests are automatically wrapped with a Core Directive
- Health check endpoint at `/`
- Model listing endpoint at `/v1/models`

### Installation

```bash
pip install -r requirements.txt
```

### Running the Server

```bash
python server.py
```

The server will start on `http://localhost:8000`.

### API Usage

#### Chat Completions

```bash
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-3.5-turbo",
    "messages": [
      {"role": "user", "content": "Hello, how are you?"}
    ]
  }'
```

Every request to this endpoint automatically has the Core Directive wrapped around it, ensuring consistent behavior across all chat completions. 
