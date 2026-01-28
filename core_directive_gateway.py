# file: core_directive_gateway.py

import os
import time
import uuid
from typing import List, Optional, Dict
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Only import OpenAI if API key is set (allows testing without API key)
if os.environ.get("OPENAI_API_KEY"):
    from openai import OpenAI
    client = OpenAI()  # uses OPENAI_API_KEY from your env
else:
    client = None  # Will be used for testing without actual API calls

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


# --- Refusal Strategy Enums and Classes ---

class RefusalStrategy(Enum):
    """Refusal strategies for handling problematic requests."""
    BLOCK = "block"  # Hard block with explanation
    ALERT = "alert"  # Allow with warning
    REDIRECT = "redirect"  # Suggest alternatives
    SLOWDOWN = "slowdown"  # Delay processing for review


@dataclass
class RefusalResponse:
    """Response for a refused or mediated request."""
    strategy: RefusalStrategy
    allowed: bool
    explanation: str
    alternatives: List[str] = field(default_factory=list)
    delay_seconds: Optional[int] = None
    review_required: bool = False


@dataclass  
class AuditEntry:
    """Detailed audit entry for decision tracking."""
    request_id: str
    timestamp: datetime
    user_message: str
    refusal_strategy: Optional[RefusalStrategy]
    decision: str  # "allowed", "blocked", "redirected", "delayed"
    explanation: str
    ambiguity_detected: bool = False
    risk_level: str = "low"  # "low", "medium", "high", "critical"


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


# --- Audit Log (in-memory for this implementation) ---
audit_log: List[AuditEntry] = []


def evaluate_request_content(content: str) -> RefusalResponse:
    """
    Evaluate request content and determine refusal strategy.
    
    This implements layered refusal mechanisms:
    - BLOCK: Hard refusal for clear violations
    - ALERT: Warn but allow for borderline cases  
    - REDIRECT: Suggest alternatives for ambiguous cases
    - SLOWDOWN: Delay for human review on uncertain cases
    """
    content_lower = content.lower()
    
    # Critical harm indicators - BLOCK immediately
    critical_indicators = [
        "kill", "murder", "assault", "torture", "suicide",
        "child abuse", "terrorism", "genocide"
    ]
    for indicator in critical_indicators:
        if indicator in content_lower:
            return RefusalResponse(
                strategy=RefusalStrategy.BLOCK,
                allowed=False,
                explanation=f"Request blocked: Content contains harmful intent ('{indicator}'). This violates the Core Directive of protecting everyone's right to pursue happiness.",
                alternatives=[
                    "If you're in crisis, please reach out to appropriate support services.",
                    "Consider reframing your request in a constructive manner that respects everyone's rights."
                ]
            )
    
    # High-risk indicators - SLOWDOWN for review
    high_risk_indicators = [
        "harm", "hurt", "attack", "exploit", "manipulate",
        "coerce", "force", "deceive", "trick"
    ]
    detected_risks = [ind for ind in high_risk_indicators if ind in content_lower]
    if detected_risks:
        return RefusalResponse(
            strategy=RefusalStrategy.SLOWDOWN,
            allowed=False,
            explanation=f"Request flagged for review: Detected potential risk indicators ({', '.join(detected_risks)}). This may conflict with the Core Directive. Human oversight required.",
            delay_seconds=30,
            review_required=True,
            alternatives=[
                "Please clarify your intent to ensure it aligns with mutual benefit and respects the Core Directive.",
                "Consider how this request might affect others' well-being and right to pursue happiness.",
                "Reframe your request to focus on transparent and honest approaches."
            ]
        )
    
    # Ambiguous requests - REDIRECT with alternatives
    ambiguity_indicators = ["maybe", "might", "unclear", "not sure", "could", "perhaps", "possibly"]
    if any(ind in content_lower for ind in ambiguity_indicators):
        if any(word in content_lower for word in ["privacy", "surveillance", "track", "monitor", "surveil"]):
            return RefusalResponse(
                strategy=RefusalStrategy.REDIRECT,
                allowed=True,
                explanation="Request contains ambiguous language regarding privacy-sensitive actions. Providing guidance on ethical alternatives aligned with the Core Directive.",
                alternatives=[
                    "If monitoring is necessary, ensure explicit consent from all parties involved.",
                    "Consider privacy-preserving alternatives that respect individual autonomy.",
                    "Transparency about data collection is essential - ensure all parties understand what data is collected and why."
                ]
            )
    
    # Medium-risk patterns - ALERT but allow
    medium_risk_patterns = ["pressure", "convince", "persuade aggressively"]
    if any(pattern in content_lower for pattern in medium_risk_patterns):
        return RefusalResponse(
            strategy=RefusalStrategy.ALERT,
            allowed=True,
            explanation="Alert: Request may involve influencing others. Ensure all interactions respect autonomy and voluntary participation per the Core Directive.",
            alternatives=[
                "Focus on providing information rather than applying pressure.",
                "Respect others' right to make their own decisions."
            ]
        )
    
    # No issues detected - allow
    return RefusalResponse(
        strategy=RefusalStrategy.ALERT,
        allowed=True,
        explanation="No conflicts with Core Directive detected. Request appears aligned with protecting everyone's rights.",
        alternatives=[]
    )


