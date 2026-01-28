"""
Domain-Specific Evaluator Template

This template provides a framework for creating domain-specific evaluators
that integrate with the Core Directive evaluation kernel. Each peripheral
layer can implement its own evaluator following this pattern.

Example domains:
- Neural interfaces and brain-computer interfaces
- RF sensing and surveillance technologies
- Cognitive rights and mental privacy
- Biotechnology and human enhancement
- Social media and digital platforms

Usage:
1. Copy this template to your peripheral layer directory
2. Rename the class to match your domain (e.g., NeuralInterfaceEvaluator)
3. Implement the domain-specific evaluation logic
4. Register with the DirectiveEvaluator using register_domain_evaluator()
"""

from dataclasses import dataclass
from typing import Optional, Dict, List
import sys
import os

# Add parent directory to path to import core modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from evaluator import (
    DetailedEvaluation,
    DirectiveEvaluation,
    ImpactAssessment,
    ConflictAssessment,
    SemanticContext,
    ProbabilisticAssessment,
    ImpactCategory,
    ConflictType,
    ActionResult,
)


@dataclass
class DomainSpecificContext:
    """
    Domain-specific context information.
    
    Extend this with fields specific to your domain.
    """
    domain_name: str
    technology_type: str
    risk_factors: List[str]
    special_considerations: List[str]


