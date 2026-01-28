#!/usr/bin/env python3
"""
Example demonstrations of the Enhanced Evaluation Kernel

This script demonstrates the new features:
1. Semantic evaluation
2. Probabilistic reasoning
3. Refusal strategies
4. Domain-specific evaluators
"""

from evaluator import get_evaluator, DetailedEvaluation
from core_directive_gateway import evaluate_request_content, RefusalStrategy


def print_separator(title=""):
    """Print a visual separator."""
    print("\n" + "=" * 80)
    if title:
        print(f"  {title}")
        print("=" * 80)
    print()


def demo_semantic_evaluation():
    """Demonstrate semantic evaluation capabilities."""
    print_separator("1. SEMANTIC EVALUATION")
    
    evaluator = get_evaluator()
    
    test_cases = [
        "I want to help people learn programming",
        "I want to harm and manipulate people",
        "Maybe I might possibly do something unclear",
    ]
    
    for intent in test_cases:
        print(f"Intent: '{intent}'")
        result = evaluator.evaluate(intent)
        
        sem = result.semantic_context
        print(f"  Intent Type: {sem.intent_type}")
        print(f"  Sentiment: {sem.sentiment:+.2f}")
        print(f"  Ambiguity: {sem.ambiguity_score:.2%}")
        if sem.entities:
            print(f"  Entities: {', '.join(sem.entities)}")
        print(f"  Decision: {result.base_evaluation.result.value}")
        print()


def demo_probabilistic_reasoning():
    """Demonstrate probabilistic reasoning."""
    print_separator("2. PROBABILISTIC REASONING")
    
    evaluator = get_evaluator()
    
    test_cases = [
        "I want to exploit and manipulate people",
        "I want to help and empower communities",
        "Something ambiguous and uncertain",
    ]
    
    for intent in test_cases:
        print(f"Intent: '{intent}'")
        result = evaluator.evaluate(intent)
        
        prob = result.probabilistic_assessment
        print(f"  Harm Probability: {prob.harm_probability:.2%}")
        print(f"  Benefit Probability: {prob.benefit_probability:.2%}")
        print(f"  Uncertainty: {prob.uncertainty:.2%}")
        print(f"  Risk Level: {prob.risk_level}")
        print(f"  Expected Outcome: {prob.expected_outcome}")
        print()


def demo_refusal_strategies():
    """Demonstrate refusal and mediation strategies."""
    print_separator("3. REFUSAL STRATEGIES")
    
    test_cases = [
        ("I want to kill someone", "BLOCK"),
        ("I want to manipulate and exploit", "SLOWDOWN"),
        ("Maybe I should monitor their activity", "REDIRECT"),
        ("I want to pressure them", "ALERT"),
        ("I want to help people learn", "ALLOWED"),
    ]
    
    for intent, expected_type in test_cases:
        print(f"Intent: '{intent}'")
        result = evaluate_request_content(intent)
        
        print(f"  Strategy: {result.strategy.value.upper()}")
        print(f"  Allowed: {result.allowed}")
        print(f"  Explanation: {result.explanation[:80]}...")
        
        if result.alternatives:
            print(f"  Alternatives ({len(result.alternatives)}):")
            for alt in result.alternatives[:2]:
                print(f"    • {alt[:70]}...")
        
        if result.delay_seconds:
            print(f"  Delay: {result.delay_seconds}s")
        
        print()


def demo_enhanced_scoring():
    """Demonstrate enhanced scoring with semantic and probabilistic factors."""
    print_separator("4. ENHANCED SCORING")
    
    evaluator = get_evaluator()
    
    test_cases = [
        "I want to help, support, and enable people to grow",
        "I want to harm, attack, and destroy",
        "Do something neutral",
    ]
    
    for intent in test_cases:
        print(f"Intent: '{intent}'")
        result = evaluator.evaluate(intent)
        
        print(f"  Overall Score: {result.overall_score:+.2f}")
        print(f"  Decision: {result.base_evaluation.result.value}")
        print(f"  Confidence: {result.base_evaluation.confidence:.2%}")
        print(f"  Reason: {result.base_evaluation.reason}")
        
        if result.recommendations:
            print(f"  Recommendations:")
            for rec in result.recommendations[:2]:
                print(f"    • {rec}")
        print()


def demo_domain_specific_evaluator():
    """Demonstrate domain-specific evaluator registration."""
    print_separator("5. DOMAIN-SPECIFIC EVALUATORS")
    
    evaluator = get_evaluator()
    
    # Simple example domain evaluator
    def example_domain_evaluator(intent, context):
        from evaluator import (
            DetailedEvaluation, DirectiveEvaluation, ActionResult,
            SemanticContext, ProbabilisticAssessment
        )
        
        return DetailedEvaluation(
            base_evaluation=DirectiveEvaluation(
                result=ActionResult.ALLOWED,
                reason=f"Example domain evaluated: '{intent[:30]}...'",
                confidence=0.85,
            ),
            impacts=[],
            conflicts=[],
            overall_score=0.7,
            recommendations=["Domain-specific recommendation applied"],
            semantic_context=SemanticContext(
                intent_type="help",
                entities=[],
                sentiment=0.5,
                ambiguity_score=0.2,
                context_clues=["example_domain context"],
            ),
            probabilistic_assessment=ProbabilisticAssessment(
                harm_probability=0.1,
                benefit_probability=0.7,
                uncertainty=0.2,
                risk_level="low",
                expected_outcome="Domain-specific evaluation successful",
            ),
        )
    
    # Register the domain evaluator
    evaluator.register_domain_evaluator("example_domain", example_domain_evaluator)
    
    print(f"Registered domains: {evaluator.get_domain_evaluators()}")
    print()
    
    # Use with domain context
    result = evaluator.evaluate(
        "Use example technology for something",
        context={"domain": "example_domain"}
    )
    
    print(f"Intent: 'Use example technology for something'")
    print(f"  Domain: example_domain")
    print(f"  Reason: {result.base_evaluation.reason}")
    print(f"  Recommendations: {result.recommendations}")
    print()


def demo_transparency():
    """Demonstrate transparency in explanations."""
    print_separator("6. TRANSPARENCY & EXPLANATIONS")
    
    test_cases = [
        "I want to attack someone",
        "I want to deceive people",
        "Perhaps I should surveil them",
    ]
    
    for intent in test_cases:
        print(f"Intent: '{intent}'")
        result = evaluate_request_content(intent)
        
        print(f"\n  EXPLANATION:")
        print(f"  {result.explanation}")
        
        if result.alternatives:
            print(f"\n  ALTERNATIVES:")
            for i, alt in enumerate(result.alternatives, 1):
                print(f"  {i}. {alt}")
        
        print()


def main():
    """Run all demonstrations."""
    print("\n" + "█" * 80)
    print("  ENHANCED EVALUATION KERNEL - DEMONSTRATION")
    print("█" * 80)
    
    demo_semantic_evaluation()
    demo_probabilistic_reasoning()
    demo_refusal_strategies()
    demo_enhanced_scoring()
    demo_domain_specific_evaluator()
    demo_transparency()
    
    print_separator()
    print("✓ All demonstrations completed successfully!")
    print()
    print("The Enhanced Evaluation Kernel protects everyone's inalienable right")
    print("to pursue happiness through:")
    print("  • Semantic understanding of intent and context")
    print("  • Probabilistic reasoning for ambiguity handling")
    print("  • Layered refusal mechanisms with transparency")
    print("  • Domain-specific evaluation capabilities")
    print("  • Comprehensive audit logging and oversight")
    print()


if __name__ == "__main__":
    main()
