import urllib.request
import urllib.error
import json
import re
import sys
# cbd?

user = input('Введите имя пользователя')  # в чате в телеграме Ростислав Алексеевич разрешил не использовать список
# для этого задания, хотя в критериях оценки осталась старая формулировка
token = '3e57825d4d8ec8f948d9a0dthc7c0797a953737d'  # insert your token
headers = {'apikey': 'token %s' % token}


def choose_func():

    choice = input('Введите номер той функции из списка, которую хотите исползовать:\n'
                   '1. Узнать названия и описания репозиториев пользователя\n'
                   '2. Узнать список языков пользователя и репозитории, в которых они используются\n'
                   '3. Узнать у кого из пользователей, в заложенном в программу списке, больше всего репозиториев\n')
    if choice == '1':
        repo_info(get_repos())
    elif choice == '2':
        repo_name, data = repo_info1(get_repos1())
        languages_sort(get_languages(repo_name, data), data)
    elif choice == '3':
        repo_amount()
    # elif choice == 4:

    elif choice != '1' and choice != '2' and choice != '3' and choice != '4':
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
        sys.exit()


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
        sys.exit()


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
    # Everything that repo_info does can be done in another way basing on JSON dicts.
    # languages = []
    # for i in data:
    # print(i['name'], i['description'])
    # languages.append(i['language'])


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
        except urllib.error.URLError as e:
            print('A problem occurred: ' + str(e.reason))
            sys.exit()
    return data_languages


def languages_sort(data_languages, data):
    i = 0
    ii = 0
    lang_clear = []
    lang_list = []
    while i < len(data_languages):
        a = re.findall(r'(?<=\')([a-zA-z]*)(?=\')', str(data_languages[i]))
        lang_list.append(a)
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
        i += 1
    print('\nПользователь ' + str(user) + ' пишет на ' + str_lang)
    for i in data:
        repo_list = [i['name']]
        print('В репозитории ' + str(repo_list[0]) + ' используются языки:')
        while ii < len(lang_list):
            if lang_list[ii] == '[]':
                print('None')
            else:
                print(lang_list[ii])
            ii += 1
            break
    # честно говоря, так и не понял какого формата вывода от нас ожидали на использование языков -
    # количество или какой язык в каком репозитории, но в итоге полученная информация сходна с той, что в примере.
    return 0


def repo_amount():
    users = ['elmiram', 'maryszmary', 'lizaku', 'nevmenandr', 'ancatmara', 'roctbb', 'akutuzov', 'agricolamz',
             'lehkost', 'kylepjohnson', 'mikekestemont', 'demidovakatya', 'shwars', 'JelteF', 'timgraham',
             'arogozhnikov', 'jasny', 'bcongdon', 'whyisjake', 'gvanrossum']
    i = 0
    ii = 0
    biggest = 0
    biggest_user_num = 0
    regname = re.compile("'name':.*?, 'full_name':", re.DOTALL)
    reglicense = re.compile(", 'license'.*?}")
    repo_count = []
    while i < len(users):
        url = 'https://api.github.com/users/%s/repos' % users[i]
        try:
            request = urllib.request.Request(url, headers=headers)
            response = urllib.request.urlopen(request)
            text = response.read().decode('utf-8')
            data = json.loads(text)
            repo_name = reglicense.sub('}', str(data))
            repo_name = regname.findall(repo_name)
            while ii < len(repo_name):
                repo_name[ii] = repo_name[ii][9:-15]
                ii += 1
            repo_count.append(repo_name)
            i += 1
        except urllib.error.URLError as e:
            print('A problem occurred: ' + str(e.reason))
            sys.exit()
    i = 0
    while i < len(repo_count):
        if len(repo_count[i]) > biggest:
            biggest = len(repo_count[i])
            biggest_user_num = i
        i += 1
        biggest_user = users[biggest_user_num]
        print('Больше всех репозиториев у ' + str(biggest_user))


choose_func()
