import urllib.request
import urllib.error
import json
import re


# Here the program gets the repository of the chosen user
def get_repos():
    user = input('Введите имя пользователя')
    url = 'https://api.github.com/users/%s/repos' % user
    token = 'b02538ca223cdc7465f127b059d57b35aff50a99'
    headers = {'apikey': 'token %s' % token}
    try:
        request = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(request)
        text = response.read().decode('utf-8')  # читаем ответ в строку
        data = json.loads(text)
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
    print(repo_descr)
    while i < len(repo_descr):
        repo_descr[i] = regdescr1.sub('', repo_descr[i])
        repo_descr[i] = repo_descr[i][:-9]
        i += 1
    print(repo_descr)
    i = 0
    while i < len(repo_name):
        repo_name[i] = repo_name[i][9:-15]
        i += 1
    print(repo_name)
    return repo_name


repo_info(get_repos())
