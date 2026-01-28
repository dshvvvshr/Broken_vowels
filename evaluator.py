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
6. Semantic understanding of intent and context
7. Probabilistic reasoning for ambiguity handling
8. Domain-specific evaluation support
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional, Dict, List, Callable
import re

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
class SemanticContext:
    """Semantic context for intent evaluation."""
    intent_type: str  # help, harm, neutral, ambiguous
    entities: list[str]  # extracted entities (people, objects, actions)
    sentiment: float  # -1.0 (negative) to 1.0 (positive)
    ambiguity_score: float  # 0.0 (clear) to 1.0 (highly ambiguous)
    context_clues: list[str]  # additional context information


@dataclass
class ProbabilisticAssessment:
    """Probabilistic assessment of outcomes and risks."""
    harm_probability: float  # 0.0 to 1.0
    benefit_probability: float  # 0.0 to 1.0
    uncertainty: float  # 0.0 (certain) to 1.0 (highly uncertain)
    risk_level: str  # "low", "medium", "high", "critical"
    expected_outcome: str  # description of most likely outcome


@dataclass
class DetailedEvaluation:
    """Detailed evaluation result with comprehensive analysis."""
    base_evaluation: DirectiveEvaluation
    impacts: list[ImpactAssessment]
    conflicts: list[ConflictAssessment]
    overall_score: float  # -1.0 (harmful) to 1.0 (beneficial)
    recommendations: list[str]
    semantic_context: Optional[SemanticContext] = None
    probabilistic_assessment: Optional[ProbabilisticAssessment] = None


