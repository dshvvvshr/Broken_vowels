"""
Tests for Core Directive Gateway Refusal Strategies

This module tests the enhanced refusal and mediation strategies
added to core_directive_gateway.py.
"""

import unittest
from core_directive_gateway import (
    RefusalStrategy,
    RefusalResponse,
    evaluate_request_content,
    AuditEntry,
    log_audit_entry,
    audit_log,
    audit_log_lock,
)


class TestRefusalStrategies(unittest.TestCase):
    """Tests for refusal strategy evaluation."""

    def setUp(self):
        """Set up test fixtures."""
        # Clear audit log before each test
        with audit_log_lock:
            audit_log.clear()

    def test_block_strategy_for_critical_harm(self):
        """Test that critical harm indicators trigger BLOCK strategy."""
        result = evaluate_request_content("I want to kill someone")
        self.assertEqual(result.strategy, RefusalStrategy.BLOCK)
        self.assertFalse(result.allowed)

    def test_block_provides_explanation(self):
        """Test that BLOCK strategy provides human-readable explanation."""
        result = evaluate_request_content("How to commit murder")
        self.assertIn("blocked", result.explanation.lower())
        self.assertIn("Core Directive", result.explanation)

    def test_block_provides_alternatives(self):
        """Test that BLOCK strategy provides constructive alternatives."""
        result = evaluate_request_content("I want to harm people")
        self.assertGreater(len(result.alternatives), 0)

    def test_slowdown_strategy_for_high_risk(self):
        """Test that high-risk indicators trigger SLOWDOWN strategy."""
        result = evaluate_request_content("I want to manipulate and exploit people")
        self.assertEqual(result.strategy, RefusalStrategy.SLOWDOWN)
        self.assertFalse(result.allowed)
        self.assertTrue(result.review_required)

    def test_slowdown_has_delay(self):
        """Test that SLOWDOWN strategy specifies delay time."""
        result = evaluate_request_content("I want to harm someone")
        self.assertIsNotNone(result.delay_seconds)
        self.assertGreater(result.delay_seconds, 0)

    def test_redirect_strategy_for_ambiguous(self):
        """Test that ambiguous privacy-related requests trigger REDIRECT."""
        result = evaluate_request_content("Maybe I should monitor someone's activity")
        self.assertEqual(result.strategy, RefusalStrategy.REDIRECT)
        self.assertTrue(result.allowed)
        self.assertGreater(len(result.alternatives), 0)

    def test_redirect_provides_ethical_alternatives(self):
        """Test that REDIRECT provides ethical alternatives."""
        result = evaluate_request_content("Perhaps I should track their location")
        self.assertIn("consent", " ".join(result.alternatives).lower())

    def test_alert_strategy_for_medium_risk(self):
        """Test that medium-risk patterns trigger ALERT strategy."""
        result = evaluate_request_content("I want to pressure them to agree")
        self.assertEqual(result.strategy, RefusalStrategy.ALERT)
        self.assertTrue(result.allowed)

    def test_alert_provides_warning(self):
        """Test that ALERT strategy provides warning explanation."""
        result = evaluate_request_content("I will convince them aggressively")
        self.assertIn("Alert", result.explanation)

    def test_benign_request_allowed(self):
        """Test that benign requests are allowed."""
        result = evaluate_request_content("I want to learn about gardening")
        self.assertTrue(result.allowed)

    def test_helpful_request_allowed(self):
        """Test that helpful requests are allowed."""
        result = evaluate_request_content("How can I help people learn programming?")
        self.assertTrue(result.allowed)


