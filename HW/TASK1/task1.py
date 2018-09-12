# It's supposed in this program that every letter should be guessed,
# which means that if there is a repeated letter in the word,
# it should be guessed twice.
import random


# This  def allows player to choose the category


def choose_category():
    players_choice = int(input('Type the number of the category you want to play: \n 1) Столярные инструменты \n '
                               '2) Слесарные инструменты \n 3) Футбольные клубы, образованные в 1933 году'))
    return players_choice


# This def opens the chosen file to a list


def open_file_to_list(players_choice):
    # Players' input is valid

    if players_choice == 1:
        filename = 'stolyarnie_instrumenti.txt'
    elif players_choice == 2:
        filename = 'slesarnie_instrumenti.txt'
    elif players_choice == 3:
        filename = 'football_clubs_origin_1933.txt'

    # Players' input is invalid

    elif players_choice != 1 and players_choice != 2 and players_choice != 3:
        print("That's an inappropriate input. Restart the game.")

    # Chosen .txt file is opened as a list

    with open(filename, encoding='utf-8') as file:
        file = file.read()
        file = file.split("\n")
        return file


# This def selects a random word from the list


def random_word(file):
    i = random.randint(0, 11)
    word_to_guess = file[i]
    return word_to_guess


# This def creates a variable which is actually the random word from previous def^ but all the letters are '_' now


def make_word_hidden(word_to_guess):
    i = 0
    underline = ''
    while i < len(word_to_guess):
        print('_ ')
        underline += '_ '
        i += 1
    print('У вас есть 10 попыток, чтобы угадать слово из' + str(len(word_to_guess)) + 'букв')
    return underline


# This def is the gameplay


def game(word_to_guess, underline):
    attempts = 10
    list_of_letters = list(word_to_guess)
    while attempts > 0:
        players_guess = str(input('Guess a letter'))

        # Player did guess the letter: a letter of the hidden word is revealed.

        for i in range(len(list_of_letters)):
            if players_guess == list_of_letters[i]:
                list_underline = list(underline)
                list_underline[i] = players_guess + ' '
                if underline.split(' ') == list_of_letters:
                    print('WIN')

            # Player didn't guess the letter

            else:
                attempts -= 1
                if attempts == 0:
                    print('Попыток не осталось! Вы проиграли. Хотите сыграть еще раз?')
                elif attempts == 1:
                    print('Осталась 1 попытка')
                elif 1 < attempts < 5:
                    print('Осталось' + attempts + 'попытки')
                elif 5 <= attempts <= 10:
                    print('Осталось' + attempts + 'попыток')
        print(underline)
