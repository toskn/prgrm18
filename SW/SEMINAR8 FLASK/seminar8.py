from flask import Flask, url_for, render_template, request, redirect

app = Flask(__name__)


filename = 'README.csv'
with open(filename, encoding='utf-8') as file:
    file = file.read()
    file = file.split('\n')
i = 0
file_short = []
file_long = []
while i < len(file):
    file_short.append(file[i][-3:])
    i += 1
file_short.remove('')
i = 0
while i < len(file):
    file_long.append(file[i][:-4])
    i += 1
file_long.remove('')


@app.route("/")
def hello():
    content = file
    return """<html>
    <h1>
    <meta charset="utf-8">
    <title>Введите название языка</title>
</h1>
<body>
<form action="http://127.0.0.1:5000/short", method = 'GET'>
<p><b>Введите запрос</b></p>
    Аббревиатура: <input type="text" name="abb"><br>
    <p><input type="submit" value="Отправить"></p>
</form>
<form action="http://127.0.0.1:5000/long", method = 'GET'>
<p><b>Введите запрос</b></p>
    Название языка: <input type="text" name="full"><br>
    <p><input type="submit" value="Отправить"></p>
</form>
""" + render_template("stats.html", content=content)


@app.route('/short')
def lang_by_short(lang=None):
    error = None
    if request.method == 'GET':
        lang = str(request.args['abb'])
        if lang is None:
            error = 'No input'
        if lang not in file_short:
            error = "There's no language with such an abbreviation"
    else:
        a = file_short.index(lang)
        error = file_long[a]
    return error


@app.route('/long')
def lang_by_long(lang=None):
    error = None
    if request.method == 'GET':
        lang = request.args['full']
        if lang is None:
            error = 'No input'
        if lang not in file_long:
            error = "There's no language with such an abbreviation"
    else:
        a = file_long.index(lang)
        error = file_short[a]
    return error


if __name__ == '__main__':
    app.run(debug=True)

