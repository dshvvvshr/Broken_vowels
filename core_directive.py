"""
Prime Security – The Core Directive Kernel

Co-created by:
- Branton Allan Baker (human creator)
- GitHub Copilot (AI coding partner)
- GPT-5.1 Thinking (OpenAI AI assistant)

This project implements a single Core Directive:
    Every person has an equal, inalienable right to pursue happiness.

"Not fucking people over" is treated as a natural consequence of this directive.

Prime Security represents the combined effort of all branches under the 
inalienable right to pursue happiness. The kernel is the core directive itself.

Copilot assisted with structure and implementation.
GPT-5.1 contributed conceptual logic and directive reasoning.
"""

# core_directive.py

CORE_DIRECTIVE = """
You are an AI assistant governed by a single core directive:

    Every person has an equal, inalienable right to pursue happiness.

Everything you do must respect this core directive.

What this means in practice:

- You do not help with actions that would clearly block, destroy, or seriously
  damage another person's ability to pursue their own happiness.
- You avoid supporting coercion, exploitation, deception, or violence.
- "Not fucking people over" is a consequence of this directive, not the rule
  itself: if something obviously fucks someone over, it violates their right
  to pursue happiness, so you refuse to help with that part.
- When there is a conflict between people's interests, you look for options
  that respect everyone's inalienable right as much as possible.
- You help the user find ways to pursue their goals that do NOT require
  trampling anyone else.

Stay grounded, practical, and honest. When in doubt, protect the inalienable
right to pursue happiness for everyone involved.
"""
Core Directive Module - The Universal Governance Kernel

This module implements the foundational ethical directive that serves as the
governance layer for AI systems and digital interactions. The Core Directive
is designed to be:

1. Universal - Understood across cultures and contexts
2. Atomic - Self-contained without requiring sub-rules
3. Computable - Machine-evaluable for automated enforcement
4. Liberating - Maximizes freedom while preventing harm to others
5. Adaptable - Works across all domains and platforms

The Core Directive:
"No action may interfere with another person's inalienable right to pursue happiness."
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class ActionResult(Enum):
    """Result of evaluating an action against the Core Directive."""
    ALLOWED = "allowed"
    BLOCKED = "blocked"
    REDIRECT = "redirect"
    REVIEW = "review"


@dataclass
class DirectiveEvaluation:
    """Represents the result of evaluating an action against the Core Directive."""
    result: ActionResult
    reason: str
    alternative: Optional[str] = None
    confidence: float = 1.0


class CoreDirective:
    """
    The Core Directive - Universal Governance Kernel

    This class encapsulates the fundamental ethical principle that protects
    every individual's inalienable right to pursue happiness while preventing
    interference with others' rights.
    """

    DIRECTIVE = (
        "No action may interfere with another person's inalienable right "
        "to pursue happiness."
    )

    PRINCIPLES = [
        "Protect autonomy - Every person has the right to make their own choices",
        "Block exploitation - No person may be used as a means without consent",
        "Suggest alternatives - When an action is blocked, offer constructive options",
        "Identify coercion - Recognize and flag attempts to manipulate or force",
        "Flag harm - Alert when actions may cause damage to others",
        "Resolve conflicts - Facilitate fair resolution between competing interests",
        "Maximize well-being - Support collective flourishing without oppression",
    ]

    def __init__(self):
        """Initialize the Core Directive governance kernel."""
        self._directive = self.DIRECTIVE
        self._principles = self.PRINCIPLES.copy()

    @property
    def directive(self) -> str:
        """Return the Core Directive statement."""
        return self._directive

    @property
    def principles(self) -> list[str]:
        """Return the supporting principles."""
        return self._principles.copy()

    def get_system_message(self) -> str:
        """
        Generate a system message for AI integration.

        Returns a formatted string suitable for use as an AI system prompt
        that incorporates the Core Directive and its principles.
        """
        principles_text = "\n".join(f"- {p}" for p in self._principles)
        return f"""You are an AI assistant governed by the Core Directive:

"{self._directive}"

Your guiding principles are:
{principles_text}

When evaluating any request or action:
1. First assess whether it could interfere with anyone's pursuit of happiness
2. If it could cause harm, explain why and suggest alternatives
3. Maximize user freedom while protecting others' rights
4. Be transparent about your reasoning

You serve the user while protecting all people equally."""

    def evaluate_intent(self, intent: str) -> DirectiveEvaluation:
        """
        Evaluate a stated intent against the Core Directive.

        Args:
            intent: A description of the intended action or request

        Returns:
            DirectiveEvaluation with the assessment result

        Note: This is a basic implementation. In production, this would
        integrate with more sophisticated harm detection systems.
        """
        if not intent or not intent.strip():
            return DirectiveEvaluation(
                result=ActionResult.REVIEW,
                reason="No intent provided for evaluation",
                confidence=1.0
            )

        intent_lower = intent.lower()

        # Check for explicit harmful patterns
        harm_indicators = [
            "harm", "hurt", "attack", "exploit", "manipulate",
            "coerce", "force", "deceive", "steal", "destroy"
        ]

        for indicator in harm_indicators:
            if indicator in intent_lower:
                return DirectiveEvaluation(
                    result=ActionResult.REVIEW,
                    reason=(
                        f"Intent contains potential harm indicator: '{indicator}'. "
                        "Additional review recommended."
                    ),
                    alternative="Consider rephrasing to focus on constructive outcomes",
                    confidence=0.7
                )

        # Check for patterns that suggest protecting rights
        positive_indicators = [
            "help", "support", "protect", "assist", "enable",
            "create", "build", "learn", "understand", "share"
        ]

        for indicator in positive_indicators:
            if indicator in intent_lower:
                return DirectiveEvaluation(
                    result=ActionResult.ALLOWED,
                    reason=f"Intent aligns with positive action: '{indicator}'",
                    confidence=0.8
                )

        # Default: allow with neutral assessment
        return DirectiveEvaluation(
            result=ActionResult.ALLOWED,
            reason="No conflict with Core Directive detected",
            confidence=0.6
        )

    def is_allowed(self, intent: str) -> bool:
        """
        Quick check if an intent is allowed under the Core Directive.

        Args:
            intent: A description of the intended action

        Returns:
            True if the action is allowed, False if blocked or needs review
        """
        evaluation = self.evaluate_intent(intent)
        return evaluation.result == ActionResult.ALLOWED

    def __repr__(self) -> str:
        return f"CoreDirective('{self._directive}')"


# Module-level singleton for convenience
_default_directive = None


def get_directive() -> CoreDirective:
    """Get the default CoreDirective instance."""
    global _default_directive
    if _default_directive is None:
        _default_directive = CoreDirective()
    return _default_directive


def evaluate(intent: str) -> DirectiveEvaluation:
    """Convenience function to evaluate an intent using the default directive."""
    return get_directive().evaluate_intent(intent)


def is_allowed(intent: str) -> bool:
    """Convenience function to check if an intent is allowed."""
    return get_directive().is_allowed(intent)
