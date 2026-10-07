import math


class InvalidAmountError(ValueError):
    """Некорректная сумма операции (не число, отрицательная, нулевая, NaN, inf)."""


class InsufficientFundsError(ValueError):
    """Недостаточно средств на счёте."""


class BankAccount:
    def __init__(self, owner, account_number):
        if not isinstance(owner, str) or not owner.strip():
            raise ValueError("Имя владельца должно быть непустой строкой")
        if not isinstance(account_number, str) or not account_number.strip():
            raise ValueError("Номер счёта должен быть непустой строкой")
        self.owner = owner
        self.account_number = account_number
        self._balance = 0

    @staticmethod
    def _validate_amount(amount):
        if isinstance(amount, bool) or not isinstance(amount, (int, float)):
            raise InvalidAmountError("Сумма должна быть числом")
        if math.isnan(amount) or math.isinf(amount):
            raise InvalidAmountError("Сумма должна быть конечным числом")
        if amount <= 0:
            raise InvalidAmountError("Сумма должна быть положительной")

    def deposit(self, amount):
        """Пополнить счёт."""
        self._validate_amount(amount)
        self._balance += amount

    def withdraw(self, amount):
        """Снять деньги со счёта."""
        self._validate_amount(amount)
        if amount > self._balance:
            raise InsufficientFundsError("Недостаточно средств на счёте")
        self._balance -= amount

    def transfer(self, other, amount):
        """Перевести деньги на другой счёт. При ошибке оба счёта не меняются."""
        if not isinstance(other, BankAccount):
            raise TypeError("Получатель должен быть объектом BankAccount")
        if other is self:
            raise ValueError("Нельзя переводить деньги на тот же счёт")
        # Все проверки выполняются до изменения балансов
        self._validate_amount(amount)
        if amount > self._balance:
            raise InsufficientFundsError("Недостаточно средств на счёте")
        self._balance -= amount
        other._balance += amount

    def get_balance(self):
        """Вернуть текущий баланс."""
        return self._balance

    def is_empty(self):
        """Счёт пуст, если баланс равен нулю."""
        return self._balance == 0