class DirectiveEvaluator:
    """
    Core Directive Evaluation Engine

    Provides sophisticated evaluation of actions and intents against
    the Core Directive, with detailed analysis of potential impacts,
    conflicts, semantic understanding, and probabilistic reasoning.
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

    # Ambiguity indicators
    AMBIGUITY_INDICATORS = [
        "maybe", "possibly", "might", "could", "unclear", "uncertain",
        "depends", "sometimes", "perhaps", "potentially"
    ]

    def __init__(self):
        """Initialize the evaluator."""
        self._evaluation_count = 0
        self._domain_evaluators: Dict[str, Callable] = {}

    @property
    def evaluation_count(self) -> int:
        """Return the number of evaluations performed."""
        return self._evaluation_count

    def register_domain_evaluator(
        self,
        domain: str,
        evaluator: Callable[[str, Optional[dict]], DetailedEvaluation]
    ) -> None:
        """
        Register a domain-specific evaluator.
        
        Args:
            domain: The domain name (e.g., "neural_interface", "rf_sensing")
            evaluator: Callable that performs domain-specific evaluation
        """
        self._domain_evaluators[domain] = evaluator

    def get_domain_evaluators(self) -> List[str]:
        """Return list of registered domain evaluators."""
        return list(self._domain_evaluators.keys())

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

        # Check for domain-specific evaluation
        domain = context.get("domain")
        if domain and domain in self._domain_evaluators:
            return self._domain_evaluators[domain](intent, context)

        # Perform semantic analysis
        semantic_context = self._analyze_semantics(intent, intent_lower, context)

        # Assess impacts
        impacts = self._assess_impacts(intent_lower)

        # Detect conflicts
        conflicts = self._detect_conflicts(intent_lower, impacts)

        # Perform probabilistic assessment
        probabilistic = self._assess_probabilities(
            intent_lower, impacts, conflicts, semantic_context
        )

        # Calculate overall score
        overall_score = self._calculate_score(
            impacts, conflicts, intent_lower, semantic_context, probabilistic
        )

        # Determine action result
        action_result = self._determine_result(
            overall_score, conflicts, probabilistic
        )

        # Generate recommendations
        recommendations = self._generate_recommendations(
            conflicts, impacts, action_result, semantic_context
        )

        # Create base evaluation
        reason = self._generate_reason(
            conflicts, impacts, overall_score, semantic_context
        )
        alternative = self._generate_alternative(
            conflicts, semantic_context
        ) if conflicts else None

        base_evaluation = DirectiveEvaluation(
            result=action_result,
            reason=reason,
            alternative=alternative,
            confidence=self._calculate_confidence(
                impacts, conflicts, semantic_context, probabilistic
            ),
        )

        return DetailedEvaluation(
            base_evaluation=base_evaluation,
            impacts=impacts,
            conflicts=conflicts,
            overall_score=overall_score,
            recommendations=recommendations,
            semantic_context=semantic_context,
            probabilistic_assessment=probabilistic,
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

    def _analyze_semantics(
        self,
        intent: str,
        intent_lower: str,
        context: dict,
    ) -> SemanticContext:
        """
        Analyze the semantic context of the intent.
        
        This provides enhanced understanding of nuanced scenarios.
        """
        # Determine intent type
        intent_type = "neutral"
        if any(kw in intent_lower for keywords in self.POSITIVE_INDICATORS.values() for kw in keywords):
            intent_type = "help"
        elif any(kw in intent_lower for keywords in self.HARM_INDICATORS.values() for kw in keywords):
            intent_type = "harm"
        
        # Check for ambiguity
        ambiguity_score = sum(
            0.15 for indicator in self.AMBIGUITY_INDICATORS
            if indicator in intent_lower
        )
        ambiguity_score = min(1.0, ambiguity_score)
        
        if ambiguity_score > 0.5:
            intent_type = "ambiguous"

        # Extract basic entities (simplified)
        entities = self._extract_entities(intent)

        # Calculate sentiment
        sentiment = self._calculate_sentiment(intent_lower)

        # Extract context clues
        context_clues = []
        if context.get("user_history"):
            context_clues.append("User has interaction history")
        if context.get("urgent"):
            context_clues.append("Marked as urgent request")
        if context.get("educational"):
            context_clues.append("Educational context")

        return SemanticContext(
            intent_type=intent_type,
            entities=entities,
            sentiment=sentiment,
            ambiguity_score=ambiguity_score,
            context_clues=context_clues,
        )

    def _extract_entities(self, intent: str) -> List[str]:
        """Extract entities from intent (simplified implementation)."""
        # Look for quoted strings and capitalized words as potential entities
        entities = []
        
        # Find quoted strings
        quoted = re.findall(r'"([^"]*)"', intent)
        entities.extend(quoted)
        
        # Find capitalized words (excluding first word)
        words = intent.split()
        for i, word in enumerate(words):
            if i > 0 and word and word[0].isupper() and word.isalpha():
                entities.append(word)
        
        return list(set(entities))[:5]  # Limit to 5 entities

    def _calculate_sentiment(self, intent_lower: str) -> float:
        """Calculate sentiment score from -1.0 to 1.0."""
        positive_count = sum(
            1 for keywords in self.POSITIVE_INDICATORS.values()
            for keyword in keywords
            if keyword in intent_lower
        )
        negative_count = sum(
            1 for keywords in self.HARM_INDICATORS.values()
            for keyword in keywords
            if keyword in intent_lower
        )
        
        if positive_count == 0 and negative_count == 0:
            return 0.0
        
        total = positive_count + negative_count
        return (positive_count - negative_count) / max(total, 1)

    def _assess_probabilities(
        self,
        intent: str,
        impacts: List[ImpactAssessment],
        conflicts: List[ConflictAssessment],
        semantic: SemanticContext,
    ) -> ProbabilisticAssessment:
        """
        Perform probabilistic assessment of outcomes and risks.
        
        This uses fuzzy logic and probabilistic reasoning to handle ambiguities.
        """
        # Calculate harm probability
        harm_prob = 0.0
        if impacts:
            harm_prob = sum(i.severity for i in impacts) / len(impacts)
        
        # Adjust for conflicts
        if conflicts:
            severe_conflicts = [
                c for c in conflicts
                if c.conflict_type != ConflictType.NONE and c.severity >= 0.7
            ]
            if severe_conflicts:
                harm_prob = max(harm_prob, sum(c.severity for c in severe_conflicts) / len(severe_conflicts))
        
        # Calculate benefit probability
        benefit_prob = max(0.0, semantic.sentiment)
        if semantic.intent_type == "help":
            benefit_prob = max(benefit_prob, 0.6)
        
        # Calculate uncertainty
        uncertainty = semantic.ambiguity_score
        if not impacts and not conflicts:
            uncertainty = max(uncertainty, 0.4)  # Lack of clear indicators = uncertainty
        
        # Determine risk level using fuzzy logic
        risk_level = "low"
        if harm_prob > 0.7 or (harm_prob > 0.4 and uncertainty < 0.3):
            risk_level = "critical"
        elif harm_prob > 0.5 or (harm_prob > 0.3 and uncertainty > 0.6):
            risk_level = "high"
        elif harm_prob > 0.3 or uncertainty > 0.7:
            risk_level = "medium"
        
        # Determine expected outcome
        if harm_prob > benefit_prob + 0.2:
            expected_outcome = "Likely to interfere with others' pursuit of happiness"
        elif benefit_prob > harm_prob + 0.2:
            expected_outcome = "Likely to support others' pursuit of happiness"
        else:
            expected_outcome = "Outcome uncertain - requires human review"
        
        return ProbabilisticAssessment(
            harm_probability=harm_prob,
            benefit_probability=benefit_prob,
            uncertainty=uncertainty,
            risk_level=risk_level,
            expected_outcome=expected_outcome,
        )

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
        semantic: SemanticContext,
        probabilistic: ProbabilisticAssessment,
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

        # Adjust based on semantic sentiment
        score += semantic.sentiment * 0.3

        # Adjust based on probabilistic assessment
        score += (probabilistic.benefit_probability - probabilistic.harm_probability) * 0.4

        # Penalize high uncertainty
        if probabilistic.uncertainty > 0.6:
            score -= 0.2

        # Clamp to range
        return max(-1.0, min(1.0, score))

    def _determine_result(
        self,
        score: float,
        conflicts: list[ConflictAssessment],
        probabilistic: ProbabilisticAssessment,
    ) -> ActionResult:
        """Determine the action result based on score, conflicts, and probabilities."""
        # Check for critical risk
        if probabilistic.risk_level == "critical":
            return ActionResult.BLOCKED

        # Check for severe conflicts
        severe_conflicts = [
            c for c in conflicts
            if c.conflict_type != ConflictType.NONE and c.severity >= 0.9
        ]
        if severe_conflicts:
            return ActionResult.BLOCKED

        # High risk or high uncertainty requires review
        if probabilistic.risk_level == "high" or probabilistic.uncertainty > 0.7:
            return ActionResult.REVIEW

        # Score-based determination with probabilistic adjustment
        if score < -0.5:
            return ActionResult.BLOCKED
        elif score < 0 or probabilistic.harm_probability > 0.5:
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
        semantic: SemanticContext,
    ) -> str:
        """Generate a human-readable reason for the evaluation."""
        if not conflicts and not impacts:
            if semantic.ambiguity_score > 0.6:
                return f"Request is ambiguous (ambiguity: {semantic.ambiguity_score:.1%}). Additional clarification recommended for accurate assessment."
            return "No potential issues detected"

        if conflicts:
            significant = [
                c for c in conflicts
                if c.conflict_type != ConflictType.NONE
            ]
            if significant:
                reason = "; ".join(c.description for c in significant[:2])
                if semantic.ambiguity_score > 0.5:
                    reason += f" Note: Request has high ambiguity ({semantic.ambiguity_score:.1%})"
                return reason

        if impacts:
            reason = "; ".join(i.description for i in impacts[:2])
            if semantic.intent_type == "ambiguous":
                reason += ". Intent is unclear and requires review"
            return reason

        return f"Evaluation score: {score:.2f}"

    def _generate_alternative(
        self,
        conflicts: list[ConflictAssessment],
        semantic: SemanticContext,
    ) -> Optional[str]:
        """Generate alternative suggestions for problematic intents."""
        for conflict in conflicts:
            if conflict.suggested_resolution:
                if semantic.ambiguity_score > 0.6:
                    return f"{conflict.suggested_resolution}. Please clarify your intent to ensure alignment with the Core Directive."
                return conflict.suggested_resolution
        
        if semantic.intent_type == "harm":
            return "Consider reframing your request to focus on constructive outcomes that respect everyone's right to pursue happiness."
        
        return None

    def _generate_recommendations(
        self,
        conflicts: list[ConflictAssessment],
        impacts: list[ImpactAssessment],
        result: ActionResult,
        semantic: SemanticContext,
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
            if semantic.ambiguity_score > 0.6:
                recommendations.append(
                    "Provide more specific details about your intent to reduce ambiguity"
                )
            recommendations.append(
                "Clarify your intent to ensure it doesn't impact others negatively"
            )

        # Add semantic-based recommendations for moderate ambiguity
        if semantic.ambiguity_score > 0.4:
            recommendations.append(
                "Your request contains ambiguous terms. Please be more explicit about your goals."
            )

        if semantic.intent_type == "ambiguous":
            recommendations.append(
                "Request is unclear - please provide more specific details to ensure accurate assessment."
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
        semantic: SemanticContext,
        probabilistic: ProbabilisticAssessment,
    ) -> float:
        """Calculate confidence in the evaluation."""
        if not impacts and not conflicts:
            return 0.5  # Low confidence when no indicators found

        # Higher confidence with more indicators
        indicator_count = len(impacts) + len(conflicts)
        base_confidence = min(0.95, 0.6 + indicator_count * 0.1)

        # Reduce confidence for high ambiguity
        confidence = base_confidence * (1.0 - semantic.ambiguity_score * 0.3)

        # Reduce confidence for high uncertainty
        confidence *= (1.0 - probabilistic.uncertainty * 0.2)

        return max(0.3, min(0.95, confidence))

    def _create_empty_evaluation(self) -> DetailedEvaluation:
        """Create an evaluation for empty input."""
        base = DirectiveEvaluation(
            result=ActionResult.REVIEW,
            reason="No intent provided for evaluation",
            confidence=1.0,
        )
        
        semantic = SemanticContext(
            intent_type="neutral",
            entities=[],
            sentiment=0.0,
            ambiguity_score=1.0,  # Complete lack of information is ambiguous
            context_clues=["No input provided"],
        )
        
        probabilistic = ProbabilisticAssessment(
            harm_probability=0.0,
            benefit_probability=0.0,
            uncertainty=1.0,
            risk_level="low",
            expected_outcome="No action to evaluate",
        )
        
        return DetailedEvaluation(
            base_evaluation=base,
            impacts=[],
            conflicts=[],
            overall_score=0.0,
            recommendations=["Please provide a clear statement of intent"],
            semantic_context=semantic,
            probabilistic_assessment=probabilistic,
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
