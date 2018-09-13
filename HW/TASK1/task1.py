# "ё" character isn't used
# i, ii, iii are used as counters
import random
import re
import sys


# This  def allows player to choose the category
def choose_category():
    players_choice = input('Введите номер категории, которую хотите играть: \n 1) Столярные инструменты \n '
                           '2) Слесарные инструменты \n 3) Футбольные клубы, образованные в 1933 году')
    return players_choice


# This def opens the chosen file to a list
def open_file_to_list(players_choice):
    # Players' input is valid
    if players_choice == '1':
        filename = 'stolyarnie_instrumenti.txt'
    elif players_choice == '2':
        filename = 'slesarnie_instrumenti.txt'
    elif players_choice == '3':
        filename = 'football_clubs_origin_1933.txt'

    # Players' input is invalid
    elif players_choice != '1' and players_choice != '2' and players_choice != '3':
        sys.exit("Такая категория отсутствует. Перезапустите игру.")

    # Chosen .txt file is opened as a list
    with open(filename, encoding='utf-8') as file:
        file = file.read()
        file = file.split("\n")
        return file


# This def selects a random word from the list
def random_word(file):
    i = random.randint(0, 10)
    word_to_guess = file[i]
    return word_to_guess


# This def is the gameplay
def game(word_to_guess):
    attempts = 10
    list_of_tries = ['ё']
    i = 0
    ii = 0
    iii = 0
    list_of_letters = list(word_to_guess)
    underline = ''

    # Preparing the word, making it "_ _ _"-like
    while i < len(word_to_guess):
        underline += '_ '
        i += 1
    underline = underline[:-1]
    list_underline = underline.split(' ')
    print(underline)
    print('У вас есть 10 попыток, чтобы угадать слово из ' + str(len(word_to_guess)) + ' букв')

    # Preparation finished, the game starts here.
    while attempts > 0 and underline.split(' ') != list_of_letters:
        players_guess = str(input('Введите букву'))

        # Here the players' input is checked:
        # 1) if it contain letters
        # 2) if there is only one letter
        # 3) if letter is cyrillic
        if players_guess.isalpha() and len(players_guess) == 1 and bool(re.search('[а-яА-Я]', players_guess)):
            # this tells player if he already tried this letter
            for i in range(len(list_of_tries)):
                if players_guess == list_of_tries[i]:
                    print('Вы уже вводили эту букву')
                    attempts += 1
                    if attempts > 10:
                        attempts = 10
            list_of_tries.append(players_guess)
            list_of_tries = list(set(list_of_tries))
            print("Список уже введенных букв: " + str(list_of_tries))
            # Player did guess a letter; a letter of the hidden word is revealed.
            # To reveal a letter a string is created from the list.
            for i in range(len(list_of_letters)):
                if players_guess == list_of_letters[i]:
                    list_underline[i] = players_guess
                    underline = ' '.join(list_underline)
                    ii += 1
                if players_guess not in list_of_letters:
                    iii = ii

                    # Player didn't guess the letter
                    # For the sake of optimization its better to reverse the order of elifs,
                    # but here it doesn't really matter
            if ii == iii:
                print('Такой буквы в слове нет.')
                attempts -= 1
                if attempts == 0:
                    print('Попыток не осталось! Вы проиграли. Хотите сыграть еще раз?')
                elif attempts == 1:
                    print('Осталась 1 попытка')
                elif 1 < attempts < 5:
                    print('Осталось ' + str(attempts) + ' попытки')
                elif 5 <= attempts <= 10:
                    print('Осталось ' + str(attempts) + ' попыток')
            if underline.split(' ') == list_of_letters:
                print('Победа! Вы разгадали слово!')
            print(underline)
        else:
            print("Ошибка ввода. Пожалуйста, введите одну букву русского алфавита. 'Ё' не играет.")


game(random_word(open_file_to_list(choose_category())))
