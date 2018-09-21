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


def temp_and_clouds(html):
    final_temp = []
    regtemp = re.compile('<div class="forecast-briefly__name">Сегодня</div>.*?'
                         '<div class="forecast-briefly__condition">Ясно</div>', re.DOTALL)
    temp = regtemp.findall(html)
    regtag = re.compile('<.*?>', re.DOTALL)
    regword = re.compile(r'[^\x00-\x7F\x80-\xFF\u0100-\u017F\u0180-\u024F\u1E00-\u1EFF]')
    regdate = re.compile(r'\d.*?[.]', re.DOTALL)
    for i in temp:
        clean_temp = regtag.sub('', i)
        clean_temp = regword.sub('', clean_temp)
        clean_temp = regdate.sub('', clean_temp)
        final_temp.append(clean_temp)
        print(final_temp)


temp_and_clouds(downloading_page())
