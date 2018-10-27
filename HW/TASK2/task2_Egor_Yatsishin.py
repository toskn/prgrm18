import urllib.request
import urllib.error
import json
import re
import sys

# elif choice == '4':
# repo_name, data = repo_info2(language_popular_data())
# languages_sort2(get_languages2(repo_name, data), data)
user = input('Введите имя пользователя')  # в чате в телеграме Ростислав Алексеевич разрешил не использовать список
#  для этого задания, хотя в критериях оценки осталась старая формулировка. Да, из-за того, что я не работал изначально
#  с предложенным списком  некоторые функции пришлось заводить несколько раз, нет общей функции для получения "data",
#  но ничего, в следующий раз я не буду заниматься таким.
token = ''  # insert your token
user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
headers = {'User-Agent': user_agent, 'Authorization': 'token %s' % token}


def choose_func():
    choice = input('Введите номер той функции из списка, которую хотите использовать:\n'
                   '1. Узнать названия и описания репозиториев пользователя\n'
                   '2. Узнать список языков пользователя и репозитории, в которых они используются\n'
                   '3. Узнать у кого из пользователей, в заложенном в программу списке, больше всего репозиториев\n'
                   '4. Узнать самый популярный язык среди пользователей из списка\n'
                   '5. Узнать у кого из пользователей, в заложенном в программу списке, больше всего подписчиков\n')
    if choice == '1':
        repo_info(get_repos())
    elif choice == '2':
        repo_name, data = repo_info1(get_repos1())
        languages_sort(get_languages(repo_name, data), data)
    elif choice == '3':
        repo_amount()
    elif choice == '4':
        most_common(languages_sort2(get_languages2(language_popular_data())))
    elif choice == '5':
        most_followers()
    elif choice != '1' and choice != '2' and choice != '3' and choice != '4' and choice != '5':
        sys.exit("Такая функция отсутствует. Перезапустите программу.")

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
    # Nearly everything that repo_info does can be done in another way basing on JSON dicts.
    # languages = []
    # for i in data:
    # print(i['name'], i['description'])
    # languages.append(i['language']) - this is the only difference.
    # By using dicts we only get to work with a single language.


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


def get_languages2(repo_name_full):
    i = 0
    ii = 0
    data_languages = []
    users = ['lizaku', 'elmiram', 'maryszmary', 'nevmenandr', 'ancatmara', 'roctbb', 'akutuzov', 'agricolamz',
             'lehkost', 'kylepjohnson', 'mikekestemont', 'demidovakatya', 'shwars', 'JelteF', 'timgraham',
             'arogozhnikov', 'jasny', 'bcongdon', 'whyisjake', 'gvanrossum']
    while i < len(users):
        while ii < len(repo_name_full[i]):
            url = 'https://api.github.com/repos/' + str(users[i]) + '/' + str(repo_name_full[i][ii]) + '/languages'
            try:
                request = urllib.request.Request(url, headers=headers)
                response = urllib.request.urlopen(request)
                text = response.read().decode('utf-8')
                data = json.loads(text)
                data_languages.append(data)
            except urllib.error.URLError as e:
                print('A problem occurred: ' + str(e.reason))
                sys.exit()
            ii += 1
        i += 1
    return data_languages


def languages_sort2(data_languages):
    i = 0
    lang_clear = []
    lang_list = []
    while i < len(data_languages):
        a = re.findall(r'(?<=\')([a-zA-z]*)(?=\')', str(data_languages[i]))
        lang_list.append(a)
        for key in data_languages[i]:
            lang_clear.append(key)
        i += 1
    return lang_clear


def most_common(lang_clear):
    print('Самый популярный язык: ' + str(max(set(lang_clear), key=lang_clear.count)))
    return 0


