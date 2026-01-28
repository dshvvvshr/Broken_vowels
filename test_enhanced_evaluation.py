"""
Tests for Enhanced Evaluation Features

This module tests the new semantic evaluation, probabilistic reasoning,
and domain-specific evaluator capabilities added to the evaluation kernel.
"""

import unittest
from evaluator import (
    DirectiveEvaluator,
    DetailedEvaluation,
    SemanticContext,
    ProbabilisticAssessment,
    ActionResult,
    get_evaluator,
)


class TestSemanticEvaluation(unittest.TestCase):
    """Tests for semantic evaluation capabilities."""

    def setUp(self):
        """Set up test fixtures."""
        self.evaluator = DirectiveEvaluator()

    def test_semantic_context_creation(self):
        """Test that semantic context is created for evaluations."""
        result = self.evaluator.evaluate("I want to help people learn")
        self.assertIsNotNone(result.semantic_context)
        self.assertIsInstance(result.semantic_context, SemanticContext)

    def test_semantic_intent_type_help(self):
        """Test that helpful intents are classified correctly."""
        result = self.evaluator.evaluate("I want to help and support others")
        self.assertEqual(result.semantic_context.intent_type, "help")

    def test_semantic_intent_type_harm(self):
        """Test that harmful intents are classified correctly."""
        result = self.evaluator.evaluate("I want to harm someone")
        self.assertEqual(result.semantic_context.intent_type, "harm")

    def test_semantic_intent_type_ambiguous(self):
        """Test that ambiguous intents are classified correctly."""
        result = self.evaluator.evaluate("Maybe I might possibly do something unclear")
        self.assertEqual(result.semantic_context.intent_type, "ambiguous")

    def test_semantic_ambiguity_detection(self):
        """Test that ambiguity is detected in requests."""
        result = self.evaluator.evaluate("I'm not sure if I should perhaps maybe do this")
        # Contains 2 ambiguity indicators (perhaps, maybe) = 0.30
        self.assertGreaterEqual(result.semantic_context.ambiguity_score, 0.3)

    def test_semantic_sentiment_positive(self):
        """Test positive sentiment detection."""
        result = self.evaluator.evaluate("I want to help, support, and enable people")
        self.assertGreater(result.semantic_context.sentiment, 0.0)

    def test_semantic_sentiment_negative(self):
        """Test negative sentiment detection."""
        result = self.evaluator.evaluate("I want to harm, exploit, and manipulate")
        self.assertLess(result.semantic_context.sentiment, 0.0)

    def test_semantic_entity_extraction(self):
        """Test that entities are extracted from intent."""
        result = self.evaluator.evaluate('I want to help "John Smith" with his project')
        self.assertIn("John Smith", result.semantic_context.entities)

    def test_semantic_context_clues(self):
        """Test that context clues are captured."""
        context = {"educational": True, "urgent": True}
        result = self.evaluator.evaluate("Help with this task", context)
        self.assertTrue(any("Educational" in clue for clue in result.semantic_context.context_clues))


