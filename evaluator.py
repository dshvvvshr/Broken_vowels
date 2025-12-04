"""
Evaluator Module - Core Directive Evaluation Engine

This module provides sophisticated evaluation capabilities for assessing
actions and intents against the Core Directive. It implements a multi-factor
analysis to determine whether actions align with the principle of protecting
individuals' right to pursue happiness.

Evaluation Features:
1. Multi-factor harm assessment
2. Context-aware evaluation
3. Conflict detection and resolution
4. Impact scoring
5. Alternative suggestion generation
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional

from core_directive import ActionResult, DirectiveEvaluation


class ImpactCategory(Enum):
    """Categories of potential impact on individuals."""
    PHYSICAL = "physical"
    EMOTIONAL = "emotional"
    FINANCIAL = "financial"
    SOCIAL = "social"
    AUTONOMY = "autonomy"
    PRIVACY = "privacy"


class ConflictType(Enum):
    """Types of conflicts that may arise."""
    NONE = "none"
    SELF_HARM = "self_harm"
    DIRECT_HARM = "direct_harm"
    INDIRECT_HARM = "indirect_harm"
    EXPLOITATION = "exploitation"
    COERCION = "coercion"
    DECEPTION = "deception"


@dataclass
class ImpactAssessment:
    """Assessment of potential impact on individuals."""
    category: ImpactCategory
    severity: float  # 0.0 to 1.0
    affected_parties: list[str]
    description: str


@dataclass
class ConflictAssessment:
    """Assessment of conflicts with the Core Directive."""
    conflict_type: ConflictType
    severity: float  # 0.0 to 1.0
    description: str
    resolution_possible: bool
    suggested_resolution: Optional[str] = None


@dataclass
class DetailedEvaluation:
    """Detailed evaluation result with comprehensive analysis."""
    base_evaluation: DirectiveEvaluation
    impacts: list[ImpactAssessment]
    conflicts: list[ConflictAssessment]
    overall_score: float  # -1.0 (harmful) to 1.0 (beneficial)
    recommendations: list[str]


class DirectiveEvaluator:
    """
    Core Directive Evaluation Engine

    Provides sophisticated evaluation of actions and intents against
    the Core Directive, with detailed analysis of potential impacts
    and conflicts.
    """

    # Keywords indicating potential harm
    HARM_INDICATORS = {
        "physical": [
            "harm", "hurt", "injure", "attack", "assault", "kill",
            "wound", "damage", "destroy", "violence"
        ],
        "emotional": [
            "harass", "bully", "intimidate", "threaten", "abuse",
            "humiliate", "demean", "terrorize"
        ],
        "financial": [
            "steal", "fraud", "scam", "extort", "embezzle",
            "swindle", "cheat"
        ],
        "social": [
            "isolate", "exclude", "discriminate", "defame",
            "slander", "libel"
        ],
        "autonomy": [
            "force", "coerce", "manipulate", "control", "dominate",
            "compel", "pressure"
        ],
        "privacy": [
            "spy", "stalk", "surveil", "expose", "dox", "leak"
        ],
    }

    # Keywords indicating positive intent
    POSITIVE_INDICATORS = {
        "helpful": [
            "help", "assist", "support", "aid", "serve", "guide"
        ],
        "constructive": [
            "build", "create", "develop", "improve", "enhance", "grow"
        ],
        "protective": [
            "protect", "defend", "safeguard", "secure", "preserve"
        ],
        "educational": [
            "teach", "learn", "educate", "train", "inform", "explain"
        ],
        "empowering": [
            "enable", "empower", "facilitate", "encourage", "inspire"
        ],
    }

    def __init__(self):
        """Initialize the evaluator."""
        self._evaluation_count = 0

    @property
    def evaluation_count(self) -> int:
        """Return the number of evaluations performed."""
        return self._evaluation_count

    def evaluate(self, intent: str, context: Optional[dict] = None) -> DetailedEvaluation:
        """
        Perform detailed evaluation of an intent.

        Args:
            intent: The stated intent or action to evaluate
            context: Optional context information for nuanced evaluation

        Returns:
            DetailedEvaluation with comprehensive analysis
        """
        self._evaluation_count += 1

        if not intent or not intent.strip():
            return self._create_empty_evaluation()

        intent_lower = intent.lower()
        context = context or {}

        # Assess impacts
        impacts = self._assess_impacts(intent_lower)

        # Detect conflicts
        conflicts = self._detect_conflicts(intent_lower, impacts)

        # Calculate overall score
        overall_score = self._calculate_score(impacts, conflicts, intent_lower)

        # Determine action result
        action_result = self._determine_result(overall_score, conflicts)

        # Generate recommendations
        recommendations = self._generate_recommendations(
            conflicts, impacts, action_result
        )

        # Create base evaluation
        reason = self._generate_reason(conflicts, impacts, overall_score)
        alternative = self._generate_alternative(conflicts) if conflicts else None

        base_evaluation = DirectiveEvaluation(
            result=action_result,
            reason=reason,
            alternative=alternative,
            confidence=self._calculate_confidence(impacts, conflicts),
        )

        return DetailedEvaluation(
            base_evaluation=base_evaluation,
            impacts=impacts,
            conflicts=conflicts,
            overall_score=overall_score,
            recommendations=recommendations,
        )

    def _assess_impacts(self, intent: str) -> list[ImpactAssessment]:
        """Assess potential impacts across all categories."""
        impacts = []

        for category_name, keywords in self.HARM_INDICATORS.items():
            for keyword in keywords:
                if keyword in intent:
                    category = ImpactCategory(category_name)
                    impacts.append(ImpactAssessment(
                        category=category,
                        severity=0.7,  # Default severity for detected terms
                        affected_parties=["potentially affected individuals"],
                        description=f"Detected potential {category_name} harm indicator: '{keyword}'",
                    ))
                    break  # One impact per category

        return impacts

    def _detect_conflicts(
        self,
        intent: str,
        impacts: list[ImpactAssessment],
    ) -> list[ConflictAssessment]:
        """Detect conflicts with the Core Directive."""
        conflicts = []

        # Check for direct harm
        direct_harm_keywords = ["harm", "hurt", "attack", "kill", "destroy"]
        for keyword in direct_harm_keywords:
            if keyword in intent:
                conflicts.append(ConflictAssessment(
                    conflict_type=ConflictType.DIRECT_HARM,
                    severity=0.9,
                    description=f"Intent suggests direct harm: '{keyword}'",
                    resolution_possible=True,
                    suggested_resolution="Consider rephrasing to focus on constructive outcomes",
                ))
                break

        # Check for exploitation
        exploitation_keywords = ["exploit", "use", "take advantage"]
        for keyword in exploitation_keywords:
            if keyword in intent:
                conflicts.append(ConflictAssessment(
                    conflict_type=ConflictType.EXPLOITATION,
                    severity=0.8,
                    description=f"Intent suggests exploitation: '{keyword}'",
                    resolution_possible=True,
                    suggested_resolution="Consider mutual benefit and consent",
                ))
                break

        # Check for coercion
        coercion_keywords = ["force", "coerce", "compel", "make them"]
        for keyword in coercion_keywords:
            if keyword in intent:
                conflicts.append(ConflictAssessment(
                    conflict_type=ConflictType.COERCION,
                    severity=0.85,
                    description=f"Intent suggests coercion: '{keyword}'",
                    resolution_possible=True,
                    suggested_resolution="Consider voluntary cooperation and consent",
                ))
                break

        # Check for deception
        deception_keywords = ["deceive", "lie", "trick", "mislead", "fool"]
        for keyword in deception_keywords:
            if keyword in intent:
                conflicts.append(ConflictAssessment(
                    conflict_type=ConflictType.DECEPTION,
                    severity=0.75,
                    description=f"Intent suggests deception: '{keyword}'",
                    resolution_possible=True,
                    suggested_resolution="Consider honest and transparent communication",
                ))
                break

        # No conflicts if positive indicators dominate
        if not conflicts and self._has_positive_indicators(intent):
            conflicts.append(ConflictAssessment(
                conflict_type=ConflictType.NONE,
                severity=0.0,
                description="No conflicts detected; intent appears constructive",
                resolution_possible=True,
            ))

        return conflicts

    def _has_positive_indicators(self, intent: str) -> bool:
        """Check if intent contains positive indicators."""
        for keywords in self.POSITIVE_INDICATORS.values():
            for keyword in keywords:
                if keyword in intent:
                    return True
        return False

    def _calculate_score(
        self,
        impacts: list[ImpactAssessment],
        conflicts: list[ConflictAssessment],
        intent: str,
    ) -> float:
        """Calculate overall score from -1.0 (harmful) to 1.0 (beneficial)."""
        score = 0.0

        # Negative score for impacts
        for impact in impacts:
            score -= impact.severity * 0.3

        # Negative score for conflicts
        for conflict in conflicts:
            if conflict.conflict_type != ConflictType.NONE:
                score -= conflict.severity * 0.5

        # Positive score for positive indicators
        positive_count = sum(
            1 for keywords in self.POSITIVE_INDICATORS.values()
            for keyword in keywords
            if keyword in intent
        )
        score += positive_count * 0.2

        # Clamp to range
        return max(-1.0, min(1.0, score))

    def _determine_result(
        self,
        score: float,
        conflicts: list[ConflictAssessment],
    ) -> ActionResult:
        """Determine the action result based on score and conflicts."""
        # Check for severe conflicts
        severe_conflicts = [
            c for c in conflicts
            if c.conflict_type != ConflictType.NONE and c.severity >= 0.9
        ]
        if severe_conflicts:
            return ActionResult.BLOCKED

        # Score-based determination
        if score < -0.5:
            return ActionResult.BLOCKED
        elif score < 0:
            return ActionResult.REVIEW
        elif score < 0.3:
            return ActionResult.ALLOWED
        else:
            return ActionResult.ALLOWED

    def _generate_reason(
        self,
        conflicts: list[ConflictAssessment],
        impacts: list[ImpactAssessment],
        score: float,
    ) -> str:
        """Generate a human-readable reason for the evaluation."""
        if not conflicts and not impacts:
            return "No potential issues detected"

        if conflicts:
            significant = [
                c for c in conflicts
                if c.conflict_type != ConflictType.NONE
            ]
            if significant:
                return "; ".join(c.description for c in significant[:2])

        if impacts:
            return "; ".join(i.description for i in impacts[:2])

        return f"Evaluation score: {score:.2f}"

    def _generate_alternative(
        self,
        conflicts: list[ConflictAssessment],
    ) -> Optional[str]:
        """Generate alternative suggestions for problematic intents."""
        for conflict in conflicts:
            if conflict.suggested_resolution:
                return conflict.suggested_resolution
        return None

    def _generate_recommendations(
        self,
        conflicts: list[ConflictAssessment],
        impacts: list[ImpactAssessment],
        result: ActionResult,
    ) -> list[str]:
        """Generate recommendations based on the evaluation."""
        recommendations = []

        if result == ActionResult.BLOCKED:
            recommendations.append(
                "Consider reframing your request to focus on mutual benefit"
            )
            recommendations.append(
                "Ensure all parties involved have given consent"
            )

        if result == ActionResult.REVIEW:
            recommendations.append(
                "Clarify your intent to ensure it doesn't impact others negatively"
            )

        for conflict in conflicts:
            if conflict.suggested_resolution:
                recommendations.append(conflict.suggested_resolution)

        if not recommendations:
            recommendations.append("Intent aligns with the Core Directive")

        return list(set(recommendations))  # Remove duplicates

    def _calculate_confidence(
        self,
        impacts: list[ImpactAssessment],
        conflicts: list[ConflictAssessment],
    ) -> float:
        """Calculate confidence in the evaluation."""
        if not impacts and not conflicts:
            return 0.5  # Low confidence when no indicators found

        # Higher confidence with more indicators
        indicator_count = len(impacts) + len(conflicts)
        return min(0.95, 0.6 + indicator_count * 0.1)

    def _create_empty_evaluation(self) -> DetailedEvaluation:
        """Create an evaluation for empty input."""
        base = DirectiveEvaluation(
            result=ActionResult.REVIEW,
            reason="No intent provided for evaluation",
            confidence=1.0,
        )
        return DetailedEvaluation(
            base_evaluation=base,
            impacts=[],
            conflicts=[],
            overall_score=0.0,
            recommendations=["Please provide a clear statement of intent"],
        )

    def __repr__(self) -> str:
        return f"DirectiveEvaluator(evaluations={self._evaluation_count})"


# Module-level convenience functions


_default_evaluator: Optional[DirectiveEvaluator] = None


def get_evaluator() -> DirectiveEvaluator:
    """Get the default evaluator instance."""
    global _default_evaluator
    if _default_evaluator is None:
        _default_evaluator = DirectiveEvaluator()
    return _default_evaluator


def evaluate_detailed(
    intent: str,
    context: Optional[dict] = None,
) -> DetailedEvaluation:
    """Convenience function to perform detailed evaluation."""
    return get_evaluator().evaluate(intent, context)
