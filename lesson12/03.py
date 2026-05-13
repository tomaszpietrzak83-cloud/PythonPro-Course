class CurrencyCalculator:
    @staticmethod
    def usdToPln(usd):
        return round(usd * 3.6172, 2)  # course from 2026-05-12


amount = CurrencyCalculator.usdToPln(127)
print(amount)
