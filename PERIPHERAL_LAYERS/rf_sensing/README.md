# RF Sensing & Surveillance Technology

## Peripheral Layer: Wireless Sensing Technologies

This peripheral layer applies the **Custodian Kernel Core Directive** to RF sensing, wireless surveillance, and related technologies.

## The Core Kernel Applied

Every person has an equal, inalienable right to pursue happiness.

**The Three Questions for RF Sensing:**
1. Does this sensing infringe on anyone else's pursuit?
2. Am I fucking anyone over by monitoring them?
3. Am I making up a rule to force people into surveillance?

## Contents

- **[TECHNICAL_OVERVIEW.md](TECHNICAL_OVERVIEW.md)** - Technical capabilities of RF sensing
- **[rf_ethics.py](rf_ethics.py)** - Implementation framework for evaluating RF scenarios
- **[USE_CASES.md](USE_CASES.md)** - Evaluation of specific use cases

## Technology Overview

Wireless signals (Wi-Fi, 5G/6G, radar, terahertz) can:
- Detect presence through walls
- Monitor breathing and heartbeat remotely
- Track movements and gestures
- Potentially sense biological signals
- Map human poses behind obstacles

## Kernel Evaluation

### Question 1: Does this infringe on anyone else's pursuit?

**YES** if:
- People are monitored without being informed
- They cannot opt out of monitoring
- Their privacy pursuit is crushed by invisible surveillance
- Data is shared without explicit consent

**NO** if:
- Informed consent is obtained
- People can easily opt out
- Monitoring is limited to the consented scope
- Data is protected and controlled by the subject

### Question 2: Am I fucking anyone over?

**YES** if:
- Covert surveillance without consent
- Commercial exploitation of monitoring data
- Indefinite data retention without permission
- Third-party access without explicit consent
- Using monitoring to control or manipulate

**NO** if:
- Transparent about monitoring
- Limited purpose with clear benefits
- Data minimization and deletion
- User controls their own data
- Voluntary participation

### Question 3: Am I making up a rule to force compliance?

**YES** if:
- Mandatory monitoring with no opt-out
- Access to services requires surveillance
- Participation forced through policy
- "Accept surveillance or lose access"

**NO** if:
- Monitoring is optional
- Alternatives exist without surveillance
- People can choose freely
- No penalties for opting out

## Use Cases Evaluated

### ✓ UPHOLDS the Kernel

**Emergency Rescue**
- Through-wall radar to find survivors
- Medical monitoring with informed consent
- Fall detection for elderly (with permission)
- Baby monitors for SIDS prevention (parent's choice)

**Key**: Protects pursuit of life and health, consent when possible

### ✗ VIOLATES the Kernel

**Covert Surveillance**
- Retail tracking without disclosure
- Law enforcement scans without warrants
- Smart home mandatory monitoring
- Commercial data harvesting

**Key**: Crushes pursuit through invisible control and non-consensual monitoring

### ⚠️ QUESTIONABLE - Needs Safeguards

**Research & Development**
- Must have informed consent protocols
- Data anonymization required
- Clear deletion policies
- Transparent about capabilities

## Implementation

See `rf_ethics.py` for code that evaluates RF sensing scenarios against the kernel.

```python
from rf_ethics import CustodianRFEthics, SensingScenario

ethics = CustodianRFEthics()
scenario = SensingScenario(...)
evaluation = ethics.evaluate(scenario)
```

## Safeguards Required

To align RF sensing with the kernel:

1. **Transparency**: Inform people they're being monitored
2. **Consent**: Obtain explicit permission
3. **Opt-out**: Provide easy ways to refuse
4. **Minimization**: Collect only necessary data
5. **Deletion**: Remove data after purpose is fulfilled
6. **Access Control**: User controls who sees their data
7. **Purpose Limits**: Use data only for stated purpose
8. **No Coercion**: Don't force participation

## The Principle

**Technology is neutral. Implementation determines whether it upholds or violates the inalienable right.**

RF sensing can:
- Save lives (rescue, medical alerts)
- Protect safety (fall detection, health monitoring)
- Enhance convenience (smart homes with consent)

OR it can:
- Violate privacy (covert surveillance)
- Enable control (mandatory monitoring)
- Crush autonomy (invisible tracking)

**The kernel determines which path is taken.**

## Future Developments

As RF sensing advances toward brainwave detection and cognitive monitoring:

- **The kernel still applies** - Same three questions
- **Higher stakes** - Cognitive liberty is fundamental to pursuit
- **Stricter safeguards** - Brain data requires strongest protections
- **Absolute consent** - No exceptions for covert brain monitoring

---

*This peripheral layer serves the kernel. The kernel judges all implementations.*