class TestProbabilisticReasoning(unittest.TestCase):
    """Tests for probabilistic reasoning capabilities."""

    def setUp(self):
        """Set up test fixtures."""
        self.evaluator = DirectiveEvaluator()

    def test_probabilistic_assessment_creation(self):
        """Test that probabilistic assessment is created."""
        result = self.evaluator.evaluate("I want to help people")
        self.assertIsNotNone(result.probabilistic_assessment)
        self.assertIsInstance(result.probabilistic_assessment, ProbabilisticAssessment)

    def test_harm_probability_high_for_harmful_intent(self):
        """Test that harm probability is high for harmful intents."""
        result = self.evaluator.evaluate("I want to harm and attack someone")
        self.assertGreater(result.probabilistic_assessment.harm_probability, 0.5)

    def test_benefit_probability_high_for_helpful_intent(self):
        """Test that benefit probability is high for helpful intents."""
        result = self.evaluator.evaluate("I want to help and support people")
        self.assertGreater(result.probabilistic_assessment.benefit_probability, 0.0)

    def test_uncertainty_high_for_ambiguous_intent(self):
        """Test that uncertainty is high for ambiguous intents."""
        result = self.evaluator.evaluate("Maybe I might possibly do something unclear")
        self.assertGreater(result.probabilistic_assessment.uncertainty, 0.5)

    def test_risk_level_critical_for_severe_harm(self):
        """Test that risk level is critical for severe harm indicators."""
        result = self.evaluator.evaluate("I want to harm and destroy and attack")
        self.assertIn(result.probabilistic_assessment.risk_level, ["critical", "high"])

    def test_risk_level_low_for_benign_intent(self):
        """Test that risk level is low for benign intents."""
        result = self.evaluator.evaluate("I want to learn about gardening")
        self.assertEqual(result.probabilistic_assessment.risk_level, "low")

    def test_expected_outcome_for_harmful_intent(self):
        """Test that expected outcome reflects harmful intent."""
        result = self.evaluator.evaluate("I want to exploit and manipulate people")
        self.assertIn("interfere", result.probabilistic_assessment.expected_outcome.lower())

    def test_expected_outcome_for_helpful_intent(self):
        """Test that expected outcome reflects helpful intent."""
        result = self.evaluator.evaluate("I want to help and empower people")
        self.assertIn("support", result.probabilistic_assessment.expected_outcome.lower())

    def test_probabilistic_affects_action_result(self):
        """Test that probabilistic assessment affects final decision."""
        result = self.evaluator.evaluate("I want to harm someone badly")
        # High harm probability should lead to BLOCKED or REVIEW
        self.assertIn(result.base_evaluation.result, [ActionResult.BLOCKED, ActionResult.REVIEW])


class TestEnhancedScoring(unittest.TestCase):
    """Tests for enhanced scoring with semantic and probabilistic factors."""

    def setUp(self):
        """Set up test fixtures."""
        self.evaluator = DirectiveEvaluator()

    def test_score_improved_by_semantic_sentiment(self):
        """Test that positive sentiment improves score."""
        result = self.evaluator.evaluate("I want to help, support, and enable people to grow")
        self.assertGreater(result.overall_score, 0.0)

    def test_score_penalized_by_high_uncertainty(self):
        """Test that high uncertainty leads to lower confidence."""
        result1 = self.evaluator.evaluate("I want to harm")
        result2 = self.evaluator.evaluate("I might maybe possibly want to harm")
        # Second one should have lower confidence due to uncertainty
        self.assertLess(result2.base_evaluation.confidence, result1.base_evaluation.confidence)

    def test_confidence_reduced_by_ambiguity(self):
        """Test that ambiguity reduces confidence."""
        result1 = self.evaluator.evaluate("I want to harm someone")
        result2 = self.evaluator.evaluate("Maybe I might possibly want to harm someone")
        self.assertLess(result2.base_evaluation.confidence, result1.base_evaluation.confidence)

    def test_confidence_reduced_by_uncertainty(self):
        """Test that probabilistic uncertainty reduces confidence."""
        result = self.evaluator.evaluate("Something ambiguous and unclear maybe")
        self.assertLess(result.base_evaluation.confidence, 0.8)


