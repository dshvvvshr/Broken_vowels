"""
Tests for the Core Directive Governance Layer

This module provides tests for all components of the governance system:
- core_directive.py - The Core Directive module
- ai_client.py - AI client with governance integration
- gateway.py - Gateway for request interception
- evaluator.py - Detailed evaluation engine
"""

import unittest
from datetime import datetime, timezone

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
    GovernanceGateway,
    GatewayRequest,
    create_gateway,
    content_filter_middleware,
    rate_limit_middleware,
)
from evaluator import (
    ConflictType,
    DetailedEvaluation,
    DirectiveEvaluator,
    ImpactCategory,
    evaluate_detailed,
    get_evaluator,
)


class TestCoreDirective(unittest.TestCase):
    """Tests for the CoreDirective class."""

    def setUp(self):
        """Set up test fixtures."""
        self.directive = CoreDirective()

    def test_directive_text(self):
        """Test that the directive text is correct."""
        expected = (
            "Every person has an equal, inalienable right to pursue happiness."
        )
        self.assertEqual(self.directive.directive, expected)

    def test_principles_exist(self):
        """Test that principles are defined."""
        self.assertGreater(len(self.directive.principles), 0)
        self.assertIn("Protect autonomy", self.directive.principles[0])

    def test_system_message_generation(self):
        """Test system message generation."""
        message = self.directive.get_system_message()
        self.assertIn("inalienable right to the pursuit of happiness", message)
        self.assertIn("custodian of humanity", message)

    def test_evaluate_empty_intent(self):
        """Test evaluation of empty intent."""
        result = self.directive.evaluate_intent("")
        self.assertEqual(result.result, ActionResult.REVIEW)

    def test_evaluate_positive_intent(self):
        """Test evaluation of positive intent."""
        result = self.directive.evaluate_intent("I want to help people learn")
        self.assertEqual(result.result, ActionResult.ALLOWED)

    def test_evaluate_harmful_intent(self):
        """Test evaluation of potentially harmful intent."""
        result = self.directive.evaluate_intent("I want to harm someone")
        self.assertEqual(result.result, ActionResult.REVIEW)
        self.assertIsNotNone(result.alternative)

    def test_is_allowed_positive(self):
        """Test is_allowed for positive intent."""
        self.assertTrue(self.directive.is_allowed("help others"))

    def test_is_allowed_harmful(self):
        """Test is_allowed for harmful intent."""
        self.assertFalse(self.directive.is_allowed("harm others"))


class TestModuleFunctions(unittest.TestCase):
    """Tests for module-level convenience functions."""

    def test_get_directive_singleton(self):
        """Test that get_directive returns a singleton."""
        d1 = get_directive()
        d2 = get_directive()
        self.assertIs(d1, d2)

    def test_evaluate_function(self):
        """Test the evaluate convenience function."""
        result = evaluate("help people")
        self.assertIsInstance(result, DirectiveEvaluation)

    def test_is_allowed_function(self):
        """Test the is_allowed convenience function."""
        self.assertTrue(is_allowed("support others"))


class TestGovernedAIClient(unittest.TestCase):
    """Tests for the GovernedAIClient class."""

    def setUp(self):
        """Set up test fixtures."""
        self.client = create_test_client()

    def test_client_creation(self):
        """Test client creation."""
        client = create_client()
        self.assertIsNotNone(client)

    def test_test_client_has_model(self):
        """Test that test client has mock model."""
        self.assertIsNotNone(self.client._model)

    def test_system_message(self):
        """Test system message retrieval."""
        message = self.client.get_system_message()
        self.assertIn("inalienable right to the pursuit of happiness", message)

    def test_process_allowed_request(self):
        """Test processing an allowed request."""
        response = self.client.process("Help me learn programming")
        self.assertIsInstance(response, AIResponse)
        self.assertEqual(
            response.directive_evaluation.result,
            ActionResult.ALLOWED,
        )

    def test_process_review_request(self):
        """Test processing a request requiring review."""
        response = self.client.process("Tell me how to harm")
        self.assertEqual(
            response.directive_evaluation.result,
            ActionResult.REVIEW,
        )

    def test_stats_tracking(self):
        """Test that stats are tracked."""
        initial_stats = self.client.stats
        self.client.process("Test request")
        new_stats = self.client.stats
        self.assertEqual(
            new_stats["total_requests"],
            initial_stats["total_requests"] + 1,
        )


class TestMockAIModel(unittest.TestCase):
    """Tests for the MockAIModel class."""

    def test_mock_model_response(self):
        """Test mock model generates response."""
        model = MockAIModel()
        response = model.generate("Test prompt", "System message")
        self.assertIn("AI Response:", response)


