"""Pydantic models for chat completions API."""

from typing import List, Optional, Union
from pydantic import BaseModel


class Message(BaseModel):
    """A message in the chat conversation."""
    role: str
    content: str


class ChatCompletionRequest(BaseModel):
    """Request model for chat completions endpoint."""
    model: str
    messages: List[Message]
    temperature: Optional[float] = 1.0
    max_tokens: Optional[int] = None
    stream: Optional[bool] = False


class Choice(BaseModel):
    """A completion choice."""
    index: int
    message: Message
    finish_reason: str


class Usage(BaseModel):
    """Token usage information."""
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class ChatCompletionResponse(BaseModel):
    """Response model for chat completions endpoint."""
    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: List[Choice]
    usage: Usage
