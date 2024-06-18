class Subscription:
    def __init__(self, type, duration, cashback_policy):
        self.type = type
        self.duration = duration
        self.cashback_policy = cashback_policy

    def apply_cashback(self, amount, purchases_count):
        if self.type == "Silver" and purchases_count <= 3:
            return amount * 0.20
        elif self.type == "Gold" and purchases_count <= 5:
            return amount * 0.50
        return 0