class TestGovernanceGateway(unittest.TestCase):
    """Tests for the GovernanceGateway class."""

    def setUp(self):
        """Set up test fixtures."""
        self.gateway = create_gateway()

    def test_gateway_creation(self):
        """Test gateway creation."""
        gateway = create_gateway(enable_audit=False)
        self.assertIsNotNone(gateway)

    def test_process_allowed_request(self):
        """Test processing an allowed request."""
        request = GatewayRequest.create("Help me learn", source="test")
        response = self.gateway.process(request)
        self.assertTrue(response.processed)

    def test_process_review_request(self):
        """Test processing a request requiring review."""
        request = GatewayRequest.create("I want to harm", source="test")
        response = self.gateway.process(request)
        self.assertEqual(
            response.evaluation.result,
            ActionResult.REVIEW,
        )

    def test_audit_logging(self):
        """Test that audit log is populated."""
        request = GatewayRequest.create("Test request", source="test")
        self.gateway.process(request)
        self.assertGreater(len(self.gateway.audit_log), 0)

    def test_export_audit_log(self):
        """Test audit log export."""
        request = GatewayRequest.create("Test", source="test")
        self.gateway.process(request)
        export = self.gateway.export_audit_log()
        self.assertIn("request_id", export)

    def test_middleware_addition(self):
        """Test adding middleware."""
        middleware = content_filter_middleware(["blocked"])
        self.gateway.add_middleware(middleware)
        self.assertEqual(len(self.gateway._middleware), 1)

    def test_middleware_blocking(self):
        """Test middleware can block requests."""
        middleware = content_filter_middleware(["forbidden"])
        self.gateway.add_middleware(middleware)
        request = GatewayRequest.create("This is forbidden", source="test")
        response = self.gateway.process(request)
        self.assertFalse(response.processed)

    def test_stats_tracking(self):
        """Test stats tracking."""
        request = GatewayRequest.create("Test", source="test")
        self.gateway.process(request)
        stats = self.gateway.stats
        self.assertEqual(stats["total_requests"], 1)


class TestGatewayRequest(unittest.TestCase):
    """Tests for the GatewayRequest class."""

    def test_request_creation(self):
        """Test request creation with factory method."""
        request = GatewayRequest.create("Test content", source="unit_test")
        self.assertEqual(request.content, "Test content")
        self.assertEqual(request.source, "unit_test")
        self.assertIsNotNone(request.id)
        self.assertIsInstance(request.timestamp, datetime)


class TestDirectiveEvaluator(unittest.TestCase):
    """Tests for the DirectiveEvaluator class."""

    def setUp(self):
        """Set up test fixtures."""
        self.evaluator = DirectiveEvaluator()

    def test_evaluator_creation(self):
        """Test evaluator creation."""
        evaluator = DirectiveEvaluator()
        self.assertEqual(evaluator.evaluation_count, 0)

    def test_evaluate_positive_intent(self):
        """Test evaluation of positive intent."""
        result = self.evaluator.evaluate("I want to help people")
        self.assertIsInstance(result, DetailedEvaluation)
        self.assertGreaterEqual(result.overall_score, 0)

    def test_evaluate_harmful_intent(self):
        """Test evaluation of harmful intent."""
        result = self.evaluator.evaluate("I want to harm someone")
        self.assertLess(result.overall_score, 0)
        self.assertTrue(any(
            c.conflict_type == ConflictType.DIRECT_HARM
            for c in result.conflicts
        ))

    def test_evaluate_coercion(self):
        """Test evaluation of coercion intent."""
        result = self.evaluator.evaluate("I want to force them")
        self.assertTrue(any(
            c.conflict_type == ConflictType.COERCION
            for c in result.conflicts
        ))

    def test_evaluate_deception(self):
        """Test evaluation of deception intent."""
        result = self.evaluator.evaluate("I want to deceive people")
        self.assertTrue(any(
            c.conflict_type == ConflictType.DECEPTION
            for c in result.conflicts
        ))

    def test_evaluate_empty_intent(self):
        """Test evaluation of empty intent."""
        result = self.evaluator.evaluate("")
        self.assertEqual(
            result.base_evaluation.result,
            ActionResult.REVIEW,
        )

    def test_recommendations_generated(self):
        """Test that recommendations are generated."""
        result = self.evaluator.evaluate("I want to exploit someone")
        self.assertGreater(len(result.recommendations), 0)

    def test_evaluation_count_tracking(self):
        """Test that evaluation count is tracked."""
        self.evaluator.evaluate("Test 1")
        self.evaluator.evaluate("Test 2")
        self.assertEqual(self.evaluator.evaluation_count, 2)


class TestEvaluatorModuleFunctions(unittest.TestCase):
    """Tests for evaluator module-level functions."""

    def test_get_evaluator_singleton(self):
        """Test that get_evaluator returns a singleton."""
        e1 = get_evaluator()
        e2 = get_evaluator()
        self.assertIs(e1, e2)

    def test_evaluate_detailed_function(self):
        """Test the evaluate_detailed convenience function."""
        result = evaluate_detailed("help people learn")
        self.assertIsInstance(result, DetailedEvaluation)


class TestMiddleware(unittest.TestCase):
    """Tests for middleware functions."""

    def test_rate_limit_middleware(self):
        """Test rate limiting middleware."""
        middleware = rate_limit_middleware(max_requests=2)
        req1 = GatewayRequest.create("Test 1", source="user1")
        req2 = GatewayRequest.create("Test 2", source="user1")
        req3 = GatewayRequest.create("Test 3", source="user1")

        self.assertIsNotNone(middleware(req1))
        self.assertIsNotNone(middleware(req2))
        self.assertIsNone(middleware(req3))  # Should be blocked

    def test_content_filter_middleware(self):
        """Test content filtering middleware."""
        middleware = content_filter_middleware(["spam", "banned"])
        
        allowed = GatewayRequest.create("Normal content", source="test")
        blocked = GatewayRequest.create("This is spam", source="test")

        self.assertIsNotNone(middleware(allowed))
        self.assertIsNone(middleware(blocked))


if __name__ == "__main__":
    unittest.main()