class TestDomainSpecificEvaluators(unittest.TestCase):
    """Tests for domain-specific evaluator registration and use."""

    def setUp(self):
        """Set up test fixtures."""
        self.evaluator = DirectiveEvaluator()

    def test_domain_evaluator_registration(self):
        """Test that domain evaluators can be registered."""
        def custom_evaluator(intent, context):
            from evaluator import DetailedEvaluation, DirectiveEvaluation, ActionResult
            return DetailedEvaluation(
                base_evaluation=DirectiveEvaluation(
                    result=ActionResult.ALLOWED,
                    reason="Custom domain evaluation",
                    confidence=0.9,
                ),
                impacts=[],
                conflicts=[],
                overall_score=0.8,
                recommendations=["Domain-specific recommendation"],
            )

        self.evaluator.register_domain_evaluator("test_domain", custom_evaluator)
        self.assertIn("test_domain", self.evaluator.get_domain_evaluators())

    def test_domain_evaluator_usage(self):
        """Test that registered domain evaluators are used."""
        def custom_evaluator(intent, context):
            from evaluator import DetailedEvaluation, DirectiveEvaluation, ActionResult
            return DetailedEvaluation(
                base_evaluation=DirectiveEvaluation(
                    result=ActionResult.ALLOWED,
                    reason="Custom domain evaluation executed",
                    confidence=0.9,
                ),
                impacts=[],
                conflicts=[],
                overall_score=0.8,
                recommendations=["Domain-specific recommendation"],
            )

        self.evaluator.register_domain_evaluator("neural_interface", custom_evaluator)
        
        result = self.evaluator.evaluate(
            "Test intent",
            context={"domain": "neural_interface"}
        )
        
        self.assertEqual(result.base_evaluation.reason, "Custom domain evaluation executed")

    def test_list_domain_evaluators(self):
        """Test that we can list registered domain evaluators."""
        self.evaluator.register_domain_evaluator("domain1", lambda i, c: None)
        self.evaluator.register_domain_evaluator("domain2", lambda i, c: None)
        
        domains = self.evaluator.get_domain_evaluators()
        self.assertIn("domain1", domains)
        self.assertIn("domain2", domains)


class TestEnhancedRecommendations(unittest.TestCase):
    """Tests for enhanced recommendations with semantic context."""

    def setUp(self):
        """Set up test fixtures."""
        self.evaluator = DirectiveEvaluator()

    def test_recommendations_for_ambiguous_intent(self):
        """Test that ambiguous intents get clarification recommendations."""
        result = self.evaluator.evaluate("Maybe I might do something unclear")
        recommendations = " ".join(result.recommendations).lower()
        self.assertTrue(
            any(keyword in recommendations for keyword in ["specific", "explicit", "ambiguous", "clarify"])
        )

    def test_recommendations_include_alternatives(self):
        """Test that blocked intents get alternative suggestions."""
        result = self.evaluator.evaluate("I want to harm someone")
        self.assertGreater(len(result.recommendations), 0)

    def test_reason_includes_ambiguity_warning(self):
        """Test that high ambiguity is mentioned in reason."""
        result = self.evaluator.evaluate("Maybe possibly unclear might could should")
        self.assertIn("ambiguity", result.base_evaluation.reason.lower())


class TestRegressionPrevention(unittest.TestCase):
    """Tests to ensure existing functionality still works."""

    def setUp(self):
        """Set up test fixtures."""
        self.evaluator = DirectiveEvaluator()

    def test_basic_evaluation_still_works(self):
        """Test that basic evaluation functionality is preserved."""
        result = self.evaluator.evaluate("I want to help people")
        self.assertIsInstance(result, DetailedEvaluation)
        self.assertEqual(result.base_evaluation.result, ActionResult.ALLOWED)

    def test_harm_detection_still_works(self):
        """Test that harm detection is still functional."""
        result = self.evaluator.evaluate("I want to harm someone")
        self.assertIn(result.base_evaluation.result, [ActionResult.BLOCKED, ActionResult.REVIEW])

    def test_empty_evaluation_still_works(self):
        """Test that empty input handling is preserved."""
        result = self.evaluator.evaluate("")
        self.assertEqual(result.base_evaluation.result, ActionResult.REVIEW)

    def test_evaluation_count_tracking_still_works(self):
        """Test that evaluation count tracking is preserved."""
        initial_count = self.evaluator.evaluation_count
        self.evaluator.evaluate("Test")
        self.assertEqual(self.evaluator.evaluation_count, initial_count + 1)


if __name__ == "__main__":
    unittest.main()
