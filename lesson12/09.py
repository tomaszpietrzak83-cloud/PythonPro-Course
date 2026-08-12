from dataclasses import dataclass


@dataclass
class BankAccount:
    _balance: float

    class LackOfFundsError(Exception):
        def __init__(self, message="Insufficient funds for withdrawal."):
            super().__init__(message)

    class InvalidAmountError(Exception):
        def __init__(self, message="Amount must be positive."):
            super().__init__(message)

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, value):
        if value < 0:
            raise BankAccount.InvalidAmountError(
                "Initial balance cannot be negative."
            )

        self._balance = value

    def deposit(self, amount):

        if amount <= 0:
            raise BankAccount.InvalidAmountError(
                "Deposit amount must be positive."
            )
        self._balance += amount
        print(f"Deposited: {amount}. New balance: {self._balance}")

    def withdraw(self, amount):
        if amount <= 0:
            raise BankAccount.InvalidAmountError(
                "Withdrawal amount must be positive."
            )

        if amount >= self._balance:
            raise BankAccount.LackOfFundsError()
        self._balance -= amount
        print(f"Withdrew: {amount}. New balance: {self._balance}")


account = BankAccount(_balance=256.0)

try:
    amount = -250
    account.deposit(amount)
except BankAccount.InvalidAmountError as e:
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
except BankAccount.InvalidAmountError as e:
    print(f"Error: {e} incorrect amount: {amount}")

try:
    amount1 = 100
    account.deposit(amount1)
    amount2 = 50
    account.withdraw(amount2)
except (BankAccount.InvalidAmountError, BankAccount.LackOfFundsError) as e:
    print(f"Error: {e}")
