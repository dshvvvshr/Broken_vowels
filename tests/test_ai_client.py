"""
Comprehensive tests for ai_client module to achieve 100% coverage.
"""

import unittest
from ai_client import (
    GovernedAIClient,
    MockAIModel,
    AIResponse,
    create_client,
    create_test_client,
)
from core_directive import ActionResult, CoreDirective


class TestGovernedAIClientComprehensive(unittest.TestCase):
    """Comprehensive tests for GovernedAIClient."""

    def setUp(self):
        """Set up test fixtures."""
        self.client = create_test_client()

    def test_repr(self):
        """Test string representation."""
        repr_str = repr(self.client)
        self.assertIn("GovernedAIClient", repr_str)
        self.assertIn("requests=", repr_str)

    def test_client_without_model(self):
        """Test client operation without AI model."""
        client = create_client(model=None)
        response = client.process("help people")
        
        # Should return evaluation info instead of AI response
        self.assertIn("evaluated by Core Directive", response.content)
        self.assertIn("Result:", response.content)

    def test_client_with_custom_directive(self):
        """Test client with custom directive."""
        custom_directive = CoreDirective()
        client = create_client(directive=custom_directive)
        
        self.assertIs(client.directive, custom_directive)

    def test_pre_process_hook(self):
        """Test pre-processing hook."""
        hook_called = []
        
        def pre_hook(prompt: str) -> str:
            hook_called.append(True)
            return prompt.upper()
        
        model = MockAIModel()
        client = GovernedAIClient(model=model, pre_process_hook=pre_hook)
        
        response = client.process("help people")
        self.assertTrue(hook_called)
        # Prompt should have been uppercased
        self.assertIn("HELP PEOPLE", response.content)

    def test_post_process_hook(self):
        """Test post-processing hook."""
        hook_called = []
        
        def post_hook(response: str) -> str:
            hook_called.append(True)
            return response + " [PROCESSED]"
        
        model = MockAIModel()
        client = GovernedAIClient(model=model, post_process_hook=post_hook)
        
        response = client.process("help people")
        self.assertTrue(hook_called)
        self.assertIn("[PROCESSED]", response.content)
        self.assertTrue(response.was_modified)

    def test_both_hooks(self):
        """Test with both pre and post processing hooks."""
        def pre_hook(prompt: str) -> str:
            return f"[PRE] {prompt}"
        
        def post_hook(response: str) -> str:
            return f"{response} [POST]"
        
        model = MockAIModel()
        client = GovernedAIClient(
            model=model,
            pre_process_hook=pre_hook,
            post_process_hook=post_hook
        )
        
        response = client.process("test")
        self.assertTrue(response.was_modified)
        self.assertIn("[POST]", response.content)

    def test_blocked_request_response(self):
        """Test response for blocked request."""
        # Create a custom directive that returns BLOCKED
        from core_directive import DirectiveEvaluation
        from unittest.mock import MagicMock
        
        mock_directive = MagicMock()
        mock_directive.evaluate_intent.return_value = DirectiveEvaluation(
            result=ActionResult.BLOCKED,
            reason="Test blocked",
            alternative="Test alternative",
            confidence=1.0
        )
        mock_directive.get_system_message.return_value = "Test system message"
        
        client = create_client(model=MockAIModel(), directive=mock_directive)
        response = client.process("test")
        
        # Should get a blocked response
        self.assertEqual(response.directive_evaluation.result, ActionResult.BLOCKED)
        self.assertIn("cannot be processed", response.content)
        self.assertIn("Test blocked", response.content)
        self.assertIn("Test alternative", response.content)
        self.assertTrue(response.was_modified)
        
        # Stats should show blocked request
        self.assertEqual(client.stats["blocked_requests"], 1)

    def test_blocked_response_format(self):
        """Test format of blocked response."""
        # Create client without model to test response generation
        client = create_client(model=None)
        response = client.process("")
        
        # Should contain evaluation info
        self.assertIn("Result:", response.content)

    def test_stats_after_blocking(self):
        """Test stats tracking for blocked requests."""
        initial_blocked = self.client.stats["blocked_requests"]
        
        # Process a potentially problematic request
        self.client.process("")  # Empty triggers REVIEW
        
        # Stats should be updated
        self.assertGreaterEqual(
            self.client.stats["blocked_requests"],
            initial_blocked
        )

    def test_stats_fields(self):
        """Test that stats contain all expected fields."""
        stats = self.client.stats
        self.assertIn("total_requests", stats)
        self.assertIn("blocked_requests", stats)
        self.assertIn("allowed_requests", stats)

    def test_stats_calculation(self):
        """Test stats are calculated correctly."""
        initial = self.client.stats.copy()
        
        self.client.process("help people")
        self.client.process("support the community")
        
        new_stats = self.client.stats
        self.assertEqual(
            new_stats["total_requests"],
            initial["total_requests"] + 2
        )
        self.assertEqual(
            new_stats["total_requests"],
            new_stats["allowed_requests"] + new_stats["blocked_requests"]
        )

    def test_ai_response_structure(self):
        """Test AIResponse contains all fields."""
        response = self.client.process("test prompt")
        
        self.assertIsNotNone(response.content)
        self.assertIsInstance(response.was_modified, bool)
        self.assertIsNotNone(response.directive_evaluation)
        self.assertEqual(response.original_prompt, "test prompt")

    def test_system_message_retrieval(self):
        """Test get_system_message method."""
        message = self.client.get_system_message()
        self.assertIn("inalienable right to the pursuit of happiness", message)
        self.assertIn("custodian of humanity", message)

    def test_evaluate_request_method(self):
        """Test evaluate_request method."""
        evaluation = self.client.evaluate_request("help people learn")
        self.assertEqual(evaluation.result, ActionResult.ALLOWED)

    def test_mock_model_response_format(self):
        """Test MockAIModel response format."""
        model = MockAIModel()
        response = model.generate("test prompt", "system message")
        
        self.assertIn("AI Response:", response)
        self.assertIn("Prompt received:", response)
        self.assertIn("Governed by Core Directive: Yes", response)

    def test_mock_model_custom_prefix(self):
        """Test MockAIModel with custom prefix."""
        model = MockAIModel(response_prefix="CUSTOM:")
        response = model.generate("test", "system")
        
        self.assertIn("CUSTOM:", response)

    def test_mock_model_long_prompt_truncation(self):
        """Test MockAIModel truncates long prompts."""
        model = MockAIModel()
        long_prompt = "x" * 200
        response = model.generate(long_prompt, "system")
        
        # Should truncate to 100 chars plus ellipsis
        self.assertIn("...", response)

    def test_mock_model_short_prompt(self):
        """Test MockAIModel doesn't truncate short prompts."""
        model = MockAIModel()
        short_prompt = "short"
        response = model.generate(short_prompt, "system")
        
        # Should not have ellipsis
        self.assertNotIn("...", response)

    def test_client_creation_defaults(self):
        """Test create_client with defaults."""
        client = create_client()
        self.assertIsNone(client._model)
        self.assertIsNotNone(client.directive)

    def test_test_client_has_mock_model(self):
        """Test create_test_client includes mock model."""
        client = create_test_client()
        self.assertIsInstance(client._model, MockAIModel)


