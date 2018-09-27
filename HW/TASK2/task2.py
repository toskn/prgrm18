import urllib.request
import urllib.error
import json
import re


def choose_func():
    choice = input('Введите номер той функции из списка, которую хотите исползовать:\n'
                   '1. Узнать названия и описания репозиториев пользователя\n'
                   '2. Узнать список языков пользователя и репозитории, в которых они используются\n')
    if choice == 1:
        repo_info(get_repos())
    elif choice == 2:
        get_languages(repo_info(get_repos()))
    return 0


# Here the program gets the repository of the chosen user
def get_repos():
    user = input('Введите имя пользователя')
    url = 'https://api.github.com/users/%s/repos' % user
    token = 'ccb3a4b775d7e1a38f77fc97ac5496b9b2e16c86'
    headers = {'apikey': 'token %s' % token}
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


def get_languages(repo_name):
    user = input('Введите имя пользователя')
    token = ''  # insert your token
    headers = {'apikey': 'token %s' % token}
    i = 0
    data_languages = []
    while i < len(repo_name):
        url = 'https://api.github.com/repos/%s/' + repo_name[i] + '/languages' % user
        try:
            request = urllib.request.Request(url, headers=headers)
            response = urllib.request.urlopen(request)
            text = response.read().decode('utf-8')
            data = json.loads(text)
            data_languages.append(data)
            print(data_languages)
            return data_languages
        except urllib.error.URLError as e:
            print('A problem occurred: ' + str(e.reason))
