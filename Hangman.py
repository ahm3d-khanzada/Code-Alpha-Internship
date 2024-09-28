import random
from wordlist import animal, food, fruit, vegetable

# dictionary of key

hangman = {
    0: ("  _______     ",
        " |/           ",
        " |            ",
        " |            ",
        " |            ",
        " |            ",
        "_|___         "),

    1: ("  _______     ",
        " |/      |    ",
        " |            ",
        " |            ",
        " |            ",
        " |            ",
        "_|___         "),

    2: ("  _______     ",
        " |/      |    ",
        " |       o    ",
        " |            ",
        " |            ",
        " |            ",
        "_|___         "),

    3: ("  _______     ",
        " |/      |    ",
        " |       o    ",
        " |       |    ",
        " |            ",
        " |            ",
        "_|___         "),

    4: ("  _______     ",
        " |/      |    ",
        " |       o    ",
        " |      /|    ",
        " |            ",
        " |            ",
        "_|___         "),

    5: ("  _______     ",
        " |/      |    ",
        " |       o    ",
        " |      /|\\  ",
        " |            ",
        " |            ",
        "_|___         "),

    6: ("  _______     ",
        " |/      |    ",
        " |       o    ",
        " |      /|\\  ",
        " |       |    ",
        " |            ",
        "_|___         "),

    7: ("  _______     ",
        " |/      |    ",
        " |       o    ",
        " |      /|\\  ",
        " |       |    ",
        " |      /     ",
        "_|___         "),

    8: ("  _______     ",
        " |/      |    ",
        " |       o    ",
        " |      /|\\  ",
        " |       |    ",
        " |      / \\  ",
        "_|___         ")
}


def display_man(wrong_guesses):
    print("**************************")
    for line in hangman[wrong_guesses]:
        print(line)
    print("**************************")


def display_hint(hint):
    print(" ".join(hint))


def display_answer(answer):
    print(" ".join(answer))


answer = ""


def main():
    game = input("Select your game type: Animal(1), Food(2), Vegetable(3), Fruit(4): \n").lower()

    answer = ""

    if game == "1" or game == "animal":
        answer = random.choice(animal)
    elif game == "2" or game == "food":
        answer = random.choice(food)
    elif game == "3" or game == "vegetable":
        answer = random.choice(vegetable)
    elif game == "4" or game == "fruit":
        answer = random.choice(fruit)
    else:
        print("Invalid Input!")
        return  # Exit the function if the input is invalid

    hint = ["_"] * len(answer)
    wrong_guesses = 0
    guesses_letter = set()
    is_running = True

    while is_running:
        display_man(wrong_guesses)
        display_hint(hint)
        guess = input("Enter a letter: ").lower()

        if len(guess) != 1 or not guess.isalpha():
            print("Guess one alphabet at a time")
            continue

        if guess in guesses_letter:
            print(f"{guess} is already guessed")
            continue

        guesses_letter.add(guess)

        if guess in answer:
            for i in range(len(answer)):
                if answer[i] == guess:
                    hint[i] = guess
        else:
            wrong_guesses += 1

        if "_" not in hint:
            display_man(wrong_guesses)
            display_answer(answer)
            print("YOU WIN!")
            is_running = False
        elif wrong_guesses >= len(hangman) - 1:
            display_man(wrong_guesses)
            print("YOU LOSE!")
            is_running = False


if __name__ == "__main__":
    main()
