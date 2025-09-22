import unittest
from accounts import Account, Transaction, get_share_price
from datetime import datetime, timedelta
from unittest.mock import patch

class TestAccount(unittest.TestCase):

    def setUp(self):
        self.account = Account(user_id=1, initial_deposit=1000)

    def test_initial_balance(self):
        self.assertEqual(self.account.balance, 1000)
        self.assertEqual(self.account.initial_deposit, 1000)
        self.assertEqual(self.account.portfolio, {})
        self.assertEqual(self.account.transactions, [])

    def test_deposit(self):
        self.account.deposit(500)
        self.assertEqual(self.account.balance, 1500)

    def test_deposit_negative_amount(self):
        self.account.deposit(-500)
        self.assertEqual(self.account.balance, 1000)  # Balance should remain unchanged

    def test_withdraw_sufficient_funds(self):
        self.account.withdraw(200)
        self.assertEqual(self.account.balance, 800)

    def test_withdraw_insufficient_funds(self):
        with self.assertRaises(ValueError):
            self.account.withdraw(1500)
        self.assertEqual(self.account.balance, 1000)  # Balance should remain unchanged

    def test_buy_shares_sufficient_funds(self):
        self.account.buy_shares("AAPL", 5)
        self.assertEqual(self.account.balance, 1000 - 5 * 150)
        self.assertEqual(self.account.portfolio, {"AAPL": 5})
        self.assertEqual(len(self.account.transactions), 1)
        self.assertEqual(self.account.transactions[0].type, "buy")

    def test_buy_shares_insufficient_funds(self):
        with self.assertRaises(ValueError):
            self.account.buy_shares("AAPL", 100)
        self.assertEqual(self.account.balance, 1000)  # Balance should remain unchanged
        self.assertEqual(self.account.portfolio, {})  # Portfolio should remain unchanged

    def test_sell_shares_sufficient_holdings(self):
        self.account.buy_shares("AAPL", 10)
        self.account.sell_shares("AAPL", 5)
        self.assertEqual(self.account.balance, 1000 - 10 * 150 + 5 * 150)
        self.assertEqual(self.account.portfolio, {"AAPL": 5})
        self.assertEqual(len(self.account.transactions), 2)
        self.assertEqual(self.account.transactions[1].type, "sell")

    def test_sell_shares_insufficient_holdings(self):
        with self.assertRaises(ValueError):
            self.account.sell_shares("AAPL", 5)
        self.assertEqual(self.account.balance, 1000)  # Balance should remain unchanged
        self.assertEqual(self.account.portfolio, {})  # Portfolio should remain unchanged

    def test_get_portfolio_value(self):
        self.account.buy_shares("AAPL", 10)
        self.account.buy_shares("TSLA", 2)
        self.assertEqual(self.account.get_portfolio_value(), 10 * 150 + 2 * 700)

    def test_get_profit_loss(self):
        self.account.buy_shares("AAPL", 10)
        self.assertEqual(self.account.get_profit_loss(), -10 * 150 + 10 * 150)  # No profit/loss initially

    def test_get_holdings(self):
        self.account.buy_shares("AAPL", 10)
        self.account.buy_shares("TSLA", 2)
        self.assertEqual(self.account.get_holdings(), {"AAPL": 10, "TSLA": 2})

    def test_get_transactions(self):
        self.account.buy_shares("AAPL", 10)
        self.account.sell_shares("AAPL", 5)
        transactions = self.account.get_transactions()
        self.assertEqual(len(transactions), 2)
        self.assertEqual(transactions[0]['type'], "buy")
        self.assertEqual(transactions[1]['type'], "sell")

    @patch('accounts.datetime')
    def test_transaction_timestamp(self, mock_datetime):
        mock_datetime.now.return_value = datetime(2023, 1, 1, 12, 0, 0)
        self.account.buy_shares("AAPL", 10)
        self.assertEqual(self.account.transactions[0].timestamp, datetime(2023, 1, 1, 12, 0, 0))

if __name__ == '__main__':
    unittest.main()