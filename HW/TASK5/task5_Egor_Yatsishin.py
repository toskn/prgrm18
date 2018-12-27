from flask import Flask, render_template, request
import sqlite3
from pymystem3 import Mystem
import re


app = Flask(__name__)
filename = 'news_info.csv'
m = Mystem()


def create_and_fill_db():
    i = 0
    conn = sqlite3.connect('db.sqlite')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS "
              "news(id, news_name, news_text, news_lemma, news_link)")
    with open(filename, encoding='utf-8') as file:
        file = file.read()
        file = file.split("\n")
        file.remove(file[0])
        while i + 1 < len(file):
            file_split = file[i].split(',')
            c.execute("INSERT INTO "
                      "news(news_name, news_text, news_lemma, news_link)"
                      " VALUES"
                      "(?, ?, ?, ?)",
                      (file_split[0], file_split[1],
                       file_split[2], file_split[3]))
            conn.commit()
            i += 1
    conn.close()
    return 0


def organised_set(seq):
    seen = set()
    seen_add = seen.add
    return tuple([x for x in seq if not (x in seen or seen_add(x))])


@app.route('/')
def main_page():
    return render_template('index.html')


@app.route('/result', methods=['POST'])
def result_page():
    conn = sqlite3.connect('db.sqlite')
    c = conn.cursor()
    template_nm = 'result.html'
    i = 0
    ii = 0
    a = 0
    news_results = []
    news_name_list = []
    news_text_list = []
    news_link_list = []
    position_list = []
    list_to_show = []
    list_of_dicts = []

    if request.method == 'POST':
        search = request.form['search']
        lemmas = m.lemmatize(search)
        lemmas = [x for x in lemmas if x != '\n']
        lemmas = [x for x in lemmas if x != ' ']
        lemmas = ' '.join(lemmas)
        lemmas = [lemmas]

        for element in lemmas:
            c.execute("SELECT news_lemma FROM main.news "
                      "WHERE news_lemma LIKE ?", ('% ' + element + ' %',))
            results = c.fetchall()
            if len(results) > 0:

                for element_results in results:
                    c.execute("SELECT news_name, news_text,"
                              " news_lemma, news_link"
                              " FROM main.news WHERE news_lemma=?",
                              (element_results[0],))
                    news_results.append(tuple(c.fetchall()))

                for object_of_results in news_results:
                    object_of_results = organised_set(tuple(object_of_results))
                news_results = list(organised_set(organised_set(news_results)))

                while i < len(news_results):
                    for item in news_results[i]:
                        position_full = \
                            re.search(r'\b(' + re.escape(element) + r')\b',
                                      item[2], re.IGNORECASE)
                        position = position_full.start()
                        position_list.append(int(position))
                    i += 1

                for row in news_results:
                        for row1 in row:
                                news_name_list.append(row1[0])
                                news_text_list.append(row1[1])
                                news_link_list.append(row1[3])
                news_name_list = list(organised_set(news_name_list))
                news_text_list = list(organised_set(news_text_list))
                news_link_list = list(organised_set(news_link_list))

                while ii < len(position_list):
                    while a < len(news_text_list):

                        if position_list[ii] <= 50 and \
                                position_list[ii]+50 <= len(news_text_list[a]):
                            list_to_show.append(
                                    news_text_list[a][0:position_list[ii]+50])

                        elif position_list[ii] >= 50 and \
                                position_list[ii]+50 >= len(news_text_list[a]):
                            list_to_show.append(news_text_list[a]
                                                [position_list[ii]-50:
                                                 len(news_text_list[a])])

                        elif position_list[ii] >= 50 and \
                                position_list[ii]+50 <= len(news_text_list[a]):
                            list_to_show.append(news_text_list[a]
                                                [position_list[ii]-50:
                                                 position_list[ii]+50])

                        elif position_list[ii] <= 50 and \
                                position_list[ii]+50 >= len(news_text_list[a]):
                            list_to_show.append(
                                news_text_list[a][0:len(news_text_list[a])])
                        a += 1
                    ii += 1
                i = 0
                while i < len(news_name_list):
                    list_of_dicts.append(dict(name=news_name_list[i],
                                              text=list_to_show[i],
                                              link=news_link_list[i]))
                    i += 1
            else:
                template_nm = 'nothing.html'
    conn.close()
    return render_template(template_nm,
                           list_of_dicts=list_of_dicts,
                           search=search)


if __name__ == '__main__':
    app.run(debug=True)
