import urllib.request
import urllib.error
import re


def downloading_page():
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
    try:
        req = urllib.request.Request('https://yandex.ru/pogoda/moscow/', headers={'User-Agent': user_agent})
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
            return html
    except urllib.error.URLError as e:
        print(e.reason)


def temp_and_cloud(html):
    # The part about the temperature
    final_temp = []
    regtemp = re.compile('Сегодня</div>.*?</a></div>', re.DOTALL)
    temp = regtemp.findall(html)
    regtag = re.compile('<.*?>', re.DOTALL)
    regword = re.compile(r'[^\x00-\x7F\x80-\xFF\u0100-\u017F\u0180-\u024F\u1E00-\u1EFF]')  # nothing except Latin
    regdate = re.compile(r'\d.*?[.]', re.DOTALL)
    # Actually, i could just slice the important part, but i practiced re.
    for i in temp:
        clean_temp = regtag.sub('', i)
        clean_temp = regword.sub('', clean_temp)
        clean_temp = regdate.sub('', clean_temp)
        final_temp.append(clean_temp)
        print('Температура днём: ' + str(final_temp[0][0:4]) + '\n' + 'Температура ночью: ' + str(final_temp[0][4:]))

    # The part about the clouds
    final_cloud = []
    cloud = regtemp.findall(html)
    for i in cloud:
        clean_cloud = regtag.sub('', i)
        final_cloud.append(clean_cloud)
        print('Облачность: ' + str(final_cloud[0][32:]))


temp_and_cloud(downloading_page())
