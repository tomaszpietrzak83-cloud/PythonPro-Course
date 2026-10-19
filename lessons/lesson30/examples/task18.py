import random
import threading
import time

from lab_support import event, launch, metric, span


class BankAccount:
    def __init__(self):
        self.balance = 200
        self.lock = threading.Lock()
        self.history = []

    def deposit(self, amount):
        # @step deposit
        with self.lock:
            self.balance += amount
            self.history.append(amount)
            event("balance", "Account", f"+{amount}", value=self.balance)

    def withdraw(self, amount):
        # @step withdraw
        with self.lock:
            if self.balance >= amount:
                self.balance -= amount
                self.history.append(-amount)
                event("balance", "Account", f"−{amount}", value=self.balance)
            else:
                event("log", "Account", f"Declined: {amount}")


def main(config):
    account = BankAccount()
    rng = random.Random(30)

    def transaction(number, method, amount):
        with span(f"Customer {number}", "transaction"):
            time.sleep(number * 0.08)
            method(amount)

    threads = [
        threading.Thread(
            target=transaction,
            args=(
                i,
                account.deposit if i < 5 else account.withdraw,
                rng.randint(20, 120),
            ),
        )
        for i in range(10)
    ]
    for worker_thread in threads:
        worker_thread.start()
    for worker_thread in threads:
        worker_thread.join()
    metric("Balance", account.balance)
    # @step reconcile
    metric("Reconciled balance", 200 + sum(account.history))


if __name__ == "__main__":
    launch(main)
