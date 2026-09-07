from hangman import (
    show_word,
    is_valid_letter,
    is_letter_guessed,
    is_word_guessed
)


# -------------------------
# Тесты корректной работы
# -------------------------

def test_show_word():
    result = show_word("python", ["p", "t", "n"])

    assert result == "p _ t _ _ n"


def test_valid_letter():
    assert is_valid_letter("a") is True


def test_word_is_guessed():
    assert is_word_guessed("cat", ["c", "a", "t"]) is True


def test_letter_is_not_guessed():
    assert is_letter_guessed("a", ["b", "c"]) is False


# -------------------------
# Тесты некорректных данных
# -------------------------

def test_empty_input():
    assert is_valid_letter("") is False


def test_multiple_letters():
    assert is_valid_letter("abc") is False


def test_number_input():
    assert is_valid_letter("5") is False


def test_special_character():
    assert is_valid_letter("!") is False


def test_repeated_letter():
    assert is_letter_guessed("a", ["a", "b"]) is True


def test_word_is_not_guessed():
    assert is_word_guessed("python", ["p", "y"]) is False
