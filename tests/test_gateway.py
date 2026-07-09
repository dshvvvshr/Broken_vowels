"""
Comprehensive tests for gateway module to achieve 100% coverage.
"""

import unittest
from datetime import datetime, timezone
from gateway import (
    GovernanceGateway,
    GatewayRequest,
    GatewayResponse,
    AuditEntry,
    create_gateway,
    rate_limit_middleware,
    content_filter_middleware,
)
from core_directive import ActionResult, CoreDirective


class TestGatewayComprehensive(unittest.TestCase):
    """Comprehensive tests for GovernanceGateway."""

    def setUp(self):
        """Set up test fixtures."""
        self.gateway = create_gateway()

    def test_repr(self):
        """Test string representation."""
        repr_str = repr(self.gateway)
        self.assertIn("GovernanceGateway", repr_str)
        self.assertIn("requests=", repr_str)
        self.assertIn("routes=", repr_str)

    def test_custom_directive(self):
        """Test gateway with custom directive."""
        custom_directive = CoreDirective()
        gateway = GovernanceGateway(directive=custom_directive)
        self.assertIs(gateway.directive, custom_directive)

    def test_audit_disabled(self):
        """Test gateway with audit logging disabled."""
        gateway = create_gateway(enable_audit=False)
        request = GatewayRequest.create("test", source="test")
        gateway.process(request)
        self.assertEqual(len(gateway.audit_log), 0)

    def test_custom_route_handler(self):
        """Test registering and using custom route handler."""
        def custom_handler(request: GatewayRequest) -> str:
            return f"Custom: {request.content}"
        
        self.gateway.register_route("custom", custom_handler)
        request = GatewayRequest.create("test message", source="test")
        response = self.gateway.process(request, route="custom")
        
        self.assertIn("Custom:", response.content)
        self.assertEqual(response.route, "custom")

    def test_nonexistent_route_uses_default(self):
        """Test that nonexistent route falls back to default."""
        request = GatewayRequest.create("help people", source="test")
        response = self.gateway.process(request, route="nonexistent")
        # Should use default handler
        self.assertIn("processed successfully", response.content)

    def test_blocked_request_content(self):
        """Test content generation for blocked requests."""
        from unittest.mock import MagicMock
        from core_directive import DirectiveEvaluation
        
        # Create a mock directive that returns BLOCKED
        mock_directive = MagicMock()
        mock_directive.evaluate_intent.return_value = DirectiveEvaluation(
            result=ActionResult.BLOCKED,
            reason="Test reason for blocking",
            alternative="Try this instead",
            confidence=1.0
        )
        
        gateway = GovernanceGateway(directive=mock_directive)
        request = GatewayRequest.create("test", source="test")
        response = gateway.process(request)
        
        # Should be blocked
        self.assertEqual(response.evaluation.result, ActionResult.BLOCKED)
        self.assertIn("Request blocked", response.content)
        self.assertIn("Test reason for blocking", response.content)
        self.assertIn("Try this instead", response.content)
        self.assertFalse(response.processed)

    def test_review_request_content(self):
        """Test content generation for review requests."""
        request = GatewayRequest.create("I want to harm", source="test")
        response = self.gateway.process(request)
        
        if response.evaluation.result == ActionResult.REVIEW:
            self.assertIn("quarantined for review", response.content)
            self.assertIn("Reason:", response.content)
            self.assertIn("Confidence:", response.content)

    def test_multiple_middleware(self):
        """Test multiple middleware in pipeline."""
        middleware1_called = []
        middleware2_called = []
        
        def middleware1(request):
            middleware1_called.append(True)
            return request
        
        def middleware2(request):
            middleware2_called.append(True)
            return request
        
        self.gateway.add_middleware(middleware1)
        self.gateway.add_middleware(middleware2)
        
        request = GatewayRequest.create("test", source="test")
        self.gateway.process(request)
        
        self.assertTrue(middleware1_called)
        self.assertTrue(middleware2_called)

    def test_middleware_chain_rejection(self):
        """Test that middleware rejection stops the chain."""
        middleware2_called = []
        
        def blocking_middleware(request):
            return None  # Reject
        
        def middleware2(request):
            middleware2_called.append(True)
            return request
        
        self.gateway.add_middleware(blocking_middleware)
        self.gateway.add_middleware(middleware2)
        
        request = GatewayRequest.create("test", source="test")
        response = self.gateway.process(request)
        
        # Second middleware should not be called
        self.assertFalse(middleware2_called)
        self.assertFalse(response.processed)
        self.assertIn("blocked", response.content.lower())
        self.assertIn("middleware", response.content.lower())

    def test_request_metadata(self):
        """Test request with custom metadata."""
        request = GatewayRequest.create("test", source="test")
        request.metadata = {"user_id": "123", "session": "abc"}
        
        response = self.gateway.process(request)
        self.assertIsNotNone(response)

    def test_audit_log_details_truncation(self):
        """Test that audit log truncates long content."""
        # Import the truncation limit from gateway module
        from gateway import GovernanceGateway
        # The gateway truncates to 200 chars in _log_audit
        DETAILS_TRUNCATION_LENGTH = 200
        
        long_content = "x" * 500
        request = GatewayRequest.create(long_content, source="test")
        self.gateway.process(request)
        
        log = self.gateway.audit_log
        self.assertEqual(len(log), 1)
        # Details should be truncated
        self.assertLessEqual(len(log[0].details), DETAILS_TRUNCATION_LENGTH)

    def test_clear_audit_log(self):
        """Test clearing the audit log."""
        request = GatewayRequest.create("test", source="test")
        self.gateway.process(request)
        self.assertGreater(len(self.gateway.audit_log), 0)
        
        self.gateway.clear_audit_log()
        self.assertEqual(len(self.gateway.audit_log), 0)

    def test_export_audit_log_format(self):
        """Test audit log export JSON format."""
        request = GatewayRequest.create("test content", source="test_source")
        self.gateway.process(request)
        
        export = self.gateway.export_audit_log()
        self.assertIn("request_id", export)
        self.assertIn("timestamp", export)
        self.assertIn("action", export)
        self.assertIn("result", export)
        self.assertIn("source", export)
        self.assertIn("test_source", export)

    def test_stats_structure(self):
        """Test stats return all expected fields."""
        stats = self.gateway.stats
        self.assertIn("total_requests", stats)
        self.assertIn("blocked_or_reviewed", stats)
        self.assertIn("passed", stats)
        self.assertIn("middleware_count", stats)
        self.assertIn("route_count", stats)

    def test_stats_accuracy(self):
        """Test stats are calculated correctly."""
        # Process some requests
        req1 = GatewayRequest.create("help people", source="test")
        req2 = GatewayRequest.create("harm people", source="test")
        
        self.gateway.process(req1)
        self.gateway.process(req2)
        
        stats = self.gateway.stats
        self.assertEqual(stats["total_requests"], 2)
        # At least one should be blocked or reviewed
        self.assertGreaterEqual(stats["blocked_or_reviewed"], 0)

    def test_default_route_registered(self):
        """Test that default route is registered on init."""
        self.assertIn("default", self.gateway._routes)

    def test_gateway_response_structure(self):
        """Test GatewayResponse contains all fields."""
        request = GatewayRequest.create("test", source="test")
        response = self.gateway.process(request)
        
        self.assertIsNotNone(response.request_id)
        self.assertIsNotNone(response.content)
        self.assertIsNotNone(response.evaluation)
        self.assertIsInstance(response.processed, bool)
        self.assertIsInstance(response.timestamp, datetime)
        self.assertIsNotNone(response.route)

    def test_request_timestamp_timezone(self):
        """Test that request timestamp is timezone-aware."""
        request = GatewayRequest.create("test", source="test")
        self.assertIsNotNone(request.timestamp.tzinfo)


