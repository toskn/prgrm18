from flask import Flask, request
app = Flask(__name__)


@app.route("/")
def hello():
    return """<html>
    <h1>
    <meta charset="utf-8">
    <title>Введите текст, мы посчитаем его длину</title>
<h1>
<body>
<form action="http://127.0.0.1:5000/result">
<p><b>Введите поисковый запрос</b></p>
<input type="textarea" name="text">
<p><input type="submit"></p>
</form>
</body>
</html>
"""


@app.route("/result")
def result():
    text = request.args['text']
    text = len(text)
    return "длина вашего текста " + str(text)


app.run()

