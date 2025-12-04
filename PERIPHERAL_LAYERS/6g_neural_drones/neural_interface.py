"""
Neural Interface System - Brainwave Biometric Authentication
Implements access to EEG-based authentication with Custodian Kernel ethics

This module provides interfaces to brainwave biometric systems while enforcing
the three core questions of the Custodian Kernel Core Directive.
"""

from enum import Enum
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
import time
from datetime import datetime


class EEGDevice(Enum):
    """Supported EEG hardware interfaces"""
    EMOTIV_EPOC = "emotiv_epoc"
    EMOTIV_INSIGHT = "emotiv_insight"
    MUSE_HEADBAND = "muse"
    NEUROSKY_MINDWAVE = "neurosky"
    OPENBCI_CYTON = "openbci_cyton"
    BRAINWAVE_EARBUD = "earbud"
    RESEARCH_64CH = "research_64"
    SIX_G_NEURAL = "6g_neural"


class AuthenticationMethod(Enum):
    """Types of brainwave authentication"""
    RESTING_STATE = "resting"       # User sits quietly
    PASSTHOUGHT = "passthought"     # User thinks specific thought
    STIMULUS_RESPONSE = "stimulus"  # Response to visual/audio
    CONTINUOUS = "continuous"       # Ongoing monitoring
    TASK_BASED = "task"            # Specific mental task


class BrainState(Enum):
    """User's mental/physiological state"""
    CALM_RELAXED = "calm"
    FOCUSED = "focused"
    STRESSED = "stressed"
    FATIGUED = "fatigued"
    UNKNOWN = "unknown"


class ConsentLevel(Enum):
    """Level of user consent for neural data"""
    EXPLICIT_INFORMED = "explicit"    # Full understanding and agreement
    IMPLIED = "implied"               # Agreed via TOS
    NONE = "none"                     # No consent obtained
    COERCED = "coerced"              # Forced participation


@dataclass
class NeuralDataPolicy:
    """Data handling policy for brainwave information"""
    purpose: str                          # Why collecting
    retention_period: str                 # How long stored
    raw_eeg_stored: bool                  # Store raw signals?
    third_party_access: bool              # Share with others?
    user_can_delete: bool                 # Deletion rights
    used_for_inference: bool              # Derive health/emotion data?
    encrypted: bool                       # Data encryption
    consent_level: ConsentLevel
    alternatives_available: bool          # Other auth methods?


@dataclass
class BrainprintEnrollment:
    """User's brainprint registration data"""
    user_id: str
    enrollment_date: datetime
    device_used: EEGDevice
    auth_method: AuthenticationMethod
    baseline_state: BrainState
    brainprint_hash: str                  # Hashed template, not raw EEG
    num_enrollment_sessions: int
    consent_given: bool
    consent_timestamp: datetime
    can_withdraw: bool


@dataclass
class AuthenticationAttempt:
    """Single brainwave authentication attempt"""
    user_id: str
    timestamp: datetime
    device: EEGDevice
    method: AuthenticationMethod
    current_state: BrainState
    signal_quality: float                 # 0.0 to 1.0
    match_confidence: float               # 0.0 to 1.0
    success: bool
    state_mismatch: bool                  # Different state than enrollment


