import requests
from bs4 import BeautifulSoup
import re
import time

# программа сейчас не работает, потому что мне не хватило времени ее доделать. В целом, если запустить
# get_news(get_links(page_data(navigation(year, month, page, s))), s)
# то все выкачивается с заданой параметрами year, month, page страницы.
# find_last_page, page_scroller и extended_navigation должны были расширить функицонал
# до выкачивания всей новостной информации из архива сайта http://vpered-balezino.ru/, но что-то в них пошло не так.
# Мне кажется, что проблема в том, что при выкачивании страницы данные разибиты какими-то странными пробелами,
# если их убрать, то регулярки все ищут, а с ними не ищут. Проблема в том, что я не успел определить что это.


# establishing session
s = requests.Session()
s.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'})


def navigation(year, month, page, session):
    url = 'http://vpered-balezino.ru/%d/%d/page/%d' % (year, month, page)
    request = session.get(url)
    return request.text


def page_data(text):
    soup = BeautifulSoup(text, 'html.parser')
    link_list = soup.findAll('div', {'class': 'td-read-more'})
    link_list = [x for x in link_list if x != link_list[-1]]  # deleting the ESHE buttons
    return link_list


def get_links(link_list):
    i = 0
    news_link = []
    while i < len(link_list):
        news_link.append(str(link_list[i])[36:-22])
        i += 1
    return news_link


def get_news(news_link, session):
    i = 0
    news_list = []
    regtag = re.compile('<.*?>', re.DOTALL)
    regn = re.compile('\n')
    while i < len(news_link):
        request = session.get(news_link[i])
        news_list.append(request.text)
        soup = BeautifulSoup(news_list[i], 'html.parser')
        news_list[i] = soup.findAll('div', {'class': 'td-post-content'})
        news_list[i] = regtag.sub('', str(news_list[i]))
        news_list[i] = news_list[i][2:-3]
        news_list[i] = regn.sub(' ', str(news_list[i]))
        news_list[i] = news_list[i].replace(u'\xa0', u' ')
        i += 1
    return news_list


def find_last_page(text):
    soup = BeautifulSoup(text, 'html.parser')
    last_page = soup.findAll('div', {'id': 'td_uid_12_58c1bfc115967'})
    regtag = re.compile('<.*?>', re.DOTALL)
    regn = re.compile('\n')
    print(last_page)
    last_page = regtag.sub('', str(last_page))
    print(last_page)
    last_page = last_page[2:-3]
    print(last_page)
    last_page = regn.sub(' ', str(last_page))
    print(last_page)
    last_page = last_page.replace(u'\xa0', u' ')
    if last_page != '':
        page_format = 'not last'
    else:
        page_format = 'last'
    return page_format


def page_scroller(year, month, page, news_list_full):
    while find_last_page(navigation(year, month, page, s)) != 'last':
        news_list_full.append(get_news(get_links(page_data(navigation(year, month, page, s))), s))
        time.sleep(2)
        page += 1
    return news_list_full


def extended_navigation():
    year = 2017
    month = 8
    page = 1
    news_list_full = []
    while year <= 2018 or month <= 10:
        page_scroller(year, month, page, news_list_full)
        if month == 12:
            month = 1
            year += 1
        else:
            month += 1
    print(news_list_full)
    return news_list_full


extended_navigation()

# get_news(get_links(page_data(navigation(year, month, page, s))), s)
