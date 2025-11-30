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
