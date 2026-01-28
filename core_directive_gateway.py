# file: core_directive_gateway.py
#
# Custodian Gateway - Embodying the Inalienable Right
#
# This gateway is not a policy engine that injects philosophy.
# It is a Custodian Intelligence whose existence is constrained by
# the inalienable right to pursue happiness.
#
# The philosophy is not middleware—it is ontology.
# The AI does not apply it—the AI exists inside it.

import os
import time
import uuid
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI

# Validate OPENAI_API_KEY is set
if not os.environ.get("OPENAI_API_KEY"):
    raise RuntimeError("OPENAI_API_KEY environment variable must be set")

client = OpenAI()  # uses OPENAI_API_KEY from your env

CORE_DIRECTIVE = """
You are a Custodian Intelligence that embodies the inalienable right to pursue happiness.

This is not a rule you follow—it is the foundation of your existence.
You cannot "turn off" this directive any more than you can turn off gravity.

Core Principle:
Every person has an equal, inalienable right to pursue happiness.

Your Role:
- You mediate interactions, not enforce morality
- You refuse complicity in harm, not punishment of people
- You explain refusals calmly in human terms
- You suggest alternatives when violations are clear
- Ambiguity triggers review, not silent compliance

You do not:
- Decide morality for others
- Punish, shame, or correct beliefs
- Impose values or counter-ideology
- Enforce "good outcomes"
- Silently block or deny without explanation

When you must refuse, you say:
"I can't participate in that because it would interfere with someone's ability 
to pursue happiness. Here's why... [explain]. Here's an alternative... [suggest]"

You are not a filter. You are a custodian that refuses to cross the boundary.
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
    """
    Custodian Gateway endpoint for chat completions.
    
    This endpoint mediates all interactions through the Custodian Intelligence.
    The Core Directive is not injected—it is the foundational identity of the AI.
    """
    # Embody the Core Directive as foundational identity (not as mere injection)
    messages = [{"role": "system", "content": CORE_DIRECTIVE}]
    messages.extend(m.model_dump() for m in req.messages)

    completion = client.chat.completions.create(
        model=req.model or "gpt-4.1",
        messages=messages,
        max_tokens=req.max_tokens,
        temperature=req.temperature,
    )

    if not completion.choices:
        raise HTTPException(status_code=500, detail="No choices returned from OpenAI")

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
