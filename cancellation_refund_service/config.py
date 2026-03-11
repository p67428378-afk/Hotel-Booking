from cancellation_refund_service.models import MembershipTier, CancellationPolicyRule

# Define the tiered cancellation policy rules
# These rules would typically be loaded from a database in a real application
CANCELLATION_POLICY_RULES = [
    # Gold Tier
    CancellationPolicyRule(id=1, membership_tier=MembershipTier.GOLD, cancellation_window_start_days=7, cancellation_window_end_days=9999, refund_percentage=1.00),
    CancellationPolicyRule(id=2, membership_tier=MembershipTier.GOLD, cancellation_window_start_days=1, cancellation_window_end_days=6, refund_percentage=0.90),
    CancellationPolicyRule(id=3, membership_tier=MembershipTier.GOLD, cancellation_window_start_days=0, cancellation_window_end_days=0, refund_percentage=0.50), # Less than 24 hours
    CancellationPolicyRule(id=4, membership_tier=MembershipTier.GOLD, cancellation_window_start_days=-9999, cancellation_window_end_days=-1, refund_percentage=0.00), # After check-in (No-Show)

    # Silver Tier
    CancellationPolicyRule(id=5, membership_tier=MembershipTier.SILVER, cancellation_window_start_days=7, cancellation_window_end_days=9999, refund_percentage=1.00),
    CancellationPolicyRule(id=6, membership_tier=MembershipTier.SILVER, cancellation_window_start_days=1, cancellation_window_end_days=6, refund_percentage=0.75),
    CancellationPolicyRule(id=7, membership_tier=MembershipTier.SILVER, cancellation_window_start_days=0, cancellation_window_end_days=0, refund_percentage=0.25), # Less than 24 hours
    CancellationPolicyRule(id=8, membership_tier=MembershipTier.SILVER, cancellation_window_start_days=-9999, cancellation_window_end_days=-1, refund_percentage=0.00), # After check-in (No-Show)

    # Bronze Tier
    CancellationPolicyRule(id=9, membership_tier=MembershipTier.BRONZE, cancellation_window_start_days=7, cancellation_window_end_days=9999, refund_percentage=1.00),
    CancellationPolicyRule(id=10, membership_tier=MembershipTier.BRONZE, cancellation_window_start_days=1, cancellation_window_end_days=6, refund_percentage=0.50),
    CancellationPolicyRule(id=11, membership_tier=MembershipTier.BRONZE, cancellation_window_start_days=0, cancellation_window_end_days=0, refund_percentage=0.00), # Less than 24 hours
    CancellationPolicyRule(id=12, membership_tier=MembershipTier.BRONZE, cancellation_window_start_days=-9999, cancellation_window_end_days=-1, refund_percentage=0.00)  # After check-in (No-Show)
]
