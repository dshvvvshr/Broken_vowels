"""
Core Directive Governance Layer

A universal governance kernel for AI systems and digital interactions
that protects every individual's inalienable right to pursue happiness.

Modules:
    core_directive: The fundamental governance kernel
    ai_client: AI client integration layer
    gateway: Request interception and routing
    evaluator: Detailed evaluation engine
"""

from core_directive import (
    ActionResult,
    CoreDirective,
    DirectiveEvaluation,
    evaluate,
    get_directive,
    is_allowed,
)
from ai_client import (
    AIResponse,
    GovernedAIClient,
    MockAIModel,
    create_client,
    create_test_client,
)
from gateway import (
    AuditEntry,
    GovernanceGateway,
    GatewayRequest,
    GatewayResponse,
    create_gateway,
    content_filter_middleware,
    rate_limit_middleware,
)
from evaluator import (
    ConflictAssessment,
    ConflictType,
    DetailedEvaluation,
    DirectiveEvaluator,
    ImpactAssessment,
    ImpactCategory,
    evaluate_detailed,
    get_evaluator,
)

__version__ = "0.1.0"
__all__ = [
    # Core Directive
    "ActionResult",
    "CoreDirective",
    "DirectiveEvaluation",
    "evaluate",
    "get_directive",
    "is_allowed",
    # AI Client
    "AIResponse",
    "GovernedAIClient",
    "MockAIModel",
    "create_client",
    "create_test_client",
    # Gateway
    "AuditEntry",
    "GovernanceGateway",
    "GatewayRequest",
    "GatewayResponse",
    "create_gateway",
    "content_filter_middleware",
    "rate_limit_middleware",
    # Evaluator
    "ConflictAssessment",
    "ConflictType",
    "DetailedEvaluation",
    "DirectiveEvaluator",
    "ImpactAssessment",
    "ImpactCategory",
    "evaluate_detailed",
    "get_evaluator",
]