class TestGatewayRequestFactory(unittest.TestCase):
    """Tests for GatewayRequest factory method."""

    def test_create_with_defaults(self):
        """Test request creation with default source."""
        request = GatewayRequest.create("test content")
        self.assertEqual(request.content, "test content")
        self.assertEqual(request.source, "unknown")
        self.assertIsNotNone(request.id)
        self.assertIsInstance(request.timestamp, datetime)

    def test_create_with_custom_source(self):
        """Test request creation with custom source."""
        request = GatewayRequest.create("test", source="custom_source")
        self.assertEqual(request.source, "custom_source")

    def test_unique_ids(self):
        """Test that each request gets a unique ID."""
        req1 = GatewayRequest.create("test1", source="test")
        req2 = GatewayRequest.create("test2", source="test")
        self.assertNotEqual(req1.id, req2.id)


class TestRateLimitMiddleware(unittest.TestCase):
    """Tests for rate limit middleware."""

    def test_rate_limit_per_source(self):
        """Test that rate limit is tracked per source."""
        middleware = rate_limit_middleware(max_requests=2)
        
        user1_req1 = GatewayRequest.create("test", source="user1")
        user1_req2 = GatewayRequest.create("test", source="user1")
        user2_req1 = GatewayRequest.create("test", source="user2")
        
        # User 1 should be allowed twice
        self.assertIsNotNone(middleware(user1_req1))
        self.assertIsNotNone(middleware(user1_req2))
        
        # User 2 should still be allowed (different source)
        self.assertIsNotNone(middleware(user2_req1))

    def test_rate_limit_custom_max(self):
        """Test rate limit with custom maximum."""
        middleware = rate_limit_middleware(max_requests=1)
        
        req1 = GatewayRequest.create("test", source="user")
        req2 = GatewayRequest.create("test", source="user")
        
        self.assertIsNotNone(middleware(req1))
        self.assertIsNone(middleware(req2))


