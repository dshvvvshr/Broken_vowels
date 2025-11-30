"""FastAPI application for chat completions with Core Directive wrapper."""

import time
import uuid
from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.models import (
    ChatCompletionRequest,
    ChatCompletionResponse,
    Choice,
    Message,
    Usage,
)
from app.core_directive import CORE_DIRECTIVE

app = FastAPI(
    title="Chat Completions API",
    description="API endpoint that wraps all requests with a Core Directive",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def wrap_with_core_directive(messages: List[Message]) -> List[Message]:
    """Wrap the messages with the Core Directive as a system message.
    
    If a system message already exists, prepend the Core Directive to it.
    Otherwise, add a new system message at the beginning.
    """
    wrapped_messages = []
    has_system_message = False
    
    for msg in messages:
        if msg.role == "system":
            # Prepend Core Directive to existing system message
            wrapped_content = f"{CORE_DIRECTIVE}\n\n{msg.content}"
            wrapped_messages.append(Message(role="system", content=wrapped_content))
            has_system_message = True
        else:
            wrapped_messages.append(msg)
    
    # If no system message exists, add one at the beginning
    if not has_system_message:
        wrapped_messages.insert(0, Message(role="system", content=CORE_DIRECTIVE))
    
    return wrapped_messages


@app.post("/v1/chat/completions", response_model=ChatCompletionResponse)
async def chat_completions(request: ChatCompletionRequest) -> ChatCompletionResponse:
    """Handle chat completions requests with Core Directive wrapping.
    
    Every request that hits this endpoint gets the Core Directive
    wrapped around it as a system message.
    """
    # Wrap messages with Core Directive
    wrapped_messages = wrap_with_core_directive(request.messages)
    
    # For this implementation, we return a mock response
    # In a real scenario, you would forward to an actual LLM API
    response_content = f"Processed {len(wrapped_messages)} messages with Core Directive applied."
    
    return ChatCompletionResponse(
        id=f"chatcmpl-{uuid.uuid4().hex[:12]}",
        object="chat.completion",
        created=int(time.time()),
        model=request.model,
        choices=[
            Choice(
                index=0,
                message=Message(role="assistant", content=response_content),
                finish_reason="stop",
            )
        ],
        usage=Usage(
            prompt_tokens=len(str(wrapped_messages)),
            completion_tokens=len(response_content),
            total_tokens=len(str(wrapped_messages)) + len(response_content),
        ),
    )


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "Chat Completions API",
        "version": "1.0.0",
        "description": "All requests to /v1/chat/completions get the Core Directive wrapped around them",
        "endpoints": {
            "/v1/chat/completions": "POST - Chat completions with Core Directive",
            "/health": "GET - Health check",
        },
    }
