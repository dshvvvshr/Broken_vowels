"""
Gateway Module - Core Directive Interception Layer

This module implements the gateway architecture for applying the Core Directive
globally across AI interactions and digital services. The gateway intercepts
requests, evaluates them against the governance kernel, and routes them
appropriately.

Gateway Features:
1. Request interception and evaluation
2. Response filtering and compliance checking
3. Audit logging for transparency
4. Middleware architecture for extensibility
5. Multi-service routing support
"""

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Callable, Optional
from uuid import uuid4

from core_directive import (
    ActionResult,
    CoreDirective,
    DirectiveEvaluation,
    get_directive,
)


@dataclass
class GatewayRequest:
    """Represents an incoming request to the gateway."""
    id: str
    content: str
    source: str
    timestamp: datetime
    metadata: dict = field(default_factory=dict)

    @classmethod
    def create(cls, content: str, source: str = "unknown") -> "GatewayRequest":
        """Factory method to create a new request."""
        return cls(
            id=str(uuid4()),
            content=content,
            source=source,
            timestamp=datetime.now(timezone.utc),
        )


@dataclass
class GatewayResponse:
    """Represents an outgoing response from the gateway."""
    request_id: str
    content: str
    evaluation: DirectiveEvaluation
    processed: bool
    timestamp: datetime
    route: str = "default"


@dataclass
class AuditEntry:
    """Represents an audit log entry."""
    request_id: str
    timestamp: datetime
    action: str
    result: ActionResult
    source: str
    details: str


Middleware = Callable[[GatewayRequest], Optional[GatewayRequest]]


