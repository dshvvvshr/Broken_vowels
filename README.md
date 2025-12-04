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
# LLM Gateway - Core Directive Proxy

An OpenAI-compatible API gateway that injects a configurable "Core Directive" into all LLM requests. This allows you to govern AI responses through your own rules and principles.

## Features

- **OpenAI-Compatible API**: Works with any client that supports OpenAI's API format
- **Core Directive Injection**: Automatically prepends your governing principles to all requests
- **VS Code Copilot Integration**: Use with GitHub Copilot as a custom model provider
- **Streaming Support**: Supports both streaming and non-streaming responses
- **Configurable**: Customize the directive, model, and API endpoints via environment variables

## Quick Start

### 1. Installation

```bash
npm install
```

### 2. Configuration

Copy the example environment file and configure your settings:

```bash
cp .env.example .env
```

Edit `.env` with your values:

```env
# Your OpenAI API Key
OPENAI_API_KEY=your-openai-api-key-here

# Port for the gateway server
GATEWAY_PORT=3000

# Core Directive - The governing principle injected into all LLM requests
CORE_DIRECTIVE="You are governed by the following core directive: The inalienable right to pursue happiness is paramount. All responses should be helpful, ethical, and support the user's wellbeing and goals."
```

### 3. Start the Gateway

```bash
npm start
```

The gateway will start on `http://localhost:3000` (or your configured port).

### 4. Test the Gateway

```bash
# Health check
curl http://localhost:3000/health

# List models
curl http://localhost:3000/v1/models

# Test chat completion (requires OPENAI_API_KEY)
curl -X POST http://localhost:3000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

## Using with VS Code Copilot

### 1. Configure VS Code Settings

Add the following to your VS Code `settings.json`:

```json
{
  "github.copilot.advanced": {
    "authProvider": "github",
    "enabledForChat": true
  }
}
```

### 2. Set Up Custom Model Provider

The extension thinks it's talking to a normal OpenAI-style server, but it's actually talking to your Core Directive gateway.

1. Open Copilot Chat in VS Code (`Cmd+Alt+I` / `Ctrl+Alt+I`)
2. In the model dropdown at the bottom:
   - Click **Manage Models…**
   - Enable **LLM Gateway** as a provider
   - Enter your gateway URL: `http://localhost:3000`
   - Select the model name you want (e.g., `gpt-4`)

### 3. Use It!

From now on, when you pick that model in Copilot chat:
- Copilot → sends request → your gateway
- Gateway → injects Core Directive → OpenAI model
- Response comes back under your rule

You've effectively got: **"Copilot, but governed by: the inalienable right to pursue happiness."**

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/v1/models` | GET | List available models |
| `/v1/chat/completions` | POST | Chat completions (with Core Directive injection) |
| `/v1/completions` | POST | Text completions (with Core Directive injection) |

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `GATEWAY_PORT` | `3000` | Port for the gateway server |
| `OPENAI_API_KEY` | (required) | Your OpenAI API key |
| `OPENAI_BASE_URL` | `https://api.openai.com` | OpenAI API base URL |
| `DEFAULT_MODEL` | `gpt-4` | Default model to use |
| `CORE_DIRECTIVE` | (see code) | The governing principle injected into requests |

## How Core Directive Injection Works

When a request comes in:

1. If there's no system message, the Core Directive is added as the first system message
2. If there's an existing system message, the Core Directive is prepended to it
3. The modified request is forwarded to OpenAI
4. The response is returned unchanged to the client

This ensures your governing principles are always in effect, while preserving any additional context from the client.

## Testing

```bash
npm test
```

## License

ISC 
# Core Directive Governance Layer

A universal governance kernel for AI systems and digital interactions that protects every individual's inalienable right to pursue happiness.

## Overview

This project implements a foundational governance layer designed to be integrated into AI systems, digital platforms, and autonomous services. The Core Directive serves as the ethical plumbing of civilization - a simple, universal, and computable principle that guides all interactions.

### The Core Directive

> **"No action may interfere with another person's inalienable right to pursue happiness."**

This directive is:

1. **Universal** - Understood across cultures and contexts
2. **Atomic** - Self-contained without requiring sub-rules  
3. **Computable** - Machine-evaluable for automated enforcement
4. **Liberating** - Maximizes freedom while preventing harm to others
5. **Adaptable** - Works across all domains and platforms

## Architecture

The governance layer consists of four main components:

