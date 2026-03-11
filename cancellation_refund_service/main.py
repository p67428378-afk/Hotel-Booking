from datetime import datetime, timedelta
from typing import List, Optional

from cancellation_refund_service.models import (
    Booking,
    CancellationPolicyRule,
    MembershipTier,
    RefundStatus,
    RefundTransaction,
)
from cancellation_refund_service.config import CANCELLATION_POLICY_RULES

class RefundCalculator:
    def __init__(self, policy_rules: List[CancellationPolicyRule]):
        self.policy_rules = policy_rules

    def calculate_refund_percentage(
        self, membership_tier: MembershipTier, check_in_date: datetime, cancellation_date: datetime
    ) -> float:
        time_until_check_in = check_in_date - cancellation_date
        days_until_check_in = time_until_check_in.days

        # Determine the correct cancellation window based on days_until_check_in
        # and find the corresponding refund percentage for the membership tier.
        for rule in self.policy_rules:
            if rule.membership_tier == membership_tier:
                if rule.cancellation_window_start_days <= days_until_check_in <= rule.cancellation_window_end_days:
                    return rule.refund_percentage
        return 0.0  # Default to no refund if no rule matches

    def calculate_refund_amount(
        self, booking: Booking, cancellation_date: datetime
    ) -> float:
        refund_percentage = self.calculate_refund_percentage(
            booking.guest_membership_tier, booking.check_in_date, cancellation_date
        )
        return booking.total_amount * refund_percentage

    def process_cancellation(
        self, booking: Booking, cancellation_date: datetime, initiated_by: str, reason: Optional[str] = None
    ) -> RefundTransaction:
        calculated_refund_amount = self.calculate_refund_amount(booking, cancellation_date)

        # Simulate interaction with a payment gateway
        payment_gateway_txn_id = f"PG_TXN_{datetime.now().timestamp()}"
        refund_status = RefundStatus.SUCCESSFUL # Assume success for simulation

        # In a real system, this would involve calling the payment gateway API
        # and handling potential failures, retries, etc.

        refund_transaction = RefundTransaction(
            id=hash(payment_gateway_txn_id), # Simple hash for unique ID
            booking_id=booking.id,
            guest_id=booking.guest_id,
            calculated_refund_amount=calculated_refund_amount,
            original_booking_amount=booking.total_amount,
            payment_gateway_txn_id=payment_gateway_txn_id,
            status=refund_status,
            timestamp=datetime.now(),
            initiated_by=initiated_by,
            reason=reason
        )
        print(f"Processed cancellation for booking {booking.id}. Refund amount: {calculated_refund_amount:.2f}")
        return refund_transaction

# Example Usage
if __name__ == "__main__":
    refund_calculator = RefundCalculator(CANCELLATION_POLICY_RULES)

    # --- Example 1: Gold member cancels 5 days before check-in ---
    # Expected: 90% refund
    booking1_check_in = datetime.now() + timedelta(days=5)
    booking1 = Booking(
        id="BOOK-001",
        guest_id="GUEST-001",
        guest_membership_tier=MembershipTier.GOLD,
        check_in_date=booking1_check_in,
        total_amount=1000.00,
        original_payment_method_token="token_gold_001",
    )
    cancellation_date1 = datetime.now()
    refund_txn1 = refund_calculator.process_cancellation(booking1, cancellation_date1, "GUEST-001", "Change of plans")
    print(f"Booking 1 Refund: {refund_txn1.calculated_refund_amount:.2f} (Expected: 900.00)\n")

    # --- Example 2: Bronze member cancels 2 days before check-in ---
    # Expected: 50% refund
    booking2_check_in = datetime.now() + timedelta(days=2)
    booking2 = Booking(
        id="BOOK-002",
        guest_id="GUEST-002",
        guest_membership_tier=MembershipTier.BRONZE,
        check_in_date=booking2_check_in,
        total_amount=500.00,
        original_payment_method_token="token_bronze_002",
    )
    cancellation_date2 = datetime.now()
    refund_txn2 = refund_calculator.process_cancellation(booking2, cancellation_date2, "STAFF-001", "Guest request")
    print(f"Booking 2 Refund: {refund_txn2.calculated_refund_amount:.2f} (Expected: 250.00)\n")

    # --- Example 3: Any member cancels 7 days or more before check-in ---
    # Expected: 100% refund
    booking3_check_in = datetime.now() + timedelta(days=8)
    booking3 = Booking(
        id="BOOK-003",
        guest_id="GUEST-003",
        guest_membership_tier=MembershipTier.SILVER,
        check_in_date=booking3_check_in,
        total_amount=750.00,
        original_payment_method_token="token_silver_003",
    )
    cancellation_date3 = datetime.now()
    refund_txn3 = refund_calculator.process_cancellation(booking3, cancellation_date3, "GUEST-003")
    print(f"Booking 3 Refund: {refund_txn3.calculated_refund_amount:.2f} (Expected: 750.00)\n")

    # --- Example 4: Silver member cancels 10 hours before check-in (same day) ---
    # Expected: 25% refund
    booking4_check_in = datetime.now().replace(hour=18, minute=0, second=0, microsecond=0) + timedelta(days=0)
    booking4 = Booking(
        id="BOOK-004",
        guest_id="GUEST-004",
        guest_membership_tier=MembershipTier.SILVER,
        check_in_date=booking4_check_in,
        total_amount=1200.00,
        original_payment_method_token="token_silver_004",
    )
    cancellation_date4 = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0) # 10 hours before 18:00
    refund_txn4 = refund_calculator.process_cancellation(booking4, cancellation_date4, "GUEST-004")
    print(f"Booking 4 Refund: {refund_txn4.calculated_refund_amount:.2f} (Expected: 300.00)\n")

    # --- Example 5: No-Show (cancellation after check-in time) ---
    # Expected: 0% refund
    booking5_check_in = datetime.now() - timedelta(days=1)
    booking5 = Booking(
        id="BOOK-005",
        guest_id="GUEST-005",
        guest_membership_tier=MembershipTier.BRONZE,
        check_in_date=booking5_check_in,
        total_amount=300.00,
        original_payment_method_token="token_bronze_005",
    )
    cancellation_date5 = datetime.now()
    refund_txn5 = refund_calculator.process_cancellation(booking5, cancellation_date5, "STAFF-002", "No-show")
    print(f"Booking 5 Refund: {refund_txn5.calculated_refund_amount:.2f} (Expected: 0.00)\n")
