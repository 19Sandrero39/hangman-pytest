import unittest

from bank_account import BankAccount, InsufficientFundsError, InvalidAmountError


class TestCreation(unittest.TestCase):
    def test_account_stores_owner_and_number(self):
        acc = BankAccount("Саша", "KG001")
        self.assertEqual(acc.owner, "Саша")
        self.assertEqual(acc.account_number, "KG001")

    def test_initial_balance_is_zero(self):
        self.assertEqual(BankAccount("Саша", "KG001").get_balance(), 0)

    def test_empty_owner_raises(self):
        with self.assertRaises(ValueError):
            BankAccount("", "KG001")

    def test_empty_account_number_raises(self):
        with self.assertRaises(ValueError):
            BankAccount("Саша", "  ")

    def test_non_string_owner_raises(self):
        with self.assertRaises(ValueError):
            BankAccount(123, "KG001")


class TestDeposit(unittest.TestCase):
    def setUp(self):
        self.acc = BankAccount("Саша", "KG001")

    def test_deposit_increases_balance(self):
        self.acc.deposit(100)
        self.assertEqual(self.acc.get_balance(), 100)

    def test_multiple_deposits_accumulate(self):
        self.acc.deposit(100)
        self.acc.deposit(50.5)
        self.assertAlmostEqual(self.acc.get_balance(), 150.5)

    def test_deposit_negative_raises(self):
        with self.assertRaises(InvalidAmountError):
            self.acc.deposit(-10)
        self.assertEqual(self.acc.get_balance(), 0)

    def test_deposit_zero_raises(self):
        with self.assertRaises(InvalidAmountError):
            self.acc.deposit(0)

    def test_deposit_non_number_raises(self):
        for bad in ("100", None, [5], True):
            with self.subTest(value=bad):
                with self.assertRaises(InvalidAmountError):
                    self.acc.deposit(bad)
        self.assertEqual(self.acc.get_balance(), 0)

    def test_deposit_nan_and_inf_raise(self):
        for bad in (float("nan"), float("inf")):
            with self.subTest(value=bad):
                with self.assertRaises(InvalidAmountError):
                    self.acc.deposit(bad)


class TestWithdraw(unittest.TestCase):
    def setUp(self):
        self.acc = BankAccount("Саша", "KG001")
        self.acc.deposit(200)

    def test_withdraw_decreases_balance(self):
        self.acc.withdraw(50)
        self.assertEqual(self.acc.get_balance(), 150)

    def test_withdraw_entire_balance(self):
        self.acc.withdraw(200)
        self.assertEqual(self.acc.get_balance(), 0)

    def test_withdraw_more_than_balance_raises(self):
        with self.assertRaises(InsufficientFundsError):
            self.acc.withdraw(200.01)
        self.assertEqual(self.acc.get_balance(), 200)

    def test_withdraw_negative_raises(self):
        with self.assertRaises(InvalidAmountError):
            self.acc.withdraw(-5)
        self.assertEqual(self.acc.get_balance(), 200)

    def test_withdraw_zero_raises(self):
        with self.assertRaises(InvalidAmountError):
            self.acc.withdraw(0)

    def test_withdraw_non_number_raises(self):
        with self.assertRaises(InvalidAmountError):
            self.acc.withdraw("50")


class TestTransfer(unittest.TestCase):
    def setUp(self):
        self.a = BankAccount("Саша", "KG001")
        self.b = BankAccount("Айбек", "KG002")
        self.a.deposit(500)
        self.b.deposit(100)

    def test_successful_transfer_changes_balances(self):
        self.a.transfer(self.b, 200)
        self.assertEqual(self.a.get_balance(), 300)
        self.assertEqual(self.b.get_balance(), 300)

    def test_transfer_changes_are_equal(self):
        total_before = self.a.get_balance() + self.b.get_balance()
        a_before, b_before = self.a.get_balance(), self.b.get_balance()
        self.a.transfer(self.b, 123)
        self.assertEqual(
            a_before - self.a.get_balance(), self.b.get_balance() - b_before
        )
        self.assertEqual(total_before, self.a.get_balance() + self.b.get_balance())

    def test_transfer_insufficient_funds_keeps_state(self):
        with self.assertRaises(InsufficientFundsError):
            self.a.transfer(self.b, 1000)
        self.assertEqual(self.a.get_balance(), 500)
        self.assertEqual(self.b.get_balance(), 100)

    def test_transfer_invalid_amount_keeps_state(self):
        for bad in (-1, 0, "10", float("nan")):
            with self.subTest(value=bad):
                with self.assertRaises(InvalidAmountError):
                    self.a.transfer(self.b, bad)
        self.assertEqual(self.a.get_balance(), 500)
        self.assertEqual(self.b.get_balance(), 100)

    def test_transfer_to_same_account_raises(self):
        with self.assertRaises(ValueError):
            self.a.transfer(self.a, 10)
        self.assertEqual(self.a.get_balance(), 500)

    def test_transfer_to_non_account_raises(self):
        with self.assertRaises(TypeError):
            self.a.transfer("KG002", 10)
        self.assertEqual(self.a.get_balance(), 500)

    def test_transfer_entire_balance(self):
        self.a.transfer(self.b, 500)
        self.assertTrue(self.a.is_empty())
        self.assertEqual(self.b.get_balance(), 600)


class TestBalanceAndEmpty(unittest.TestCase):
    def setUp(self):
        self.acc = BankAccount("Саша", "KG001")

    def test_new_account_is_empty(self):
        self.assertTrue(self.acc.is_empty())

    def test_account_not_empty_after_deposit(self):
        self.acc.deposit(1)
        self.assertFalse(self.acc.is_empty())

    def test_account_empty_after_full_withdraw(self):
        self.acc.deposit(70)
        self.acc.withdraw(70)
        self.assertTrue(self.acc.is_empty())

    def test_balance_matches_sequence_of_operations(self):
        other = BankAccount("Айбек", "KG002")
        self.acc.deposit(1000)
        self.acc.withdraw(250)
        self.acc.transfer(other, 150)
        self.acc.deposit(50)
        self.assertEqual(self.acc.get_balance(), 650)
        self.assertEqual(other.get_balance(), 150)


if __name__ == "__main__":
    unittest.main()