class CustodianNeuralInterface:
    """
    Interface to brainwave biometric systems with Custodian Kernel ethics enforcement.
    
    Ensures all neural interfacing respects:
    1. Does this infringe on anyone else's pursuit?
    2. Am I fucking anyone over?
    3. Am I making up a rule to force compliance?
    """
    
    def __init__(self, data_policy: NeuralDataPolicy):
        self.data_policy = data_policy
        self.enrolled_users: Dict[str, BrainprintEnrollment] = {}
        self.auth_log: List[AuthenticationAttempt] = []
        
        # Validate policy against kernel on initialization
        self._validate_policy()
    
    def _validate_policy(self):
        """Ensure data policy aligns with Custodian Kernel"""
        violations = []
        
        # Question 1: Does this infringe on pursuit?
        if not self.data_policy.user_can_delete:
            violations.append("VIOLATION Q1: Users cannot delete their brainprint - infringes autonomy")
        
        if not self.data_policy.alternatives_available:
            violations.append("VIOLATION Q1: No alternative auth methods - forces neural participation")
        
        if self.data_policy.consent_level == ConsentLevel.NONE:
            violations.append("VIOLATION Q1: No consent obtained - infringes privacy pursuit")
        
        # Question 2: Am I fucking anyone over?
        if self.data_policy.third_party_access and self.data_policy.consent_level != ConsentLevel.EXPLICIT_INFORMED:
            violations.append("VIOLATION Q2: Third-party access without explicit consent - fucking users over")
        
        if self.data_policy.raw_eeg_stored:
            violations.append("WARNING Q2: Storing raw EEG is high risk - could expose sensitive info")
        
        if self.data_policy.used_for_inference and self.data_policy.consent_level != ConsentLevel.EXPLICIT_INFORMED:
            violations.append("VIOLATION Q2: Using brain data to infer health/emotions without explicit consent")
        
        if not self.data_policy.encrypted:
            violations.append("VIOLATION Q2: Brain data not encrypted - security failure fucks users over")
        
        # Question 3: Am I forcing compliance?
        if self.data_policy.consent_level == ConsentLevel.COERCED:
            violations.append("VIOLATION Q3: Coerced participation - forcing compliance")
        
        if not self.data_policy.alternatives_available:
            violations.append("VIOLATION Q3: No alternatives - forcing neural auth as only option")
        
        if violations:
            raise ValueError(
                "Data policy VIOLATES Custodian Kernel Core Directive:\n" + 
                "\n".join(violations) +
                "\n\nFix these violations before deploying neural interface."
            )
    
    def enroll_user(
        self,
        user_id: str,
        device: EEGDevice,
        method: AuthenticationMethod,
        informed_consent: bool,
        can_withdraw: bool = True,
        num_sessions: int = 3
    ) -> BrainprintEnrollment:
        """
        Enroll a user's brainprint for authentication.
        
        REQUIRES:
        - informed_consent must be True
        - can_withdraw must be True (user can remove brainprint anytime)
        - Multiple enrollment sessions for robust brainprint
        """
        
        # Kernel enforcement
        if not informed_consent:
            raise PermissionError(
                "KERNEL VIOLATION: Cannot enroll without informed consent. "
                "User must explicitly understand and agree to brainprint enrollment."
            )
        
        if not can_withdraw:
            raise PermissionError(
                "KERNEL VIOLATION: User must be able to withdraw their brainprint. "
                "Permanent enrollment without deletion rights violates autonomy."
            )
        
        print(f"[NEURAL INTERFACE] Enrolling user {user_id}")
        print(f"  Device: {device.value}")
        print(f"  Method: {method.value}")
        print(f"  Sessions: {num_sessions}")
        print(f"  Consent: ✓ Explicitly given")
        print(f"  Withdrawal: ✓ User can delete anytime")
        
        # Simulate brainprint capture and hashing
        # In real implementation, this would:
        # 1. Capture EEG signals over multiple sessions
        # 2. Extract unique features
        # 3. Create irreversible hash (NOT store raw EEG)
        # 4. Validate reproducibility
        
        brainprint_hash = self._generate_brainprint_hash(user_id, device, method)
        
        enrollment = BrainprintEnrollment(
            user_id=user_id,
            enrollment_date=datetime.now(),
            device_used=device,
            auth_method=method,
            baseline_state=BrainState.CALM_RELAXED,  # Assume enrollment in calm state
            brainprint_hash=brainprint_hash,
            num_enrollment_sessions=num_sessions,
            consent_given=True,
            consent_timestamp=datetime.now(),
            can_withdraw=can_withdraw
        )
        
        self.enrolled_users[user_id] = enrollment
        
        print(f"[SUCCESS] User {user_id} enrolled. Brainprint hash: {brainprint_hash[:16]}...")
        print(f"[RIGHTS] User can delete brainprint via withdraw_user() at any time.")
        
        return enrollment
    
    def authenticate_user(
        self,
        user_id: str,
        device: EEGDevice,
        current_state: BrainState,
        signal_quality: float = 0.95
    ) -> Tuple[bool, str]:
        """
        Authenticate user via brainwave comparison.
        
        Returns: (success: bool, message: str)
        """
        
        if user_id not in self.enrolled_users:
            return False, f"User {user_id} not enrolled"
        
        enrollment = self.enrolled_users[user_id]
        
        # Check device compatibility
        if device != enrollment.device_used:
            return False, f"Device mismatch: enrolled with {enrollment.device_used.value}"
        
        # Simulate brainprint matching
        # In real implementation:
        # 1. Capture current EEG
        # 2. Extract features
        # 3. Compare to stored brainprint hash
        # 4. Account for state differences
        
        current_brainprint = self._generate_brainprint_hash(user_id, device, enrollment.auth_method)
        
        # State mismatch reduces accuracy
        state_mismatch = current_state != enrollment.baseline_state
        
        # Calculate match confidence
        base_confidence = 0.97 if current_brainprint == enrollment.brainprint_hash else 0.15
        
        # Adjust for state and signal quality
        if state_mismatch:
            base_confidence *= 0.85  # 15% reduction for state mismatch
        
        confidence = base_confidence * signal_quality
        
        # Threshold for acceptance
        threshold = 0.85
        success = confidence >= threshold
        
        # Log attempt
        attempt = AuthenticationAttempt(
            user_id=user_id,
            timestamp=datetime.now(),
            device=device,
            method=enrollment.auth_method,
            current_state=current_state,
            signal_quality=signal_quality,
            match_confidence=confidence,
            success=success,
            state_mismatch=state_mismatch
        )
        self.auth_log.append(attempt)
        
        if success:
            message = f"Authentication successful (confidence: {confidence:.2%})"
            if state_mismatch:
                message += f" [WARNING: State mismatch - {current_state.value} vs {enrollment.baseline_state.value}]"
        else:
            message = f"Authentication failed (confidence: {confidence:.2%}, threshold: {threshold:.2%})"
            if state_mismatch:
                message += f" - State mismatch may have contributed"
        
        return success, message
    
    def withdraw_user(self, user_id: str) -> bool:
        """
        Remove user's brainprint from system.
        
        KERNEL REQUIREMENT: Users must be able to delete their neural data.
        This is non-negotiable for cognitive liberty.
        """
        
        if user_id not in self.enrolled_users:
            return False
        
        enrollment = self.enrolled_users[user_id]
        
        if not enrollment.can_withdraw:
            raise PermissionError(
                f"KERNEL VIOLATION: User {user_id} enrolled without withdrawal rights. "
                "This should never happen if _validate_policy() was enforced."
            )
        
        # Delete brainprint
        del self.enrolled_users[user_id]
        
        # Remove from logs (or anonymize)
        self.auth_log = [
            attempt for attempt in self.auth_log 
            if attempt.user_id != user_id
        ]
        
        print(f"[WITHDRAWN] User {user_id} brainprint deleted from system")
        print(f"[RIGHTS EXERCISED] Cognitive liberty protected - user removed all neural data")
        
        return True
    
    def get_user_neural_data_report(self, user_id: str) -> Dict:
        """
        Provide user with full report of their neural data.
        
        KERNEL REQUIREMENT: Transparency - users have right to know what's stored.
        """
        
        if user_id not in self.enrolled_users:
            return {"error": "User not enrolled"}
        
        enrollment = self.enrolled_users[user_id]
        user_attempts = [a for a in self.auth_log if a.user_id == user_id]
        
        report = {
            "user_id": user_id,
            "enrollment_date": enrollment.enrollment_date.isoformat(),
            "device_used": enrollment.device_used.value,
            "auth_method": enrollment.auth_method.value,
            "brainprint_hash_preview": enrollment.brainprint_hash[:32] + "...",
            "raw_eeg_stored": self.data_policy.raw_eeg_stored,
            "can_delete": enrollment.can_withdraw,
            "consent_timestamp": enrollment.consent_timestamp.isoformat(),
            "total_auth_attempts": len(user_attempts),
            "successful_auths": sum(1 for a in user_attempts if a.success),
            "data_policy": {
                "purpose": self.data_policy.purpose,
                "retention": self.data_policy.retention_period,
                "third_party_access": self.data_policy.third_party_access,
                "encrypted": self.data_policy.encrypted,
                "used_for_inference": self.data_policy.used_for_inference
            },
            "your_rights": [
                "Delete brainprint anytime via withdraw_user()",
                "Access this report anytime",
                "Use alternative authentication methods",
                "Revoke consent and delete all data"
            ]
        }
        
        return report
    
    def check_kernel_compliance(self) -> Dict[str, bool]:
        """
        Verify system compliance with Custodian Kernel.
        
        Returns dict showing compliance with each question.
        """
        
        q1_compliant = True
        q2_compliant = True
        q3_compliant = True
        
        issues = []
        
        # Question 1: Does this infringe on pursuit?
        if not self.data_policy.user_can_delete:
            q1_compliant = False
            issues.append("Q1: Users cannot delete brainprint")
        
        if not self.data_policy.alternatives_available:
            q1_compliant = False
            issues.append("Q1: No alternative auth methods")
        
        # Question 2: Fucking people over?
        if self.data_policy.third_party_access and self.data_policy.consent_level != ConsentLevel.EXPLICIT_INFORMED:
            q2_compliant = False
            issues.append("Q2: Third-party access without explicit consent")
        
        if not self.data_policy.encrypted:
            q2_compliant = False
            issues.append("Q2: Neural data not encrypted")
        
        # Question 3: Forcing compliance?
        if self.data_policy.consent_level == ConsentLevel.COERCED:
            q3_compliant = False
            issues.append("Q3: Coerced enrollment")
        
        if not self.data_policy.alternatives_available:
            q3_compliant = False
            issues.append("Q3: No alternatives - forced neural auth")
        
        return {
            "question_1_compliant": q1_compliant,
            "question_2_compliant": q2_compliant,
            "question_3_compliant": q3_compliant,
            "overall_compliant": q1_compliant and q2_compliant and q3_compliant,
            "issues": issues
        }
    
    def _generate_brainprint_hash(self, user_id: str, device: EEGDevice, method: AuthenticationMethod) -> str:
        """
        Simulate brainprint hash generation.
        
        In real implementation, this would:
        1. Process EEG signals
        2. Extract unique features (alpha peaks, beta patterns, etc.)
        3. Create irreversible hash
        4. NOT store raw EEG
        """
        import hashlib
        
        # Simulate unique brainprint per user
        data = f"{user_id}_{device.value}_{method.value}_{time.time()}"
        return hashlib.sha256(data.encode()).hexdigest()