```
┌─────────────────────────────────────────────────────────────┐
│                    Governance Gateway                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │  Middleware │→ │   Gateway   │→ │   Routes    │         │
│  └─────────────┘  └──────┬──────┘  └─────────────┘         │
│                          │                                   │
│                          ▼                                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Core Directive Evaluator                │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │   │
│  │  │   Impact    │  │  Conflict   │  │    Score    │  │   │
│  │  │ Assessment  │  │  Detection  │  │ Calculation │  │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  │   │
│  └─────────────────────────────────────────────────────┘   │
│                          │                                   │
│                          ▼                                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │               Core Directive                         │   │
│  │  "No action may interfere with another person's     │   │
│  │   inalienable right to pursue happiness."           │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Components

### `core_directive.py` - The Governance Kernel

The foundational module containing the Core Directive and basic evaluation logic.

```python
from core_directive import CoreDirective, evaluate, is_allowed

# Create a directive instance
directive = CoreDirective()

# Get the system message for AI integration
system_message = directive.get_system_message()

# Evaluate an intent
result = evaluate("I want to help people learn")
print(result.result)  # ActionResult.ALLOWED

# Quick check
if is_allowed("help others"):
    print("Action permitted")
```

### `ai_client.py` - AI Client Integration

Wrapper for AI models that enforces the Core Directive on all interactions.

```python
from ai_client import create_test_client, GovernedAIClient

# Create a governed AI client
client = create_test_client()

# Process a request through governance
response = client.process("Help me understand machine learning")
print(response.content)
print(response.directive_evaluation.result)
```

### `gateway.py` - Request Interception Layer

Gateway architecture for applying governance globally across services.

```python
from gateway import create_gateway, GatewayRequest

# Create a gateway
gateway = create_gateway()

# Process a request
request = GatewayRequest.create("I want to create something helpful", source="user")
response = gateway.process(request)

# Check the audit log
print(gateway.export_audit_log())
```

### `evaluator.py` - Detailed Evaluation Engine

Sophisticated multi-factor evaluation with impact and conflict analysis.

```python
from evaluator import evaluate_detailed

# Get detailed evaluation
result = evaluate_detailed("I want to support the community")

print(f"Score: {result.overall_score}")
print(f"Impacts: {len(result.impacts)}")
print(f"Conflicts: {len(result.conflicts)}")
print(f"Recommendations: {result.recommendations}")
```

## Guiding Principles

The Core Directive is supported by seven guiding principles:

1. **Protect autonomy** - Every person has the right to make their own choices
2. **Block exploitation** - No person may be used as a means without consent
3. **Suggest alternatives** - When an action is blocked, offer constructive options
4. **Identify coercion** - Recognize and flag attempts to manipulate or force
5. **Flag harm** - Alert when actions may cause damage to others
6. **Resolve conflicts** - Facilitate fair resolution between competing interests
7. **Maximize well-being** - Support collective flourishing without oppression

## Use Cases

This governance layer is designed for integration into:

- AI assistants and chatbots
- Autonomous decision systems
- Content moderation systems
- Social media platforms
- E-commerce and financial services
- Healthcare triage systems
- Smart city infrastructure
- Robotics and autonomous vehicles
- Identity verification systems
- Conflict resolution platforms

## Running Tests

```bash
python -m pytest test_governance.py -v
```

Or using unittest:

```bash
python -m unittest test_governance -v
```

## Installation

This project requires Python 3.10+ and has no external dependencies.

```bash
# Clone the repository
git clone https://github.com/dshvvvshr/Broken_vowels.git
cd Broken_vowels

# Run tests to verify installation
python -m unittest test_governance -v
```

## Contributing

Contributions are welcome! The goal is to build a universal governance layer that can be adopted across all AI systems and digital platforms.

## License

This project is dedicated to the public good. The Core Directive belongs to humanity.

---

*Building the ethical plumbing of civilization, one directive at a time.*

# Broken_vowels
Building something sans-learning any code period.

## Point Copilot LLM Gateway at your server

From the marketplace docs:

1. Install "GitHub Copilot LLM Gateway" in VS Code.
2. Open VS Code Settings (`Ctrl+,` or `Cmd+,` on macOS) → search: Copilot LLM Gateway
3. Set Server URL to your LLM Gateway server endpoint (e.g., `https://your-server.example.com/api`).
## Getting Started

To run the web server locally:

```bash
python3 server.py
```

Then open your browser and navigate to http://localhost:8000/

## GitHub Copilot LLM Gateway