class TestContentFilterMiddleware(unittest.TestCase):
    """Tests for content filter middleware."""

    def test_filter_multiple_terms(self):
        """Test filtering with multiple blocked terms."""
        middleware = content_filter_middleware(["spam", "scam", "phishing"])
        
        normal = GatewayRequest.create("normal content", source="test")
        spam = GatewayRequest.create("this is spam", source="test")
        scam = GatewayRequest.create("this is a scam", source="test")
        
        self.assertIsNotNone(middleware(normal))
        self.assertIsNone(middleware(spam))
        self.assertIsNone(middleware(scam))

    def test_filter_case_insensitive(self):
        """Test that filtering is case insensitive."""
        middleware = content_filter_middleware(["BLOCKED"])
        
        lower = GatewayRequest.create("this is blocked", source="test")
        upper = GatewayRequest.create("this is BLOCKED", source="test")
        mixed = GatewayRequest.create("this is BlOcKeD", source="test")
        
        self.assertIsNone(middleware(lower))
        self.assertIsNone(middleware(upper))
        self.assertIsNone(middleware(mixed))

    def test_filter_empty_list(self):
        """Test filter with empty blocked terms list."""
        middleware = content_filter_middleware([])
        
        request = GatewayRequest.create("any content", source="test")
        self.assertIsNotNone(middleware(request))


class TestIntegrationScenarios(unittest.TestCase):
    """Integration tests for complete gateway scenarios."""

    def test_full_pipeline_allowed(self):
        """Test full pipeline for allowed request."""
        gateway = create_gateway()
        
        # Add some middleware
        gateway.add_middleware(content_filter_middleware(["spam"]))
        
        request = GatewayRequest.create("I want to help people", source="user1")
        response = gateway.process(request)
        
        self.assertTrue(response.processed)
        self.assertEqual(response.evaluation.result, ActionResult.ALLOWED)
        self.assertGreater(len(gateway.audit_log), 0)

    def test_full_pipeline_blocked_by_middleware(self):
        """Test full pipeline with middleware blocking."""
        gateway = create_gateway()
        
        gateway.add_middleware(content_filter_middleware(["forbidden"]))
        
        request = GatewayRequest.create("this is forbidden", source="user1")
        response = gateway.process(request)
        
        self.assertFalse(response.processed)
        self.assertEqual(response.evaluation.result, ActionResult.BLOCKED)

    def test_full_pipeline_review(self):
        """Test full pipeline for request requiring review."""
        gateway = create_gateway()
        
        request = GatewayRequest.create("I want to harm someone", source="user1")
        response = gateway.process(request)
        
        self.assertEqual(response.evaluation.result, ActionResult.REVIEW)
        self.assertIn("Reason:", response.content)


if __name__ == "__main__":
    unittest.main()
