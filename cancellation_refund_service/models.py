from datetime import datetime
from enum import Enum

class MembershipTier(Enum):
    BRONZE = "Bronze"
    SILVER = "Silver"
    GOLD = "Gold"

class CancellationWindow(Enum):
    SEVEN_DAYS_OR_MORE = "7 Days or more before check-in"
    ONE_TO_SIX_DAYS = "Between 1 and 6 days before"
    LESS_THAN_24_HOURS = "Less than 24 hours before"
    AFTER_CHECK_IN = "After check-in time (No-Show)"

class RefundStatus(Enum):
    INITIATED = "Initiated"
    SUCCESSFUL = "Successful"
    FAILED = "Failed"
    MANUAL_REVIEW = "Manual Review"

class CancellationPolicyRule:
    def __init__(self, id: int, membership_tier: MembershipTier, cancellation_window_start_days: int, cancellation_window_end_days: int, refund_percentage: float):
        self.id = id
        self.membership_tier = membership_tier
        self.cancellation_window_start_days = cancellation_window_start_days
        self.cancellation_window_end_days = cancellation_window_end_days
        self.refund_percentage = refund_percentage

class RefundTransaction:
    def __init__(self, id: int, booking_id: str, guest_id: str, calculated_refund_amount: float, original_booking_amount: float, payment_gateway_txn_id: str, status: RefundStatus, timestamp: datetime, initiated_by: str, reason: str = None):
        self.id = id
        self.booking_id = booking_id
        self.guest_id = guest_id
        self.calculated_refund_amount = calculated_refund_amount
        self.original_booking_amount = original_booking_amount
        self.payment_gateway_txn_id = payment_gateway_txn_id
        self.status = status
        self.timestamp = timestamp
        self.initiated_by = initiated_by
        self.reason = reason

class Booking:
    def __init__(self, id: str, guest_id: str, guest_membership_tier: MembershipTier, check_in_date: datetime, total_amount: float, original_payment_method_token: str):
        self.id = id
        self.guest_id = guest_id
        self.guest_membership_tier = guest_membership_tier
        self.check_in_date = check_in_date
        self.total_amount = total_amount
        self.original_payment_method_token = original_payment_method_token
