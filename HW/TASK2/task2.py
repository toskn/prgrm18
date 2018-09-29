import urllib.request
import urllib.error
import json
import re
import sys


user = input('Введите имя пользователя')
token = 'ccb3a4b775d7e1a38f77fc97ac5496b9b2e16c86'  # insert your token
headers = {'apikey': 'token %s' % token}


def choose_func():

    choice = int(input('Введите номер той функции из списка, которую хотите исползовать:\n'
                       '1. Узнать названия и описания репозиториев пользователя\n'
                       '2. Узнать список языков пользователя и репозитории, в которых они используются\n'))
    if choice == 1:
        repo_info(get_repos())
    elif choice == 2:
        languages_sort(get_languages(repo_info1(get_repos1())))
    # elif choice == 3:

    # elif choice == 4:

    elif choice != 1 and choice != 2 and choice != 3 and choice != 4:
        sys.exit("Такая категория отсутствует. Перезапустите программу.")

    return 0


# Here the program gets the repository of the chosen user
def get_repos():
    url = 'https://api.github.com/users/%s/repos' % user
    try:
        request = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(request)
        text = response.read().decode('utf-8')
        data = json.loads(text)
        print('\nВы выбрали пользователя GitHub с ником "' + user + '"\nВот список его репозиториев: \n')
        return data
    except urllib.error.URLError as e:
        print('A problem occurred: ' + str(e.reason))


def repo_info(data):
    i = 0
    regdescr = re.compile("'description':.*?, 'fork':", re.DOTALL)
    regdescr1 = re.compile("\s?'description': '?")
    regname = re.compile("'name':.*?, 'full_name':", re.DOTALL)
    reglicense = re.compile(", 'license'.*?}")

    repo_descr = regdescr.findall(str(data))
    repo_name = reglicense.sub('}', str(data))
    repo_name = regname.findall(repo_name)
    while i < len(repo_descr):
        repo_descr[i] = regdescr1.sub('', repo_descr[i])
        repo_descr[i] = repo_descr[i][:-9]
        if repo_descr[i][-1:] == "'":
            repo_descr[i] = repo_descr[i][:-1]
        i += 1
    i = 0
    while i < len(repo_name):
        repo_name[i] = repo_name[i][9:-15]
        i += 1
    i = 0
    while i < len(repo_name):
        if len(repo_name) - 1 != i:
            print(str(repo_name[i]) + ": " + str(repo_descr[i]) + ",")
        else:
            print(str(repo_name[i]) + ": " + str(repo_descr[i]) + ".")
        i += 1
    return repo_name


def get_repos1():
    url = 'https://api.github.com/users/%s/repos' % user
    try:
        request = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(request)
        text = response.read().decode('utf-8')
        data = json.loads(text)
        return data
    except urllib.error.URLError as e:
        print('A problem occurred: ' + str(e.reason))


def repo_info1(data):
    i = 0
    regdescr = re.compile("'description':.*?, 'fork':", re.DOTALL)
    regdescr1 = re.compile("\s?'description': '?")
    regname = re.compile("'name':.*?, 'full_name':", re.DOTALL)
    reglicense = re.compile(", 'license'.*?}")

    repo_descr = regdescr.findall(str(data))
    repo_name = reglicense.sub('}', str(data))
    repo_name = regname.findall(repo_name)
    while i < len(repo_descr):
        repo_descr[i] = regdescr1.sub('', repo_descr[i])
        repo_descr[i] = repo_descr[i][:-9]
        if repo_descr[i][-1:] == "'":
            repo_descr[i] = repo_descr[i][:-1]
        i += 1
    i = 0
    while i < len(repo_name):
        repo_name[i] = repo_name[i][9:-15]
        i += 1
    return repo_name, data


def get_languages(repo_name, data):
    i = 0
    data_languages = []
    while i < len(repo_name):
        url = 'https://api.github.com/repos/' + str(user) + '/' + str(repo_name[i]) + '/languages'
        try:
            request = urllib.request.Request(url, headers=headers)
            response = urllib.request.urlopen(request)
            text = response.read().decode('utf-8')
            data = json.loads(text)
            data_languages.append(data)
            i += 1
            print(data_languages)
            print(type(data_languages))
            print(type(data_languages[0]))
        except urllib.error.URLError as e:
            print('A problem occurred: ' + str(e.reason))
    return data_languages, data


def languages_sort(data_languages, data):
    i = 0
    lang_clear = []
    while i < len(data_languages):
        for key in data_languages[i]:
            lang_clear.append(key)
            lang_clear = list(set(lang_clear))
        i += 1
    i = 0
    str_lang = ''
    while i < len(lang_clear):
        if i + 1 != len(lang_clear):
            str_lang = str_lang + str(lang_clear[i]) + ', '
        else:
            str_lang = str_lang + str(lang_clear[i]) + '.'
        for key in data:
            if key in data == 'language':
                if lang_clear[i] == dict.get(key, ''):
                    print('Язык' + str(lang_clear[i]) + 'используется в репозитории' + str(data['name']))

        i += 1
    print('Пользователь ' + str(user) + ' пишет на ' + str_lang)

    return 0


choose_func()
