from dataclasses import dataclass


@dataclass
class BankAccount:
    _balance: float

    class LackOfFundsError(Exception):
        pass

    @property
    def balance(self):
        return self._balance

    # @balance.setter
    # def balance(self, value):
    #     if value < 0:
    #         raise ValueError("Initial balance cannot be negative.")
    #     self._balance = value

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self._balance += amount
        print(f"Deposited: {amount}. New balance: {self._balance}")

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self._balance:
            raise BankAccount.LackOfFundsError("Insufficient funds for withdrawal.")
        self._balance -= amount
        print(f"Withdrew: {amount}. New balance: {self._balance}")


account = BankAccount(_balance=256.0)

try:
    amount = -250
    account.deposit(amount)
except ValueError as e:
    print(f"Error: {e} incorrect amount: {amount}")

try:
    amount = 300
    account.withdraw(amount)
except BankAccount.LackOfFundsError as e:
    print(
        f"Error: {e} current balance: {account._balance}, attempted withdrawal: {amount}"
    )

try:
    amount = -50
    account.withdraw(amount)
except ValueError as e:
    print(f"Error: {e} incorrect amount: {amount}")

try:
    amount1 = 100
    account.deposit(amount1)
    amount2 = 50
    account.withdraw(amount2)
except (ValueError, BankAccount.LackOfFundsError) as e:
    print(f"Error: {e}")
