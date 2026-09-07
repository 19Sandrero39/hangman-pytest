import random


WORDS = [
    "python",
    "computer",
    "keyboard",
    "programming",
    "terminal",
    "linux",
    "database",
    "algorithm",
    "network",
    "security"
]


def show_word(word, guessed_letters):
    """Показывает угаданные буквы и скрывает остальные."""
    result = ""

    for letter in word:
        if letter in guessed_letters:
            result += letter + " "
        else:
            result += "_ "

    return result.strip()


def is_valid_letter(letter):
    """Проверяет, является ли ввод одной буквой."""
    return len(letter) == 1 and letter.isalpha()


def is_letter_guessed(letter, guessed_letters):
    """Проверяет, вводилась ли буква ранее."""
    return letter in guessed_letters


def is_word_guessed(word, guessed_letters):
    """Проверяет, угадано ли всё слово."""
    return all(letter in guessed_letters for letter in word)


def play_game():
    word = random.choice(WORDS)
    guessed_letters = []
    attempts = 10

    print("=" * 30)
    print("        ВИСЕЛИЦА")
    print("=" * 30)
    print(f"У вас {attempts} попыток.")
    print()

    while attempts > 0:
        print("Слово:", show_word(word, guessed_letters))
        print("Осталось попыток:", attempts)

        letter = input("Введите букву: ").lower().strip()

        if not is_valid_letter(letter):
            print("Введите одну букву!")
            print()
            continue

        if is_letter_guessed(letter, guessed_letters):
            print("Вы уже вводили эту букву!")
            print()
            continue

        guessed_letters.append(letter)

        if letter in word:
            print("Верно!")
        else:
            attempts -= 1
            print("Такой буквы нет!")

        if is_word_guessed(word, guessed_letters):
            print()
            print("Поздравляем! Вы угадали слово:", word)
            return

        print()

    print("Попытки закончились!")
    print("Загаданное слово:", word)


def main():
    while True:
        play_game()

        answer = input("\nСыграть ещё раз? (да/нет): ").lower().strip()

        if answer not in ["yes", "да"]:
            print("Спасибо за игру!")
            break

        print()


if __name__ == "__main__":
    main()