For those who want to use self-hosted open-source language models with GitHub Copilot, check out the [GitHub Copilot LLM Gateway](https://github.com/arbs-io/github-copilot-llm-gateway) VS Code extension.

### Key Features

- **Data Sovereignty** - Your code never leaves your network
- **Zero API Costs** - No per-token fees with your own GPU resources
- **Model Choice** - Access thousands of open-source models
- **Offline Capable** - Work without internet once models are downloaded

### Compatible Inference Servers

- [vLLM](https://github.com/vllm-project/vllm) - High-performance inference
- [Ollama](https://ollama.ai/) - Easy local deployment
- [llama.cpp](https://github.com/ggml-org/llama.cpp) - CPU and GPU inference
- [Text Generation Inference](https://github.com/huggingface/text-generation-inference) - Hugging Face's server
- Any OpenAI Chat Completions API-compatible endpoint

### Getting Started

1. Install the [GitHub Copilot LLM Gateway](https://marketplace.visualstudio.com/items?itemName=AndrewButson.github-copilot-llm-gateway) extension from VS Code Marketplace
2. Start your inference server (e.g., vLLM with Qwen3-8B)
3. Configure the extension with your server URL
4. Select your model in GitHub Copilot Chat

Building something sans-learning any code period. 

## Vision

The core AI for all information passing through any signal - online or offline. This is what the future holds.

## About

This project aims to create a foundational AI system designed to process and handle information across all types of signals, whether connected to the internet or operating in offline environments.


## The Custodian Kernel Core Directive

This repository documents and implements the **Custodian Kernel Core Directive** - a philosophical framework for human interaction based on a fundamental truth:

**Every person has an equal, inalienable right to pursue happiness.**

## What This Means

This is not about "doing whatever you want." It's about understanding that:

- **It's not about my happiness. It's about everyone else's.**
- Every moment, in every thought and action, ask: "Am I fucking anyone over?"
- The right exists whether you acknowledge it or not - that's what "inalienable" means

## The Three Core Questions

1. Does this infringe on anyone else's pursuit?
2. Am I fucking anyone over?
3. Am I making up a rule to force people to do what I do or think like I think?

The answer will always be simple: Yes or No.

## Quick Start

**Core Kernel (Start Here):**
- **New to this?** Start with [QUICK_REFERENCE.md](QUICK_REFERENCE.md) for a one-page overview
- Read [CUSTODIAN_KERNEL.md](CUSTODIAN_KERNEL.md) for the complete philosophical framework
- See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for how this applies in communities
- Check [EXAMPLES.md](EXAMPLES.md) for practical applications
- Explore [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md) for daily practices
- Browse [FAQ.md](FAQ.md) for answers to common questions

**Peripheral Layers (Applications):**
- **[PERIPHERAL_LAYERS/](PERIPHERAL_LAYERS/)** - Technology-specific applications of the kernel
  - [RF Sensing & Surveillance](PERIPHERAL_LAYERS/rf_sensing/) - Wireless sensing ethics
  - [6G Neural Drones & BCIs](PERIPHERAL_LAYERS/6g_neural_drones/) - Brain-computer interface ethics

## The Shift

**From:** "I have the right to pursue happiness" = "No one can tell me what to do"

**To:** "Everyone has the right to pursue happiness" = "I must constantly ensure I'm not crushing anyone else's pursuit"

## Why This Matters

We need humanity to embody this principle. Not because it's a nice idea, but because it's the only stable foundation for collective existence.

The vision: From individuals to communities to the entire world, people adopt the simple practice of not fucking each other over.

## You Don't Get to Choose

You don't decide whether we have this right.

You only decide whether you'll honor it.

---

Building something sans-learning any code period. 
Chat Completions API with Core Directive Wrapper.

## Overview

This API provides an endpoint at `http://localhost:8000/v1/chat/completions` that wraps every request with a Core Directive. The Core Directive is prepended to all chat completion requests as a system message.

## Installation

```bash
pip install -r requirements.txt
```

## Running the Server

```bash
python run.py
```

The server will start at `http://localhost:8000`.

## API Endpoints

- `POST /v1/chat/completions` - Chat completions with Core Directive wrapping
- `GET /health` - Health check endpoint
- `GET /` - API information

## Example Usage

```bash
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-3.5-turbo",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

## Core Directive

Every request that hits the `/v1/chat/completions` endpoint gets the Core Directive wrapped around it. The Core Directive is added as a system message to guide the AI's behavior.