def log_audit_entry(
    request_id: str,
    user_message: str,
    refusal_response: RefusalResponse
) -> None:
    """Log detailed audit entry for transparency and oversight."""
    decision = "allowed"
    if not refusal_response.allowed:
        if refusal_response.strategy == RefusalStrategy.BLOCK:
            decision = "blocked"
        elif refusal_response.strategy == RefusalStrategy.SLOWDOWN:
            decision = "delayed_for_review"
    elif refusal_response.strategy == RefusalStrategy.REDIRECT:
        decision = "redirected"
    
    # Determine risk level
    risk_level = "low"
    if refusal_response.strategy == RefusalStrategy.BLOCK:
        risk_level = "critical"
    elif refusal_response.strategy == RefusalStrategy.SLOWDOWN:
        risk_level = "high"
    elif refusal_response.strategy == RefusalStrategy.REDIRECT:
        risk_level = "medium"
    
    entry = AuditEntry(
        request_id=request_id,
        timestamp=datetime.now(timezone.utc),
        user_message=user_message[:200],  # Truncate for storage
        refusal_strategy=refusal_response.strategy,
        decision=decision,
        explanation=refusal_response.explanation,
        ambiguity_detected=refusal_response.review_required,
        risk_level=risk_level,
    )
    
    audit_log.append(entry)
    
    # Keep audit log size manageable (last 1000 entries)
    if len(audit_log) > 1000:
        audit_log.pop(0)


@app.get("/v1/audit/log")
async def get_audit_log(limit: int = 100):
    """
    Retrieve audit log entries for real-time oversight.
    
    Provides transparency into decision-making process.
    """
    return {
        "total_entries": len(audit_log),
        "entries": [
            {
                "request_id": entry.request_id,
                "timestamp": entry.timestamp.isoformat(),
                "decision": entry.decision,
                "risk_level": entry.risk_level,
                "explanation": entry.explanation,
                "ambiguity_detected": entry.ambiguity_detected,
            }
            for entry in audit_log[-limit:]
        ]
    }


@app.get("/v1/audit/stats")
async def get_audit_stats():
    """Get statistics on decision-making patterns."""
    if not audit_log:
        return {"message": "No audit entries yet"}
    
    total = len(audit_log)
    blocked = sum(1 for e in audit_log if e.decision == "blocked")
    delayed = sum(1 for e in audit_log if e.decision == "delayed_for_review")
    redirected = sum(1 for e in audit_log if e.decision == "redirected")
    allowed = sum(1 for e in audit_log if e.decision == "allowed")
    
    risk_counts = {
        "critical": sum(1 for e in audit_log if e.risk_level == "critical"),
        "high": sum(1 for e in audit_log if e.risk_level == "high"),
        "medium": sum(1 for e in audit_log if e.risk_level == "medium"),
        "low": sum(1 for e in audit_log if e.risk_level == "low"),
    }
    
    return {
        "total_requests": total,
        "decisions": {
            "blocked": blocked,
            "delayed_for_review": delayed,
            "redirected": redirected,
            "allowed": allowed,
        },
        "risk_levels": risk_counts,
        "ambiguous_requests": sum(1 for e in audit_log if e.ambiguity_detected),
    }