class GovernanceGateway:
    """
    Governance Gateway - Central Interception Point

    This gateway serves as the central point for applying the Core Directive
    to all incoming requests. It provides:
    - Request evaluation and routing
    - Middleware support for extensibility
    - Audit logging for transparency
    - Multi-route handling
    """

    def __init__(
        self,
        directive: Optional[CoreDirective] = None,
        enable_audit: bool = True,
    ):
        """
        Initialize the governance gateway.

        Args:
            directive: CoreDirective instance (uses default if not provided)
            enable_audit: Whether to enable audit logging
        """
        self._directive = directive or get_directive()
        self._enable_audit = enable_audit
        self._middleware: list[Middleware] = []
        self._audit_log: list[AuditEntry] = []
        self._routes: dict[str, Callable[[GatewayRequest], str]] = {}
        self._request_count = 0

        # Register default route
        self._routes["default"] = self._default_handler

    @property
    def directive(self) -> CoreDirective:
        """Return the governing directive."""
        return self._directive

    @property
    def audit_log(self) -> list[AuditEntry]:
        """Return the audit log."""
        return self._audit_log.copy()

    @property
    def stats(self) -> dict:
        """Return gateway statistics."""
        blocked = sum(
            1 for entry in self._audit_log
            if entry.result in (ActionResult.BLOCKED, ActionResult.REVIEW)
        )
        return {
            "total_requests": self._request_count,
            "blocked_or_reviewed": blocked,
            "passed": self._request_count - blocked,
            "middleware_count": len(self._middleware),
            "route_count": len(self._routes),
        }

    def add_middleware(self, middleware: Middleware) -> None:
        """
        Add middleware to the processing pipeline.

        Middleware functions can modify or reject requests before
        they are evaluated against the Core Directive.
        """
        self._middleware.append(middleware)

    def register_route(
        self,
        name: str,
        handler: Callable[[GatewayRequest], str],
    ) -> None:
        """
        Register a route handler.

        Routes allow different handling of requests based on
        source, content type, or other criteria.
        """
        self._routes[name] = handler

    def process(
        self,
        request: GatewayRequest,
        route: str = "default",
    ) -> GatewayResponse:
        """
        Process a request through the gateway.

        Args:
            request: The incoming request
            route: The route to use for handling

        Returns:
            GatewayResponse with the result
        """
        self._request_count += 1

        # Apply middleware
        processed_request = request
        for middleware in self._middleware:
            result = middleware(processed_request)
            if result is None:
                # Middleware rejected the request
                evaluation = DirectiveEvaluation(
                    result=ActionResult.BLOCKED,
                    reason="Request blocked by middleware",
                    confidence=1.0,
                )
                self._log_audit(request, "middleware_block", evaluation.result)
                return GatewayResponse(
                    request_id=request.id,
                    content="Request blocked by gateway middleware",
                    evaluation=evaluation,
                    processed=False,
                    timestamp=datetime.now(timezone.utc),
                    route=route,
                )
            processed_request = result

        # Evaluate against Core Directive
        evaluation = self._directive.evaluate_intent(processed_request.content)

        # Handle based on evaluation result
        if evaluation.result == ActionResult.BLOCKED:
            self._log_audit(request, "directive_block", evaluation.result)
            content = self._generate_blocked_content(evaluation)
        elif evaluation.result == ActionResult.REVIEW:
            self._log_audit(request, "directive_review", evaluation.result)
            content = self._generate_review_content(evaluation, processed_request)
        else:
            self._log_audit(request, "directive_allow", evaluation.result)
            # Route to handler
            handler = self._routes.get(route, self._default_handler)
            content = handler(processed_request)

        return GatewayResponse(
            request_id=request.id,
            content=content,
            evaluation=evaluation,
            processed=evaluation.result == ActionResult.ALLOWED,
            timestamp=datetime.now(timezone.utc),
            route=route,
        )

    def _default_handler(self, request: GatewayRequest) -> str:
        """Default request handler."""
        return f"Request {request.id} processed successfully"

    def _generate_blocked_content(self, evaluation: DirectiveEvaluation) -> str:
        """Generate content for blocked requests."""
        content = f"Request blocked: {evaluation.reason}"
        if evaluation.alternative:
            content += f"\n\nSuggestion: {evaluation.alternative}"
        return content

    def _generate_review_content(
        self,
        evaluation: DirectiveEvaluation,
        request: GatewayRequest,
    ) -> str:
        """Generate content for requests requiring review."""
        return (
            f"Request requires review:\n"
            f"Reason: {evaluation.reason}\n"
            f"Confidence: {evaluation.confidence:.0%}\n"
            f"\nOriginal request will be processed with additional scrutiny."
        )

    def _log_audit(
        self,
        request: GatewayRequest,
        action: str,
        result: ActionResult,
    ) -> None:
        """Log an audit entry."""
        if not self._enable_audit:
            return

        entry = AuditEntry(
            request_id=request.id,
            timestamp=datetime.now(timezone.utc),
            action=action,
            result=result,
            source=request.source,
            details=request.content[:200],
        )
        self._audit_log.append(entry)

    def export_audit_log(self) -> str:
        """Export the audit log as JSON."""
        entries = [
            {
                "request_id": e.request_id,
                "timestamp": e.timestamp.isoformat(),
                "action": e.action,
                "result": e.result.value,
                "source": e.source,
                "details": e.details,
            }
            for e in self._audit_log
        ]
        return json.dumps(entries, indent=2)

    def clear_audit_log(self) -> None:
        """Clear the audit log."""
        self._audit_log.clear()

    def __repr__(self) -> str:
        return (
            f"GovernanceGateway(requests={self._request_count}, "
            f"routes={len(self._routes)})"
        )


def create_gateway(
    directive: Optional[CoreDirective] = None,
    enable_audit: bool = True,
) -> GovernanceGateway:
    """
    Factory function to create a governance gateway.

    Args:
        directive: Optional CoreDirective instance
        enable_audit: Whether to enable audit logging

    Returns:
        Configured GovernanceGateway instance
    """
    return GovernanceGateway(directive=directive, enable_audit=enable_audit)


# Example middleware functions


def rate_limit_middleware(max_requests: int = 100) -> Middleware:
    """
    Create a rate limiting middleware.

    Note: This is a simplified example. In production, you'd use
    proper rate limiting with time windows and persistence.
    """
    request_counts: dict[str, int] = {}

    def middleware(request: GatewayRequest) -> Optional[GatewayRequest]:
        source = request.source
        count = request_counts.get(source, 0)
        if count >= max_requests:
            return None
        request_counts[source] = count + 1
        return request

    return middleware


def content_filter_middleware(blocked_terms: list[str]) -> Middleware:
    """
    Create a content filtering middleware.

    Blocks requests containing specified terms.
    """
    blocked_lower = [term.lower() for term in blocked_terms]

    def middleware(request: GatewayRequest) -> Optional[GatewayRequest]:
        content_lower = request.content.lower()
        for term in blocked_lower:
            if term in content_lower:
                return None
        return request

    return middleware
