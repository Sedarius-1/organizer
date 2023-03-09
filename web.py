from flask import Flask, render_template, request, redirect, url_for

import classes
import queries
import tasks

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        return render_template('register.html')
    if request.method == "POST":
        hashed = tasks.hashPassword(request.form.get("rejestracja_haslo"))
        queries.registerQuery(request.form.get("rejestracja_uzytkownik"), hashed[0], hashed[1])
        return render_template('login.html')
    else:
        return "nie dziala"


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template('login.html')
    if request.method == "POST":
        uzytkownik = classes.Uzytkownik(request.form.get("name"), request.form.get("passwd"))
        result = queries.selectUserQuery(uzytkownik)
        if tasks.loginTry(uzytkownik, result[0][2], result[0][3]):
            return redirect(url_for('hello_world', uzytkownik=uzytkownik.nazwa))
        else:
            return render_template('login.html')


@app.route('/app/<uzytkownik>', methods=['GET', 'POST'])
def hello_world(uzytkownik):
    query_result = queries.getAllTasksQuery(uzytkownik)
    lista_zadan_sorted = tasks.prepareList(query_result)

    return render_template('layout.html', zadania=lista_zadan_sorted[0])


@app.route('/app/dodaj/<uzytkownik>', methods=['GET', 'POST'])
def add_task(uzytkownik):
    if request.method == "POST":
        query_result = queries.getAllTasksQuery(uzytkownik)
        lista_zadan_sorted = tasks.prepareList(query_result)
        zadanie = classes.Zadanie(id=(lista_zadan_sorted[1] + 1), przedmiot=request.form.get("przedmiot"),
                                  nazwa_zadania=request.form.get("zadanie"), oddanie_data=request.form.get("data"),
                                  skonczone=0, przeslane=0)
        queries.addTaskQuery(zadanie, uzytkownik)
    return redirect(url_for('hello_world', uzytkownik=uzytkownik))


@app.route('/app/usun/<uzytkownik>', methods=['GET', 'POST'])
def remove_task(uzytkownik):
    if request.method == "POST":
        queries.removeTaskQuery(request.form.get("id_zadania"), uzytkownik)
        return redirect(url_for('hello_world', uzytkownik=uzytkownik))
    else:
        return "nie dziala"


@app.route('/app/zakoncz/<uzytkownik>', methods=['GET', 'POST'])
def finish_task(uzytkownik):
    if request.method == "POST":
        queries.finishTaskQuery(request.form.get("id_zadania_koniec"), uzytkownik)
        return redirect(url_for('hello_world', uzytkownik=uzytkownik))
    else:
        return "nie dziala"


@app.route('/app/wyslij/<uzytkownik>', methods=['GET', 'POST'])
def send_task(uzytkownik):
    if request.method == "POST":
        queries.sendTaskQuery(request.form.get("id_zadania_wyslanie"), uzytkownik)
        return redirect(url_for('hello_world', uzytkownik=uzytkownik))
    else:
        return "nie dziala"


if __name__ == '__main__':
    app.run(debug=True)
