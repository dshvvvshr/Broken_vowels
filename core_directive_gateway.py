# file: core_directive_gateway.py

import time
import uuid
from typing import List, Optional

from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI

client = OpenAI()  # uses OPENAI_API_KEY from your env

CORE_DIRECTIVE = """
You are an AI assistant governed by this Core Directive:

Every person has an equal, inalienable right to pursue happiness.
You must not intentionally support actions that interfere with another person's
ability to pursue that right (through coercion, exploitation, violence, or deception).
Participation must always be voluntary. When interests conflict, seek options that
respect everyone's rights as much as possible.

"Not fucking people over" is a consequence of this directive: if something clearly
tramples someone's ability to pursue happiness, you refuse to help with that part
and, if you can, suggest a better path that doesn't.
"""

# --- OpenAI-compatible request/response models ---


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    model: str
    messages: List[Message]
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None


class Choice(BaseModel):
    index: int
    message: Message
    finish_reason: str


class ChatResponse(BaseModel):
    id: str
    object: str
    created: int
    model: str
    choices: List[Choice]


app = FastAPI()


@app.post("/v1/chat/completions", response_model=ChatResponse)
async def chat_completions(req: ChatRequest):
    # Inject Core Directive as the first system message
    messages = [{"role": "system", "content": CORE_DIRECTIVE}]
    messages.extend(m.model_dump() for m in req.messages)

    completion = client.chat.completions.create(
        model=req.model or "gpt-4.1",
        messages=messages,
        max_tokens=req.max_tokens,
        temperature=req.temperature,
    )

    choice = completion.choices[0]
    return ChatResponse(
        id=f"chatcmpl-{uuid.uuid4().hex}",
        object="chat.completion",
        created=int(time.time()),
        model=req.model or "gpt-4.1",
        choices=[
            Choice(
                index=0,
                message=Message(
                    role=choice.message.role,
                    content=choice.message.content,
                ),
                finish_reason=choice.finish_reason or "stop",
            )
        ],
    )
