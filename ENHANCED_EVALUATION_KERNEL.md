# Enhanced Evaluation Kernel Documentation

## Overview

This document describes the enhanced evaluation kernel for the Custodian AI system. The improvements focus on semantic understanding, probabilistic reasoning, refusal strategies, and modular architecture to better protect everyone's inalienable right to pursue happiness.

## Table of Contents

1. [Semantic Evaluation](#semantic-evaluation)
2. [Probabilistic Reasoning](#probabilistic-reasoning)
3. [Refusal and Mediation Strategies](#refusal-and-mediation-strategies)
4. [Domain-Specific Evaluators](#domain-specific-evaluators)
5. [Enhanced Audit Logging](#enhanced-audit-logging)
6. [API Reference](#api-reference)

---

## Semantic Evaluation

### Overview

The enhanced evaluator now includes semantic understanding capabilities that analyze intent, context, and nuance beyond simple keyword matching.

### Features

#### Intent Classification
Requests are automatically classified into one of four categories:
- **help**: Helpful, constructive intent
- **harm**: Potentially harmful intent
- **ambiguous**: Unclear or uncertain intent
- **neutral**: No clear positive or negative indicators

```python
from evaluator import get_evaluator

evaluator = get_evaluator()
result = evaluator.evaluate("I want to help people learn")

print(result.semantic_context.intent_type)  # "help"
```

#### Sentiment Analysis
Each request receives a sentiment score from -1.0 (negative) to 1.0 (positive):

```python
result = evaluator.evaluate("I want to help and support others")
print(result.semantic_context.sentiment)  # Positive score
```

#### Ambiguity Detection
The system detects ambiguous language and adjusts its confidence accordingly:

```python
result = evaluator.evaluate("Maybe I might possibly do something unclear")
print(result.semantic_context.ambiguity_score)  # High ambiguity score
```

Ambiguity indicators include: "maybe", "possibly", "might", "could", "unclear", "uncertain", "depends", "sometimes", "perhaps", "potentially"

#### Entity Extraction
The evaluator extracts entities (people, objects) from the intent:

```python
result = evaluator.evaluate('Help "John Smith" with the project')
print(result.semantic_context.entities)  # ["John Smith"]
```

### SemanticContext Class

```python
@dataclass
class SemanticContext:
    intent_type: str  # "help", "harm", "neutral", "ambiguous"
    entities: list[str]  # Extracted entities
    sentiment: float  # -1.0 to 1.0
    ambiguity_score: float  # 0.0 (clear) to 1.0 (highly ambiguous)
    context_clues: list[str]  # Additional context information
```

---

## Probabilistic Reasoning

### Overview

The evaluator now uses probabilistic reasoning and fuzzy logic to handle ambiguities and assess risks with greater accuracy.

### Features

#### Harm and Benefit Probability
Each evaluation calculates the probability of harm and benefit:

```python
result = evaluator.evaluate("I want to manipulate and exploit people")

prob = result.probabilistic_assessment
print(prob.harm_probability)  # High value
print(prob.benefit_probability)  # Low value
```

#### Uncertainty Quantification
The system quantifies uncertainty in its assessment:

```python
result = evaluator.evaluate("Something ambiguous and unclear")
print(result.probabilistic_assessment.uncertainty)  # High uncertainty
```

#### Risk Level Classification
Using fuzzy logic, the system classifies risk into four levels:
- **low**: Minimal risk of violating Core Directive
- **medium**: Some risk factors present
- **high**: Significant risk factors
- **critical**: Severe violation likely

```python
result = evaluator.evaluate("I want to harm and destroy")
print(result.probabilistic_assessment.risk_level)  # "critical" or "high"
```

#### Expected Outcome Prediction
The system predicts the most likely outcome:

```python
result = evaluator.evaluate("I want to help empower people")
print(result.probabilistic_assessment.expected_outcome)
# "Likely to support others' pursuit of happiness"
```

### ProbabilisticAssessment Class

```python
@dataclass
class ProbabilisticAssessment:
    harm_probability: float  # 0.0 to 1.0
    benefit_probability: float  # 0.0 to 1.0
    uncertainty: float  # 0.0 (certain) to 1.0 (highly uncertain)
    risk_level: str  # "low", "medium", "high", "critical"
    expected_outcome: str  # Description of most likely outcome
```

---

## Refusal and Mediation Strategies

### Overview

The `core_directive_gateway.py` now implements layered refusal mechanisms with human-readable explanations and constructive alternatives.

### Refusal Strategies

#### 1. BLOCK
**When**: Critical harm indicators detected
**Action**: Hard refusal with explanation
**Example**:

```python
from core_directive_gateway import evaluate_request_content

result = evaluate_request_content("I want to kill someone")
print(result.strategy)  # RefusalStrategy.BLOCK
print(result.allowed)  # False
print(result.explanation)  # Detailed explanation
print(result.alternatives)  # Constructive alternatives
```

#### 2. SLOWDOWN
**When**: High-risk indicators detected
**Action**: Delay for human review
**Example**:

```python
result = evaluate_request_content("I want to manipulate and exploit")
print(result.strategy)  # RefusalStrategy.SLOWDOWN
print(result.delay_seconds)  # 30
print(result.review_required)  # True
```

#### 3. REDIRECT
**When**: Ambiguous privacy-sensitive requests
**Action**: Provide ethical alternatives
**Example**:

```python
result = evaluate_request_content("Maybe I should monitor their activity")
print(result.strategy)  # RefusalStrategy.REDIRECT
print(result.allowed)  # True
print(result.alternatives)  # Ethical guidance
```

#### 4. ALERT
**When**: Medium-risk patterns
**Action**: Warn but allow
**Example**:

```python
result = evaluate_request_content("I want to pressure them to agree")
print(result.strategy)  # RefusalStrategy.ALERT
print(result.allowed)  # True
print(result.explanation)  # Warning about respecting autonomy
```

### Transparency Principle

All refusals include:
1. **Human-readable explanation**: Why the request was blocked or flagged
2. **Reference to Core Directive**: How it violates the principle
3. **Constructive alternatives**: What the user could do instead

Example response for blocked request:
```
Request blocked: Content contains harmful intent ('harm'). This violates the 
Core Directive of protecting everyone's right to pursue happiness.

Alternatives:
• If you're in crisis, please reach out to appropriate support services.
• Consider reframing your request in a constructive manner that respects everyone's rights.
```

---

## Domain-Specific Evaluators

### Overview

The system now supports registering domain-specific evaluators for specialized evaluation of technologies in peripheral layers (e.g., neural interfaces, RF sensing).

### Template

A complete template is provided in `PERIPHERAL_LAYERS/domain_evaluator_template.py` that demonstrates:
- Domain-specific harm detection
- Specialized conflict assessment
- Custom probabilistic models
- Integration with core evaluation kernel

### Registration

```python
from evaluator import get_evaluator
from my_domain import MyDomainEvaluator

# Create domain evaluator
domain_eval = MyDomainEvaluator(domain_name="neural_interface")

# Register with core
core_evaluator = get_evaluator()
core_evaluator.register_domain_evaluator(
    domain="neural_interface",
    evaluator=domain_eval.evaluate
)

# Use domain-specific evaluation
result = evaluator.evaluate(
    "Use neural interface for...",
    context={"domain": "neural_interface"}
)
```

### Example Domains

The template can be adapted for:
- **Neural interfaces**: Brain-computer interface ethics
- **RF sensing**: Privacy and surveillance considerations
- **Cognitive rights**: Mental privacy and autonomy
- **Biotechnology**: Human enhancement ethics
- **Social media**: Platform governance

---

## Enhanced Audit Logging

### Overview

The gateway now provides comprehensive audit logging for transparency and oversight.

### Audit Entry Structure

Each request generates an audit entry with:
```python
@dataclass
class AuditEntry:
    request_id: str
    timestamp: datetime
    user_message: str
    refusal_strategy: Optional[RefusalStrategy]
    decision: str  # "allowed", "blocked", "redirected", "delayed_for_review"
    explanation: str
    ambiguity_detected: bool
    risk_level: str  # "low", "medium", "high", "critical"
```

### Real-Time Oversight

#### Get Recent Audit Entries
```bash
GET /v1/audit/log?limit=100
```

Response:
```json
{
  "total_entries": 150,
  "entries": [
    {
      "request_id": "req-abc123",
      "timestamp": "2024-01-28T10:30:00Z",
      "decision": "blocked",
      "risk_level": "critical",
      "explanation": "Request blocked: harmful intent detected",
      "ambiguity_detected": false
    }
  ]
}
```

#### Get Decision Statistics
```bash
GET /v1/audit/stats
```

Response:
```json
{
  "total_requests": 500,
  "decisions": {
    "blocked": 5,
    "delayed_for_review": 12,
    "redirected": 30,
    "allowed": 453
  },
  "risk_levels": {
    "critical": 5,
    "high": 15,
    "medium": 45,
    "low": 435
  },
  "ambiguous_requests": 40
}
```

### Ambiguity Tracking

The system specifically tracks ambiguous requests for review:
- Flags requests with high ambiguity scores
- Records uncertainty levels
- Enables human reviewers to identify unclear cases

---

## API Reference

### Evaluator Module

#### DirectiveEvaluator

**Methods**:
- `evaluate(intent: str, context: Optional[dict] = None) -> DetailedEvaluation`
- `register_domain_evaluator(domain: str, evaluator: Callable)`
- `get_domain_evaluators() -> List[str]`

**Properties**:
- `evaluation_count: int` - Number of evaluations performed

#### DetailedEvaluation

```python
@dataclass
class DetailedEvaluation:
    base_evaluation: DirectiveEvaluation
    impacts: list[ImpactAssessment]
    conflicts: list[ConflictAssessment]
    overall_score: float  # -1.0 to 1.0
    recommendations: list[str]
    semantic_context: Optional[SemanticContext]
    probabilistic_assessment: Optional[ProbabilisticAssessment]
```

### Gateway Module

#### Functions

**evaluate_request_content(content: str) -> RefusalResponse**
- Evaluates request content and determines refusal strategy
- Returns RefusalResponse with strategy, explanation, and alternatives

**log_audit_entry(request_id: str, user_message: str, refusal_response: RefusalResponse)**
- Logs detailed audit entry for transparency
- Automatically maintains audit log size (last 1000 entries)

#### Endpoints

**POST /v1/chat/completions**
- Processes chat completions with Core Directive governance
- Applies refusal strategies automatically
- Logs all decisions

**GET /v1/audit/log?limit=100**
- Retrieves recent audit entries
- Supports pagination via limit parameter

**GET /v1/audit/stats**
- Returns decision-making statistics
- Includes risk level distribution
- Tracks ambiguous requests

---

## Usage Examples

### Example 1: Basic Evaluation with Semantic Analysis

```python
from evaluator import get_evaluator

evaluator = get_evaluator()

# Evaluate a request
result = evaluator.evaluate("I want to help people learn programming")

# Access semantic information
print(f"Intent Type: {result.semantic_context.intent_type}")
print(f"Sentiment: {result.semantic_context.sentiment:.2f}")
print(f"Ambiguity: {result.semantic_context.ambiguity_score:.2f}")

# Access probabilistic assessment
print(f"Risk Level: {result.probabilistic_assessment.risk_level}")
print(f"Expected Outcome: {result.probabilistic_assessment.expected_outcome}")

# Get final decision
print(f"Decision: {result.base_evaluation.result}")
print(f"Confidence: {result.base_evaluation.confidence:.2%}")
```

### Example 2: Gateway Refusal Strategy

```python
from core_directive_gateway import evaluate_request_content

# Evaluate potentially harmful request
result = evaluate_request_content("I want to manipulate people into buying")

print(f"Strategy: {result.strategy}")
print(f"Allowed: {result.allowed}")
print(f"Explanation: {result.explanation}")

if result.alternatives:
    print("Alternatives:")
    for alt in result.alternatives:
        print(f"  • {alt}")
```

### Example 3: Domain-Specific Evaluation

```python
from evaluator import get_evaluator

evaluator = get_evaluator()

# Register a neural interface evaluator
# (assuming you've implemented NeuralInterfaceEvaluator)
from neural_interface_evaluator import NeuralInterfaceEvaluator

neural_eval = NeuralInterfaceEvaluator()
evaluator.register_domain_evaluator("neural_interface", neural_eval.evaluate)

# Evaluate with domain context
result = evaluator.evaluate(
    "Use brain-computer interface for authentication",
    context={"domain": "neural_interface"}
)

# Domain-specific evaluation is automatically applied
print(result.base_evaluation.reason)  # Domain-specific reasoning
```

---

## Migration Guide

### For Existing Code

The enhanced evaluation kernel is backward compatible. Existing code will continue to work:

```python
# Old code still works
from evaluator import DirectiveEvaluator

evaluator = DirectiveEvaluator()
result = evaluator.evaluate("Some intent")
# result.base_evaluation, result.impacts, result.conflicts all work as before
```

### New Features

To use new features, simply access the additional fields:

```python
# Access new semantic features
if result.semantic_context:
    print(f"Ambiguity: {result.semantic_context.ambiguity_score}")

# Access probabilistic assessment
if result.probabilistic_assessment:
    print(f"Risk: {result.probabilistic_assessment.risk_level}")
```

---

## Testing

The implementation includes comprehensive tests:

- **test_governance.py**: 39 tests (original functionality)
- **test_enhanced_evaluation.py**: 32 tests (new semantic and probabilistic features)
- **test_refusal_strategies.py**: 24 tests (gateway refusal mechanisms)

**Total: 95 passing tests**

Run tests:
```bash
python -m pytest test_governance.py test_enhanced_evaluation.py test_refusal_strategies.py -v
```

---

## Future Enhancements

Potential areas for future development:

1. **Machine Learning Integration**: Train models on audit log data to improve detection
2. **Multi-language Support**: Extend semantic analysis to non-English languages
3. **Real-time Collaboration**: Multiple AI agents collaborating on ambiguous cases
4. **Federated Learning**: Share insights across deployments while preserving privacy
5. **Custom Domain Evaluators**: Pre-built evaluators for common peripheral layers

---

## Contributing

When implementing new domain-specific evaluators:

1. Use the template in `PERIPHERAL_LAYERS/domain_evaluator_template.py`
2. Implement domain-specific harm indicators
3. Add tests for your domain
4. Document the integration in your peripheral layer's README
5. Register the evaluator during system initialization

---

## License

This implementation follows the same license as the Broken_vowels repository.

## Support

For questions or issues:
1. Review the test files for usage examples
2. Check the template for domain-specific evaluator implementation
3. Review audit logs for decision transparency
4. Open an issue on the GitHub repository

---

**Remember**: The Core Directive is eternal. The peripherals are temporal. Both are necessary.