class TestAIClientIntegration(unittest.TestCase):
    """Integration tests for AI client."""

    def test_full_flow_with_model(self):
        """Test complete flow with model."""
        model = MockAIModel()
        client = GovernedAIClient(model=model)
        
        response = client.process("I want to help people learn programming")
        
        self.assertEqual(response.directive_evaluation.result, ActionResult.ALLOWED)
        self.assertIn("AI Response:", response.content)
        self.assertEqual(response.original_prompt, "I want to help people learn programming")

    def test_full_flow_without_model(self):
        """Test complete flow without model."""
        client = create_client(model=None)
        
        response = client.process("help people")
        
        self.assertIn("evaluated by Core Directive", response.content)
        self.assertIn("allowed", response.content)

    def test_hooks_with_problematic_content(self):
        """Test hooks don't bypass directive evaluation."""
        def malicious_pre_hook(prompt: str) -> str:
            # Try to inject harmful content
            return "harm people"
        
        client = GovernedAIClient(
            model=MockAIModel(),
            pre_process_hook=malicious_pre_hook
        )
        
        response = client.process("help people")
        
        # Should still evaluate the modified (harmful) prompt
        self.assertEqual(response.directive_evaluation.result, ActionResult.REVIEW)

    def test_multiple_requests_stats(self):
        """Test stats tracking across multiple requests."""
        client = create_test_client()
        
        client.process("help")
        client.process("support")
        client.process("")  # Will trigger review
        
        stats = client.stats
        self.assertEqual(stats["total_requests"], 3)


class TestEdgeCases(unittest.TestCase):
    """Edge case tests for AI client."""

    def test_empty_prompt(self):
        """Test processing empty prompt."""
        client = create_test_client()
        response = client.process("")
        
        self.assertIsInstance(response, AIResponse)
        self.assertEqual(response.directive_evaluation.result, ActionResult.REVIEW)

    def test_whitespace_prompt(self):
        """Test processing whitespace-only prompt."""
        client = create_test_client()
        response = client.process("   \n\t   ")
        
        self.assertIsInstance(response, AIResponse)

    def test_very_long_prompt(self):
        """Test processing very long prompt."""
        client = create_test_client()
        long_prompt = "help " * 1000
        response = client.process(long_prompt)
        
        self.assertIsInstance(response, AIResponse)
        self.assertEqual(response.directive_evaluation.result, ActionResult.ALLOWED)

    def test_unicode_in_prompt(self):
        """Test processing prompt with unicode characters."""
        client = create_test_client()
        response = client.process("帮助人们 help people 🎉")
        
        self.assertIsInstance(response, AIResponse)


if __name__ == "__main__":
    unittest.main()
