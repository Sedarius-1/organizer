import hmac

from flask import Flask, render_template, request, redirect, url_for
import main
import bcrypt

app = Flask(__name__)
database = main.establishConnection()


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        uzytkownik = main.Uzytkownik
        uzytkownik.nazwa = request.form.get("name")
        uzytkownik.haslo = request.form.get("passwd")
        uzytkownik.haslo = uzytkownik.haslo
        cursor = database.cursor()
        cursor.execute("use sql7602526")
        cursor.execute(f"SELECT * FROM uzytkownicy WHERE NAZWA='{uzytkownik.nazwa}'")
        result = cursor.fetchall()

        stored_password = bcrypt.hashpw(result[0][2].encode(), bcrypt.gensalt())

        input_password = uzytkownik.haslo.encode()

        if hmac.compare_digest(bcrypt.hashpw(input_password, stored_password), stored_password):
            return redirect(url_for('hello_world', uzytkownik=uzytkownik.nazwa))
        else:
            return render_template('login.html')
        # return f"NAZWA: {uzytkownik.nazwa}, HASŁO: {uzytkownik.haslo}"
    return render_template('login.html')


@app.route('/app/<uzytkownik>', methods=['GET', 'POST'])
def hello_world(uzytkownik):
    query_result = main.fetchDays(database, uzytkownik)
    lista_zadan_sorted = main.prepareList(query_result)

    return render_template('layout.html', zadania=lista_zadan_sorted)


@app.route('/app/dodaj/<uzytkownik>', methods=['GET', 'POST'])
def add_task(uzytkownik):
    if request.method == "POST":
        cursor = database.cursor()
        cursor.execute("use sql7602526")
        zadanie = main.Zadanie
        zadanie.przedmiot = request.form.get("przedmiot")
        zadanie.nazwa_zadania = request.form.get("zadanie")
        zadanie.oddanie_data = request.form.get("data")
        cursor.execute(f"INSERT INTO lista_zadan (przedmiot, nazwa_zadania, oddanie_data, skonczone,przeslane,user_id) VALUES ('{zadanie.przedmiot}','{zadanie.nazwa_zadania}','{zadanie.oddanie_data}','0','0','{uzytkownik}')")
        database.commit()
    return redirect(url_for('hello_world', uzytkownik=uzytkownik))


if __name__ == '__main__':
    app.run(debug=True)