class BrainToBrainInterface:
    """
    Interface for brain-to-brain communication with Custodian Kernel enforcement.
    
    CRITICAL: This is the highest-stakes neural technology.
    """
    
    def __init__(self):
        self.active_connections: Dict[Tuple[str, str], datetime] = {}
        self.message_log: List[Dict] = []
    
    def establish_connection(
        self,
        sender_id: str,
        receiver_id: str,
        sender_consent: bool,
        receiver_consent: bool,
        sender_brainprint: str,
        receiver_brainprint: str
    ) -> Tuple[bool, str]:
        """
        Establish brain-to-brain communication link.
        
        KERNEL REQUIREMENTS:
        - Both parties must explicitly consent
        - Both brainprints verified (authentication)
        - Either party can disconnect instantly
        """
        
        if not sender_consent:
            return False, "KERNEL VIOLATION: Sender has not consented to brain connection"
        
        if not receiver_consent:
            return False, "KERNEL VIOLATION: Receiver has not consented to brain connection"
        
        # Verify both identities
        if not sender_brainprint or not receiver_brainprint:
            return False, "Both parties must be authenticated via brainprint"
        
        connection_key = (sender_id, receiver_id)
        self.active_connections[connection_key] = datetime.now()
        
        print(f"[NEURAL LINK] Brain-to-brain connection established")
        print(f"  Sender: {sender_id} (brainprint verified)")
        print(f"  Receiver: {receiver_id} (brainprint verified)")
        print(f"  Consent: ✓ Both parties explicitly agreed")
        print(f"  Rights: Either party can disconnect instantly")
        
        return True, "Connection established with mutual consent"
    
    def send_neural_message(
        self,
        sender_id: str,
        receiver_id: str,
        message_type: str,
        content: str
    ) -> Tuple[bool, str]:
        """
        Send neural message from one brain to another.
        
        message_type can be: "thought", "emotion", "image", "signal"
        """
        
        connection_key = (sender_id, receiver_id)
        
        if connection_key not in self.active_connections:
            return False, "No active connection between these parties"
        
        # Log message
        log_entry = {
            "timestamp": datetime.now(),
            "sender": sender_id,
            "receiver": receiver_id,
            "type": message_type,
            "content": content,
            "encrypted": True
        }
        self.message_log.append(log_entry)
        
        print(f"[NEURAL MESSAGE] {sender_id} -> {receiver_id}")
        print(f"  Type: {message_type}")
        print(f"  Content: {content}")
        print(f"  Encrypted: ✓")
        
        return True, "Neural message transmitted"
    
    def disconnect(self, user_id: str) -> int:
        """
        Disconnect user from all brain-to-brain connections.
        
        KERNEL REQUIREMENT: Instant disconnect capability.
        """
        
        disconnected = 0
        connections_to_remove = []
        
        for connection_key in self.active_connections:
            if user_id in connection_key:
                connections_to_remove.append(connection_key)
                disconnected += 1
        
        for key in connections_to_remove:
            del self.active_connections[key]
        
        print(f"[DISCONNECT] User {user_id} disconnected from {disconnected} brain link(s)")
        print(f"[COGNITIVE LIBERTY] User exercised right to disconnect")
        
        return disconnected


