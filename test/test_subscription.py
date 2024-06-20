import unittest
from subscription import Subscription

class TestSubscription(unittest.TestCase):

    def test_silver_subscription_cashback(self):
        subscription = Subscription(type="Silver", duration=12, cashback_policy="20% for first 3 purchases")
        cashback = subscription.apply_cashback(amount=100, purchases_count=2)
        self.assertEqual(cashback, 20)

        cashback = subscription.apply_cashback(amount=100, purchases_count=4)
        self.assertEqual(cashback, 0)

    def test_gold_subscription_cashback(self):
        subscription = Subscription(type="Gold", duration=12, cashback_policy="50% for first 5 purchases")
        cashback = subscription.apply_cashback(amount=100, purchases_count=3)
        self.assertEqual(cashback, 50)

        cashback = subscription.apply_cashback(amount=100, purchases_count=6)
        self.assertEqual(cashback, 0)

    def test_no_cashback(self):
        subscription = Subscription(type="Bronze", duration=12, cashback_policy="No cashback")
        cashback = subscription.apply_cashback(amount=100, purchases_count=1)
        self.assertEqual(cashback, 0)

if __name__ == '__main__':
    unittest.main()
