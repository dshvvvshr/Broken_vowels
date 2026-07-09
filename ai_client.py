# ai_client.py

from openai import OpenAI
from core_directive import CORE_DIRECTIVE

# Uses OPENAI_API_KEY from your environment (do NOT hard-code it)
client = OpenAI()


def ask_happiness_core_ai(user_message: str) -> str:
    """
    Ask the AI that is governed by the inalienable right to pursue happiness.
    """
    completion = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": CORE_DIRECTIVE},
            {"role": "user", "content": user_message},
        ],
    )
    return completion.choices[0].message.content


if __name__ == "__main__":
    print("Happiness-Core AI. Ctrl+C to quit.\n")
    while True:
        try:
            msg = input("You: ")
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            break

        reply = ask_happiness_core_ai(msg)
        print("AI:", reply)
        print()
"""
AI Client Module - Core Directive Integration Layer

This module provides an AI client wrapper that integrates the Core Directive
governance kernel into AI interactions. It ensures that all AI responses
adhere to the fundamental ethical principle of protecting individuals'
right to pursue happiness.

The AI Client:
1. Wraps AI model interactions with Core Directive enforcement
2. Provides system messages that incorporate the governance kernel
3. Evaluates requests before processing
4. Filters responses for compliance
"""

from dataclasses import dataclass
from typing import Callable, Optional, Protocol

from core_directive import (
    ActionResult,
    CoreDirective,
    DirectiveEvaluation,
    get_directive,
)


class AIModelProtocol(Protocol):
    """Protocol defining the interface for AI models."""

    def generate(self, prompt: str, system_message: str) -> str:
        """Generate a response given a prompt and system message."""
        ...


@dataclass
class AIResponse:
    """Represents a governed AI response."""
    content: str
    was_modified: bool
    directive_evaluation: DirectiveEvaluation
    original_prompt: str


class GovernedAIClient:
    """
    AI Client with Core Directive Governance

    This client wraps AI model interactions to ensure compliance with
    the Core Directive. It evaluates incoming requests and outgoing
    responses to protect all individuals' rights.
    """

    def __init__(
        self,
        model: Optional[AIModelProtocol] = None,
        directive: Optional[CoreDirective] = None,
        pre_process_hook: Optional[Callable[[str], str]] = None,
        post_process_hook: Optional[Callable[[str], str]] = None,
    ):
        """
        Initialize the governed AI client.

        Args:
            model: The underlying AI model to wrap
            directive: CoreDirective instance (uses default if not provided)
            pre_process_hook: Optional function to pre-process prompts
            post_process_hook: Optional function to post-process responses
        """
        self._model = model
        self._directive = directive or get_directive()
        self._pre_process_hook = pre_process_hook
        self._post_process_hook = post_process_hook
        self._request_count = 0
        self._blocked_count = 0

    @property
    def directive(self) -> CoreDirective:
        """Return the governing directive."""
        return self._directive

    @property
    def stats(self) -> dict:
        """Return usage statistics."""
        return {
            "total_requests": self._request_count,
            "blocked_requests": self._blocked_count,
            "allowed_requests": self._request_count - self._blocked_count,
        }

    def get_system_message(self) -> str:
        """Get the system message incorporating the Core Directive."""
        return self._directive.get_system_message()

    def evaluate_request(self, prompt: str) -> DirectiveEvaluation:
        """
        Evaluate a request against the Core Directive.

        Args:
            prompt: The user's prompt/request

        Returns:
            DirectiveEvaluation with the assessment
        """
        return self._directive.evaluate_intent(prompt)

    def process(self, prompt: str) -> AIResponse:
        """
        Process a prompt through the governed AI client.

        Args:
            prompt: The user's prompt/request

        Returns:
            AIResponse with the result and governance metadata
        """
        self._request_count += 1

        # Pre-process the prompt if a hook is provided
        processed_prompt = prompt
        if self._pre_process_hook:
            processed_prompt = self._pre_process_hook(prompt)

        # Evaluate against Core Directive
        evaluation = self.evaluate_request(processed_prompt)

        # Handle blocked requests
        if evaluation.result == ActionResult.BLOCKED:
            self._blocked_count += 1
            content = self._generate_blocked_response(evaluation)
            return AIResponse(
                content=content,
                was_modified=True,
                directive_evaluation=evaluation,
                original_prompt=prompt,
            )

        # Generate response if model is available
        if self._model:
            system_message = self.get_system_message()
            content = self._model.generate(processed_prompt, system_message)
        else:
            # No model configured - return evaluation info
            content = self._generate_no_model_response(evaluation)

        # Post-process the response if a hook is provided
        if self._post_process_hook:
            content = self._post_process_hook(content)

        return AIResponse(
            content=content,
            was_modified=bool(self._pre_process_hook or self._post_process_hook),
            directive_evaluation=evaluation,
            original_prompt=prompt,
        )

    def _generate_blocked_response(self, evaluation: DirectiveEvaluation) -> str:
        """Generate a response for blocked requests."""
        response = (
            f"This request cannot be processed as it may conflict with the "
            f"Core Directive.\n\n"
            f"Reason: {evaluation.reason}\n"
        )
        if evaluation.alternative:
            response += f"\nAlternative: {evaluation.alternative}"
        return response

    def _generate_no_model_response(self, evaluation: DirectiveEvaluation) -> str:
        """Generate a response when no AI model is configured."""
        return (
            f"Request evaluated by Core Directive:\n"
            f"Result: {evaluation.result.value}\n"
            f"Reason: {evaluation.reason}\n"
            f"Confidence: {evaluation.confidence:.0%}"
        )

    def __repr__(self) -> str:
        return (
            f"GovernedAIClient(model={self._model}, "
            f"requests={self._request_count})"
        )


class MockAIModel:
    """
    Mock AI model for testing and demonstration.

    This provides a simple echo-style response for testing
    the governance layer without a real AI model.
    """

    def __init__(self, response_prefix: str = "AI Response:"):
        self._prefix = response_prefix

    def generate(self, prompt: str, system_message: str) -> str:
        """Generate a mock response."""
        return (
            f"{self._prefix}\n"
            f"Prompt received: {prompt[:100]}{'...' if len(prompt) > 100 else ''}\n"
            f"Governed by Core Directive: Yes"
        )


def create_client(
    model: Optional[AIModelProtocol] = None,
    directive: Optional[CoreDirective] = None,
) -> GovernedAIClient:
    """
    Factory function to create a governed AI client.

    Args:
        model: Optional AI model to wrap
        directive: Optional CoreDirective instance

    Returns:
        Configured GovernedAIClient instance
    """
    return GovernedAIClient(model=model, directive=directive)


def create_test_client() -> GovernedAIClient:
    """
    Create a test client with a mock AI model.

    Returns:
        GovernedAIClient configured with MockAIModel
    """
    return GovernedAIClient(model=MockAIModel())
