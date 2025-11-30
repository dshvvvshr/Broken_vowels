"""
Chat Completions API Server

This server provides an OpenAI-compatible /v1/chat/completions endpoint
that wraps all incoming requests with a Core Directive.
"""

import time
import uuid

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import uvicorn

app = FastAPI(title="Chat Completions API", version="1.0.0")

# Core Directive that wraps all incoming chat completions requests
CORE_DIRECTIVE = """You are a helpful AI assistant. Follow these guidelines:
1. Be helpful, harmless, and honest.
2. Provide accurate and relevant information.
3. Respect user privacy and maintain confidentiality.
"""


class Message(BaseModel):
    role: str
    content: str


class ChatCompletionRequest(BaseModel):
    model: str
    messages: list[Message]
    temperature: Optional[float] = 1.0
    max_tokens: Optional[int] = None
    stream: Optional[bool] = False


class ChatCompletionChoice(BaseModel):
    index: int
    message: Message
    finish_reason: str


class Usage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class ChatCompletionResponse(BaseModel):
    id: str
    object: str
    created: int
    model: str
    choices: list[ChatCompletionChoice]
    usage: Usage


def wrap_with_core_directive(messages: list[Message]) -> list[Message]:
    """
    Wraps the incoming messages with the Core Directive.
    Adds a system message at the beginning with the Core Directive.
    """
    core_directive_message = Message(role="system", content=CORE_DIRECTIVE)
    
    # Check if there's already a system message
    wrapped_messages = [core_directive_message]
    
    for msg in messages:
        if msg.role == "system":
            # Combine existing system message with core directive
            combined_content = f"{CORE_DIRECTIVE}\n\n{msg.content}"
            wrapped_messages[0] = Message(role="system", content=combined_content)
        else:
            wrapped_messages.append(msg)
    
    return wrapped_messages


@app.post("/v1/chat/completions")
async def chat_completions(request: ChatCompletionRequest):
    """
    Handle chat completions requests.
    Wraps incoming requests with the Core Directive before processing.
    """
    # Wrap messages with Core Directive
    wrapped_messages = wrap_with_core_directive(request.messages)
    
    # For demo purposes, echo back the wrapped messages
    # In a real implementation, this would forward to an actual LLM
    response_content = f"Received request with {len(wrapped_messages)} messages (including Core Directive wrapper)."
    
    # Approximate token count (rough estimate: 4 characters per token)
    prompt_chars = sum(len(msg.content) for msg in wrapped_messages)
    prompt_tokens = max(1, prompt_chars // 4)
    completion_tokens = max(1, len(response_content) // 4)
    
    response = ChatCompletionResponse(
        id=f"chatcmpl-{uuid.uuid4().hex[:12]}",
        object="chat.completion",
        created=int(time.time()),
        model=request.model,
        choices=[
            ChatCompletionChoice(
                index=0,
                message=Message(role="assistant", content=response_content),
                finish_reason="stop"
            )
        ],
        usage=Usage(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=prompt_tokens + completion_tokens
        )
    )
    
    return response


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "ok", "message": "Chat Completions API is running"}


@app.get("/v1/models")
async def list_models():
    """List available models."""
    return {
        "object": "list",
        "data": [
            {
                "id": "gpt-3.5-turbo",
                "object": "model",
                "created": 1677610602,
                "owned_by": "openai"
            }
        ]
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