class DomainEvaluatorTemplate:
    """
    Template for domain-specific evaluators.
    
    This class demonstrates how to create a specialized evaluator
    for a specific peripheral layer that integrates with the core
    evaluation kernel.
    """

    # Domain-specific harm indicators
    DOMAIN_HARM_INDICATORS = {
        "example_category": [
            "domain_specific_keyword_1",
            "domain_specific_keyword_2",
        ],
    }

    # Domain-specific positive indicators
    DOMAIN_POSITIVE_INDICATORS = {
        "example_category": [
            "beneficial_keyword_1",
            "beneficial_keyword_2",
        ],
    }

    def __init__(self, domain_name: str = "template_domain"):
        """Initialize the domain evaluator."""
        self.domain_name = domain_name
        self.evaluation_count = 0

    def evaluate(
        self,
        intent: str,
        context: Optional[Dict] = None,
    ) -> DetailedEvaluation:
        """
        Perform domain-specific evaluation.

        Args:
            intent: The stated intent or action to evaluate
            context: Domain-specific context information

        Returns:
            DetailedEvaluation with domain-specific analysis
        """
        self.evaluation_count += 1
        context = context or {}

        # Extract domain context
        domain_context = self._extract_domain_context(intent, context)

        # Perform domain-specific impact assessment
        impacts = self._assess_domain_impacts(intent.lower(), domain_context)

        # Detect domain-specific conflicts
        conflicts = self._detect_domain_conflicts(intent.lower(), domain_context)

        # Perform semantic analysis
        semantic = self._analyze_domain_semantics(intent, domain_context)

        # Probabilistic assessment
        probabilistic = self._assess_domain_probabilities(
            intent, impacts, conflicts, semantic
        )

        # Calculate overall score
        overall_score = self._calculate_domain_score(
            impacts, conflicts, semantic, probabilistic
        )

        # Determine result
        result = self._determine_domain_result(overall_score, conflicts, probabilistic)

        # Generate recommendations
        recommendations = self._generate_domain_recommendations(
            conflicts, impacts, result, domain_context
        )

        # Create base evaluation
        reason = self._generate_domain_reason(
            conflicts, impacts, overall_score, domain_context
        )

        alternative = self._generate_domain_alternative(
            conflicts, domain_context
        ) if conflicts else None

        base_evaluation = DirectiveEvaluation(
            result=result,
            reason=reason,
            alternative=alternative,
            confidence=self._calculate_domain_confidence(
                impacts, conflicts, probabilistic
            ),
        )

        return DetailedEvaluation(
            base_evaluation=base_evaluation,
            impacts=impacts,
            conflicts=conflicts,
            overall_score=overall_score,
            recommendations=recommendations,
            semantic_context=semantic,
            probabilistic_assessment=probabilistic,
        )

    def _extract_domain_context(
        self,
        intent: str,
        context: Dict,
    ) -> DomainSpecificContext:
        """
        Extract domain-specific context from the intent and context.

        Override this method to extract information specific to your domain.
        """
        return DomainSpecificContext(
            domain_name=self.domain_name,
            technology_type=context.get("technology_type", "general"),
            risk_factors=context.get("risk_factors", []),
            special_considerations=context.get("special_considerations", []),
        )

    def _assess_domain_impacts(
        self,
        intent: str,
        domain_context: DomainSpecificContext,
    ) -> List[ImpactAssessment]:
        """
        Assess domain-specific impacts.

        Override this method to implement domain-specific harm detection.
        """
        impacts = []

        # Example: Check for domain-specific harm indicators
        for category, keywords in self.DOMAIN_HARM_INDICATORS.items():
            for keyword in keywords:
                if keyword in intent:
                    impacts.append(ImpactAssessment(
                        category=ImpactCategory.PRIVACY,  # Choose appropriate category
                        severity=0.8,
                        affected_parties=["users of the technology"],
                        description=f"Domain-specific risk detected: {keyword}",
                    ))
                    break

        return impacts

    def _detect_domain_conflicts(
        self,
        intent: str,
        domain_context: DomainSpecificContext,
    ) -> List[ConflictAssessment]:
        """
        Detect domain-specific conflicts with the Core Directive.

        Override this method to implement domain-specific conflict detection.
        """
        conflicts = []

        # Example: Detect domain-specific violations
        # (Replace with actual domain logic)

        return conflicts

    def _analyze_domain_semantics(
        self,
        intent: str,
        domain_context: DomainSpecificContext,
    ) -> SemanticContext:
        """
        Perform domain-specific semantic analysis.

        Override this method to analyze domain-specific semantics.
        """
        # Default implementation - override for domain-specific logic
        return SemanticContext(
            intent_type="neutral",
            entities=[],
            sentiment=0.0,
            ambiguity_score=0.3,
            context_clues=[f"Domain: {self.domain_name}"],
        )

    def _assess_domain_probabilities(
        self,
        intent: str,
        impacts: List[ImpactAssessment],
        conflicts: List[ConflictAssessment],
        semantic: SemanticContext,
    ) -> ProbabilisticAssessment:
        """
        Perform domain-specific probabilistic assessment.

        Override this method for domain-specific risk calculation.
        """
        harm_prob = sum(i.severity for i in impacts) / max(len(impacts), 1) if impacts else 0.0
        benefit_prob = max(0.0, semantic.sentiment)

        return ProbabilisticAssessment(
            harm_probability=harm_prob,
            benefit_probability=benefit_prob,
            uncertainty=semantic.ambiguity_score,
            risk_level="medium" if harm_prob > 0.5 else "low",
            expected_outcome="Domain-specific evaluation required",
        )

    def _calculate_domain_score(
        self,
        impacts: List[ImpactAssessment],
        conflicts: List[ConflictAssessment],
        semantic: SemanticContext,
        probabilistic: ProbabilisticAssessment,
    ) -> float:
        """Calculate domain-specific score."""
        score = 0.0

        # Penalize for impacts and conflicts
        score -= sum(i.severity for i in impacts) * 0.4
        score -= sum(c.severity for c in conflicts if c.conflict_type != ConflictType.NONE) * 0.6

        # Reward for positive indicators
        score += semantic.sentiment * 0.3
        score += (probabilistic.benefit_probability - probabilistic.harm_probability) * 0.4

        return max(-1.0, min(1.0, score))

    def _determine_domain_result(
        self,
        score: float,
        conflicts: List[ConflictAssessment],
        probabilistic: ProbabilisticAssessment,
    ) -> ActionResult:
        """Determine action result based on domain-specific criteria."""
        if probabilistic.risk_level == "critical":
            return ActionResult.BLOCKED

        if score < -0.5:
            return ActionResult.BLOCKED
        elif score < 0 or probabilistic.harm_probability > 0.6:
            return ActionResult.REVIEW
        else:
            return ActionResult.ALLOWED

    def _generate_domain_recommendations(
        self,
        conflicts: List[ConflictAssessment],
        impacts: List[ImpactAssessment],
        result: ActionResult,
        domain_context: DomainSpecificContext,
    ) -> List[str]:
        """Generate domain-specific recommendations."""
        recommendations = []

        if result == ActionResult.BLOCKED:
            recommendations.append(
                f"Request blocked due to {self.domain_name}-specific concerns"
            )

        # Add domain-specific guidance
        recommendations.append(
            f"Ensure compliance with {self.domain_name} best practices"
        )

        return recommendations

    def _generate_domain_reason(
        self,
        conflicts: List[ConflictAssessment],
        impacts: List[ImpactAssessment],
        score: float,
        domain_context: DomainSpecificContext,
    ) -> str:
        """Generate domain-specific reason."""
        if conflicts:
            return f"Domain ({self.domain_name}): " + "; ".join(
                c.description for c in conflicts[:2]
            )

        if impacts:
            return f"Domain ({self.domain_name}): " + "; ".join(
                i.description for i in impacts[:2]
            )

        return f"No {self.domain_name}-specific issues detected"

    def _generate_domain_alternative(
        self,
        conflicts: List[ConflictAssessment],
        domain_context: DomainSpecificContext,
    ) -> Optional[str]:
        """Generate domain-specific alternatives."""
        for conflict in conflicts:
            if conflict.suggested_resolution:
                return f"{conflict.suggested_resolution} (Domain: {self.domain_name})"

        return None

    def _calculate_domain_confidence(
        self,
        impacts: List[ImpactAssessment],
        conflicts: List[ConflictAssessment],
        probabilistic: ProbabilisticAssessment,
    ) -> float:
        """Calculate confidence in domain evaluation."""
        base_confidence = 0.7  # Domain-specific evaluators have good confidence

        # Reduce for high uncertainty
        confidence = base_confidence * (1.0 - probabilistic.uncertainty * 0.3)

        return max(0.5, min(0.95, confidence))


# Example usage and registration
def register_with_core_evaluator():
    """
    Example of how to register this domain evaluator with the core.
    
    Call this function during system initialization to integrate
    your domain-specific evaluator.
    """
    from evaluator import get_evaluator

    # Create domain evaluator instance
    domain_eval = DomainEvaluatorTemplate(domain_name="example_domain")

    # Register with core evaluator
    core_evaluator = get_evaluator()
    core_evaluator.register_domain_evaluator(
        domain="example_domain",
        evaluator=domain_eval.evaluate,
    )

    print(f"Registered {domain_eval.domain_name} evaluator with core")


if __name__ == "__main__":
    # Test the domain evaluator
    evaluator = DomainEvaluatorTemplate("test_domain")
    
    test_intent = "Use this technology to help people"
    result = evaluator.evaluate(test_intent)
    
    print(f"Intent: {test_intent}")
    print(f"Result: {result.base_evaluation.result}")
    print(f"Reason: {result.base_evaluation.reason}")
    print(f"Score: {result.overall_score:.2f}")
