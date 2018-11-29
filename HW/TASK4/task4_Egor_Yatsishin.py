from flask import Flask, render_template, request
import csv
import json

app = Flask(__name__)
filename = 'results.csv'


@app.route('/')
def main_page():
    return render_template("index.html")


@app.route('/thanks', methods=['POST'])
def save_to_csv():
    if request.method == 'POST':
        ask = request.form['ask']
        what = request.form['what']
        how = request.form['how']
        name = request.form['name']
        surname = request.form['surname']
        fin_form = 'Спасибо за ваш ответ!'
        fieldnames = ['ask', 'what', 'how', 'name', 'surname']
        with open(filename, 'a+', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({'ask': ask, 'what': what, 'how': how,
                             'name': name, 'surname': surname})
        return render_template("thanks.html", fin_form=fin_form)


@app.route('/stats')
def show_stats():
    with open(filename, 'r', encoding='utf-8') as content:
        content = csv.reader(content)
        return render_template("stats.html", content=content)


@app.route('/json')
def json_maker():
    dict_csv = {}
    fieldnames = ['ask', 'what', 'how', 'name', 'surname']
    with open(filename, 'r+', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=fieldnames)
        for row in reader:
            name = row['name'] + ' ' + row['surname']
            dict_csv[name] = json.loads(json.dumps(row))
    return render_template("json.html", json=dict_csv)


@app.route('/search')
def do_search():
    return render_template("search.html")


@app.route('/result', methods=['POST'])
def show_result():
    dict_csv = {}
    if request.method == 'POST':
        ask = request.form['ask_search']
        what = request.form['what_search']
        fieldnames = ['ask', 'what', 'how', 'name', 'surname']
        with open(filename, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=fieldnames)
            for row in reader:
                if row['ask'] == ask:
                    if (row['what'] == what or row['how'] == what or
                            row['name'] == what or row['surname'] == what):
                        name = row['name'] + ' ' + row['surname']
                        dict_csv[name] = json.loads(json.dumps(row))
        return render_template("result.html", result=dict_csv)


if __name__ == '__main__':
    app.run(debug=True)