def repo_amount():
    users = ['lizaku', 'maryszmary', 'elmiram', 'nevmenandr', 'ancatmara', 'roctbb', 'akutuzov', 'agricolamz',
             'lehkost', 'kylepjohnson', 'mikekestemont', 'demidovakatya', 'shwars', 'JelteF', 'timgraham',
             'arogozhnikov', 'jasny', 'bcongdon', 'whyisjake', 'gvanrossum']

    i = 0
    biggest = 0
    biggest_user = ''
    regname = re.compile("'name':(.*?), 'full_name':", re.DOTALL)
    reglicense = re.compile(", 'license'.*?}")
    repo_count = {}
    while i < len(users):
        # github api is too complicated to make a switch between pages, so the max amount of repos is set as 100
        # if there's more than 1 user having 100+ repos, then the first in the list is displayed
        url = 'https://api.github.com/users/%s/repos?per_page=100' % users[i]
        try:
            request = urllib.request.Request(url, headers=headers)
            response = urllib.request.urlopen(request)
            text = response.read().decode('utf-8')
            data = json.loads(text)
            repo_name = reglicense.sub('}', str(data))
            repo_name = regname.findall(repo_name)
            repo_len = len(repo_name)
            repo_count.update({users[i]: repo_len})
            i += 1
        except urllib.error.URLError as e:
            print('A problem occurred: ' + str(e.reason))
            sys.exit()
    i = 0
    while i < len(repo_count):
        if repo_count[users[i]] > biggest:
            biggest = repo_count[users[i]]
            biggest_user = users[i]
        i += 1
    print('Больше всех репозиториев у ' + str(biggest_user))


def language_popular_data():
    users = ['lizaku', 'elmiram', 'maryszmary', 'nevmenandr', 'ancatmara', 'roctbb', 'akutuzov', 'agricolamz',
             'lehkost', 'kylepjohnson', 'mikekestemont', 'demidovakatya', 'shwars', 'JelteF', 'timgraham',
             'arogozhnikov', 'jasny', 'bcongdon', 'whyisjake', 'gvanrossum']
    i = 0
    repo_name_full = []
    regname = re.compile("'name':(.*?), 'full_name':", re.DOTALL)
    reglicense = re.compile(", 'license'.*?}")
    while i < len(users):
        url = 'https://api.github.com/users/%s/repos' % users[i]
        try:
            request = urllib.request.Request(url, headers=headers)
            response = urllib.request.urlopen(request)
            text = response.read().decode('utf-8')
            data = json.loads(text)
            repo_name = reglicense.sub('}', str(data))
            repo_name = regname.findall(repo_name)
            i += 1
            ii = 0
            while ii < len(repo_name):
                repo_name[ii] = repo_name[ii][2:-1]
                ii += 1
            repo_name_full.append(repo_name)
        except urllib.error.URLError as e:
            print('A problem occurred: ' + str(e.reason))
            sys.exit()
    return repo_name_full


def most_followers():
    users = ['lizaku', 'elmiram', 'maryszmary', 'nevmenandr',
             'ancatmara', 'roctbb', 'akutuzov', 'agricolamz',
             'lehkost', 'kylepjohnson', 'mikekestemont', 'demidovakatya', 'shwars', 'JelteF', 'timgraham',
             'arogozhnikov', 'jasny', 'bcongdon', 'whyisjake', 'gvanrossum']
    i = 0
    biggest = 0
    biggest_user = ''
    reglogin = re.compile('login')
    log_count = {}
    while i < len(users):
        url = 'https://api.github.com/users/%s/followers?per_page=100' % users[i]
        # actually tried to invent smth simple to use &page=i, but failed
        try:
            request = urllib.request.Request(url, headers=headers)
            response = urllib.request.urlopen(request)
            text = response.read().decode('utf-8')
            data = json.loads(text)
            logins = reglogin.findall(str(data))
            log_len = len(logins)
            log_count.update({users[i]: log_len})
            i += 1
        except urllib.error.URLError as e:
            print('A problem occurred: ' + str(e.reason))
            sys.exit()
    i = 0
    while i < len(log_count):
        if log_count[users[i]] > biggest:
            biggest = log_count[users[i]]
            biggest_user = users[i]
        i += 1
    print('Больше всех подпичиков у ' + str(biggest_user))


choose_func()
