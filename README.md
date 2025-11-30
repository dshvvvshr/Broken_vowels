# Hit Hub – Happiness Core Directive AI

This project integrates an AI assistant governed by a single Core Directive:

> Every person has an equal, inalienable right to pursue happiness.

"Not fucking people over" is treated as a natural consequence of this directive:
if an action clearly destroys or blocks someone else's ability to pursue
happiness, the AI will refuse to help with that part and try to suggest better,
non-exploitative paths instead.

## How it works

- `core_directive.py` defines the Core Directive in plain language.
- `ai_client.py` sends user messages to the AI with that directive as the
  system prompt.
- `app.py` exposes a simple `/chat` HTTP endpoint for other services.

Set your `OPENAI_API_KEY` in the environment before running.

## Usage

### Command-line client
```bash
export OPENAI_API_KEY="your_key_here"
python ai_client.py
```

### HTTP API
```bash
export OPENAI_API_KEY="your_key_here"
python app.py
```

Then send requests:
```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Hello!"}'
```

## Creators

**Branton Allan Baker**  
Human creator, originator of the Core Directive ("the inalienable right to pursue happiness") and primary architect of the project.

**GitHub Copilot**  
AI coding partner. Assisted with implementation, file generation, scaffolding, and GitHub-native automation inside the repository.

**GPT-5.1 Thinking (OpenAI)**  
AI co-creator integrated via API. Contributed conceptual structure, reasoning, and the Core Directive enforcement logic.