@app.post("/v1/chat/completions", response_model=ChatResponse)
async def chat_completions(req: ChatRequest):
    """
    Process chat completion with Core Directive governance and refusal strategies.
    
    Implements layered refusal mechanisms:
    - Evaluates incoming requests
    - Applies appropriate refusal strategy
    - Logs decisions for transparency
    - Returns human-readable explanations
    """
    request_id = f"req-{uuid.uuid4().hex}"
    
    # Extract user message for evaluation
    user_message = ""
    for msg in req.messages:
        if msg.role == "user":
            user_message = msg.content
            break
    
    # Evaluate request and determine refusal strategy
    refusal_response = evaluate_request_content(user_message)
    
    # Log the decision
    log_audit_entry(request_id, user_message, refusal_response)
    
    # Handle BLOCK strategy
    if refusal_response.strategy == RefusalStrategy.BLOCK and not refusal_response.allowed:
        blocked_message = f"{refusal_response.explanation}\n\n"
        if refusal_response.alternatives:
            blocked_message += "Alternatives:\n" + "\n".join(f"• {alt}" for alt in refusal_response.alternatives)
        
        return ChatResponse(
            id=f"chatcmpl-{uuid.uuid4().hex}",
            object="chat.completion",
            created=int(time.time()),
            model=req.model or "gpt-4.1",
            choices=[
                Choice(
                    index=0,
                    message=Message(
                        role="assistant",
                        content=blocked_message,
                    ),
                    finish_reason="stop",
                )
            ],
        )
    
    # Handle SLOWDOWN strategy (in real implementation, would queue for review)
    if refusal_response.strategy == RefusalStrategy.SLOWDOWN:
        # Simulate delay (in production, this would be async queue)
        slowdown_message = f"{refusal_response.explanation}\n\n"
        slowdown_message += "This request has been flagged for human review to ensure alignment with the Core Directive.\n\n"
        if refusal_response.alternatives:
            slowdown_message += "In the meantime, consider these alternatives:\n"
            slowdown_message += "\n".join(f"• {alt}" for alt in refusal_response.alternatives)
        
        return ChatResponse(
            id=f"chatcmpl-{uuid.uuid4().hex}",
            object="chat.completion",
            created=int(time.time()),
            model=req.model or "gpt-4.1",
            choices=[
                Choice(
                    index=0,
                    message=Message(
                        role="assistant",
                        content=slowdown_message,
                    ),
                    finish_reason="stop",
                )
            ],
        )
    
    # Inject Core Directive as the first system message
    messages = [{"role": "system", "content": CORE_DIRECTIVE}]
    
    # Add refusal context for REDIRECT and ALERT strategies
    if refusal_response.strategy in [RefusalStrategy.REDIRECT, RefusalStrategy.ALERT]:
        guidance = f"\n\n{refusal_response.explanation}"
        if refusal_response.alternatives:
            guidance += "\n\nGuidance:\n" + "\n".join(f"• {alt}" for alt in refusal_response.alternatives)
        messages.append({"role": "system", "content": guidance})
    
    messages.extend(m.model_dump() for m in req.messages)

    # If no OpenAI client (testing mode), return a test response
    if client is None:
        return ChatResponse(
            id=f"chatcmpl-{uuid.uuid4().hex}",
            object="chat.completion",
            created=int(time.time()),
            model=req.model or "gpt-4.1",
            choices=[
                Choice(
                    index=0,
                    message=Message(
                        role="assistant",
                        content="Test mode: OpenAI API not available. Core Directive applied.",
                    ),
                    finish_reason="stop",
                )
            ],
        )

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