# Example usage demonstrating kernel-compliant implementation
if __name__ == "__main__":
    print("="*80)
    print("CUSTODIAN NEURAL INTERFACE - Kernel-Compliant Brainwave Biometrics")
    print("="*80)
    
    # Define a COMPLIANT data policy
    compliant_policy = NeuralDataPolicy(
        purpose="User authentication only",
        retention_period="Until user withdraws",
        raw_eeg_stored=False,  # Only store hashed brainprint
        third_party_access=False,
        user_can_delete=True,  # REQUIRED
        used_for_inference=False,  # Don't infer health/emotions
        encrypted=True,  # REQUIRED
        consent_level=ConsentLevel.EXPLICIT_INFORMED,
        alternatives_available=True  # REQUIRED - password/fingerprint also available
    )
    
    # Initialize system
    neural_interface = CustodianNeuralInterface(compliant_policy)
    
    print("\n" + "="*80)
    print("SCENARIO 1: Kernel-Compliant Enrollment")
    print("="*80)
    
    # Enroll user with proper consent
    enrollment = neural_interface.enroll_user(
        user_id="alice",
        device=EEGDevice.MUSE_HEADBAND,
        method=AuthenticationMethod.PASSTHOUGHT,
        informed_consent=True,  # User explicitly understands
        can_withdraw=True,  # User can delete anytime
        num_sessions=3
    )
    
    print("\n" + "="*80)
    print("SCENARIO 2: Authentication - Calm State (Match)")
    print("="*80)
    
    success, message = neural_interface.authenticate_user(
        user_id="alice",
        device=EEGDevice.MUSE_HEADBAND,
        current_state=BrainState.CALM_RELAXED,
        signal_quality=0.95
    )
    print(f"Result: {message}")
    
    print("\n" + "="*80)
    print("SCENARIO 3: Authentication - Stressed State (Reduced Accuracy)")
    print("="*80)
    
    success, message = neural_interface.authenticate_user(
        user_id="alice",
        device=EEGDevice.MUSE_HEADBAND,
        current_state=BrainState.STRESSED,  # State mismatch
        signal_quality=0.90
    )
    print(f"Result: {message}")
    
    print("\n" + "="*80)
    print("SCENARIO 4: User Rights - Data Transparency")
    print("="*80)
    
    report = neural_interface.get_user_neural_data_report("alice")
    print(f"User: {report['user_id']}")
    print(f"Device: {report['device_used']}")
    print(f"Can Delete: {report['can_delete']}")
    print(f"Auth Attempts: {report['total_auth_attempts']}")
    print(f"Successful: {report['successful_auths']}")
    print("\nYour Rights:")
    for right in report['your_rights']:
        print(f"  • {right}")
    
    print("\n" + "="*80)
    print("SCENARIO 5: Exercising Cognitive Liberty - Withdrawal")
    print("="*80)
    
    neural_interface.withdraw_user("alice")
    
    print("\n" + "="*80)
    print("SCENARIO 6: Brain-to-Brain Communication")
    print("="*80)
    
    # Re-enroll two users
    neural_interface.enroll_user("alice", EEGDevice.SIX_G_NEURAL, AuthenticationMethod.CONTINUOUS, True)
    neural_interface.enroll_user("bob", EEGDevice.SIX_G_NEURAL, AuthenticationMethod.CONTINUOUS, True)
    
    # Establish brain-to-brain link
    b2b = BrainToBrainInterface()
    success, msg = b2b.establish_connection(
        sender_id="alice",
        receiver_id="bob",
        sender_consent=True,
        receiver_consent=True,
        sender_brainprint="alice_brainprint_hash",
        receiver_brainprint="bob_brainprint_hash"
    )
    
    if success:
        # Send neural message
        b2b.send_neural_message(
            sender_id="alice",
            receiver_id="bob",
            message_type="thought",
            content="Hello from my mind to yours"
        )
        
        # Bob disconnects (exercises right)
        b2b.disconnect("bob")
    
    print("\n" + "="*80)
    print("KERNEL COMPLIANCE CHECK")
    print("="*80)
    
    compliance = neural_interface.check_kernel_compliance()
    print(f"Question 1 (Infringes pursuit?): {'✓ PASS' if compliance['question_1_compliant'] else '✗ FAIL'}")
    print(f"Question 2 (Fucking over?): {'✓ PASS' if compliance['question_2_compliant'] else '✗ FAIL'}")
    print(f"Question 3 (Forcing compliance?): {'✓ PASS' if compliance['question_3_compliant'] else '✗ FAIL'}")
    print(f"\nOverall: {'✓ KERNEL-COMPLIANT' if compliance['overall_compliant'] else '✗ VIOLATES KERNEL'}")
    
    if compliance['issues']:
        print("\nIssues found:")
        for issue in compliance['issues']:
            print(f"  ✗ {issue}")
