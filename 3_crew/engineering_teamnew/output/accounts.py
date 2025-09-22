from datetime import datetime

# Utility Function
def get_share_price(symbol):
    # Test implementation with fixed prices
    prices = {"AAPL": 150.0, "TSLA": 700.0, "GOOGL": 2800.0}
    return prices.get(symbol, 0.0)

# Transaction Class
class Transaction:
    def __init__(self, type, symbol, quantity, price):
        self.timestamp = datetime.now()
        self.type = type
        self.symbol = symbol
        self.quantity = quantity
        self.price = price

# Account Class
class Account:
    def __init__(self, user_id, initial_deposit):
        self.user_id = user_id
        self.balance = initial_deposit
        self.initial_deposit = initial_deposit
        self.portfolio = {}
        self.transactions = []

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
        else:
            raise ValueError("Insufficient funds for withdrawal.")

    def buy_shares(self, symbol, quantity):
        price = get_share_price(symbol)
        total_cost = price * quantity
        if total_cost <= self.balance:
            self.balance -= total_cost
            self.portfolio[symbol] = self.portfolio.get(symbol, 0) + quantity
            self.transactions.append(Transaction("buy", symbol, quantity, price))
        else:
            raise ValueError("Insufficient funds to buy shares.")

    def sell_shares(self, symbol, quantity):
        if self.portfolio.get(symbol, 0) >= quantity:
            price = get_share_price(symbol)
            self.balance += price * quantity
            self.portfolio[symbol] -= quantity
            if self.portfolio[symbol] == 0:
                del self.portfolio[symbol]
            self.transactions.append(Transaction("sell", symbol, quantity, price))
        else:
            raise ValueError("Insufficient shares to sell.")

    def get_portfolio_value(self):
        return sum(get_share_price(symbol) * quantity for symbol, quantity in self.portfolio.items())

    def get_profit_loss(self):
        return self.balance + self.get_portfolio_value() - self.initial_deposit

    def get_holdings(self):
        return self.portfolio.copy()

    def get_transactions(self):
        return [transaction.__dict__ for transaction in self.transactions]