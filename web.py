from flask import Flask, render_template, request, redirect, url_for

import classes
import queries
import tasks

app = Flask(__name__)
cursor = tasks.establishConnection()


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        uzytkownik = classes.Uzytkownik(request.form.get("name"), request.form.get("passwd"))
        result = queries.selectUserQuery(cursor, uzytkownik)
        if tasks.loginTry(uzytkownik, result[0][2]):
            return redirect(url_for('hello_world', uzytkownik=uzytkownik.nazwa))
        else:
            return render_template('login.html')


@app.route('/app/<uzytkownik>', methods=['GET', 'POST'])
def hello_world(uzytkownik):
    query_result = queries.getAllTasksQuery(cursor, uzytkownik)
    lista_zadan_sorted = tasks.prepareList(query_result)

    return render_template('layout.html', zadania=lista_zadan_sorted)


@app.route('/app/dodaj/<uzytkownik>', methods=['GET', 'POST'])
def add_task(uzytkownik):
    if request.method == "POST":
        zadanie = classes.Zadanie(request.form.get("przedmiot"), request.form.get("zadanie"), request.form.get("data"), 0, 0)
        queries.addTaskQuery(zadanie, cursor, tasks.databaseConnector())
    return redirect(url_for('hello_world', uzytkownik=uzytkownik))


if __name__ == '__main__':
    app.run(debug=True)