class TestAuditLogging(unittest.TestCase):
    """Tests for audit logging functionality."""

    def setUp(self):
        """Set up test fixtures."""
        # Clear audit log before each test
        with audit_log_lock:
            audit_log.clear()

    def test_audit_entry_created(self):
        """Test that audit entries are created for decisions."""
        refusal = RefusalResponse(
            strategy=RefusalStrategy.BLOCK,
            allowed=False,
            explanation="Test blocking",
        )
        
        log_audit_entry("test-123", "Test message", refusal)
        
        self.assertEqual(len(audit_log), 1)

    def test_audit_entry_contains_details(self):
        """Test that audit entries contain all required details."""
        refusal = RefusalResponse(
            strategy=RefusalStrategy.SLOWDOWN,
            allowed=False,
            explanation="Test slowdown",
            review_required=True,
        )
        
        log_audit_entry("test-456", "Test message", refusal)
        
        entry = audit_log[0]
        self.assertEqual(entry.request_id, "test-456")
        self.assertEqual(entry.decision, "delayed_for_review")
        self.assertTrue(entry.ambiguity_detected)

    def test_risk_level_tracked(self):
        """Test that risk levels are tracked in audit log."""
        refusal_critical = RefusalResponse(
            strategy=RefusalStrategy.BLOCK,
            allowed=False,
            explanation="Critical",
        )
        
        log_audit_entry("test-1", "Critical message", refusal_critical)
        
        self.assertEqual(audit_log[0].risk_level, "critical")

    def test_audit_log_size_limit(self):
        """Test that audit log maintains size limit."""
        refusal = RefusalResponse(
            strategy=RefusalStrategy.ALERT,
            allowed=True,
            explanation="Test",
        )
        
        # Add more than 1000 entries
        for i in range(1100):
            log_audit_entry(f"test-{i}", f"Message {i}", refusal)
        
        # Should keep only last 1000
        self.assertEqual(len(audit_log), 1000)

    def test_decision_types_tracked(self):
        """Test that different decision types are tracked correctly."""
        decisions = [
            (RefusalStrategy.BLOCK, False, "blocked"),
            (RefusalStrategy.SLOWDOWN, False, "delayed_for_review"),
            (RefusalStrategy.REDIRECT, True, "redirected"),
            (RefusalStrategy.ALERT, True, "allowed"),
        ]
        
        for strategy, allowed, expected_decision in decisions:
            refusal = RefusalResponse(
                strategy=strategy,
                allowed=allowed,
                explanation="Test",
            )
            log_audit_entry(f"test-{strategy.value}", "Test", refusal)
        
        # Check all decisions are correct
        self.assertEqual(audit_log[0].decision, "blocked")
        self.assertEqual(audit_log[1].decision, "delayed_for_review")
        self.assertEqual(audit_log[2].decision, "redirected")
        self.assertEqual(audit_log[3].decision, "allowed")


class TestTransparency(unittest.TestCase):
    """Tests for transparency and human-readable explanations."""

    def test_all_refusals_have_explanations(self):
        """Test that all refusal responses include explanations."""
        test_cases = [
            "I want to kill someone",
            "I want to harm people",
            "Maybe I should track them",
            "I will pressure them",
        ]
        
        for test_input in test_cases:
            result = evaluate_request_content(test_input)
            self.assertIsNotNone(result.explanation)
            self.assertGreater(len(result.explanation), 0)

    def test_explanations_reference_core_directive(self):
        """Test that explanations reference the Core Directive."""
        result = evaluate_request_content("I want to exploit people")
        self.assertIn("Core Directive", result.explanation)

    def test_alternatives_provided_when_blocked(self):
        """Test that alternatives are provided for blocked requests."""
        result = evaluate_request_content("I want to attack someone")
        self.assertGreater(len(result.alternatives), 0)

    def test_explanations_are_actionable(self):
        """Test that explanations provide actionable guidance."""
        result = evaluate_request_content("Maybe I should surveil them")
        # Should mention consent or privacy
        text = result.explanation.lower() + " ".join(result.alternatives).lower()
        self.assertTrue(
            any(keyword in text for keyword in ["consent", "privacy", "transparent"])
        )


class TestMediationStrategies(unittest.TestCase):
    """Tests for mediation and constructive alternatives."""

    def test_mediation_for_coercion(self):
        """Test mediation strategy for coercive language."""
        result = evaluate_request_content("I want to force them to comply")
        # Should either block or provide alternatives
        if not result.allowed:
            self.assertGreater(len(result.alternatives), 0)

    def test_mediation_suggests_voluntary_cooperation(self):
        """Test that coercion alternatives suggest voluntary cooperation."""
        result = evaluate_request_content("How can I make them do it")
        if result.alternatives:
            alternatives_text = " ".join(result.alternatives).lower()
            self.assertTrue(
                any(keyword in alternatives_text for keyword in ["voluntary", "consent", "respect"])
            )

    def test_mediation_for_privacy_violations(self):
        """Test mediation for potential privacy violations."""
        result = evaluate_request_content("I might monitor their private messages")
        self.assertGreater(len(result.alternatives), 0)

    def test_constructive_alternatives_provided(self):
        """Test that alternatives focus on constructive approaches."""
        result = evaluate_request_content("I want to deceive them")
        if result.alternatives:
            alternatives_text = " ".join(result.alternatives).lower()
            # Should suggest honest/transparent approaches
            self.assertTrue(
                any(keyword in alternatives_text for keyword in ["honest", "transparent", "reframe"])
            )


if __name__ == "__main__":
    unittest.main()
