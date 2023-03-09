import hmac

import bcrypt
import mysql.connector
import password_base
import classes


def databaseConnector():
    my_database = mysql.connector.connect(
        host=password_base.host,
        user=password_base.user,
        password=password_base.password
    )
    return my_database


def establishConnection():
    database_cursor = databaseConnector().cursor()
    return database_cursor


def prepareList(myresult):
    lista_zadan = []
    result = ""
    for x in myresult:
        lista_zadan.append(
            classes.Zadanie(id=x[0], przedmiot=x[1], nazwa_zadania=x[2], oddanie_data=x[3], skonczone=int(x[4]),
                            przeslane=int(x[5])))
    lista_zadan.sort(key=lambda poj_zadanie: poj_zadanie.id)
    if len(lista_zadan)>0:
        najw_index = lista_zadan[-1].id
    else:
        najw_index = 0
    lista_zadan.sort(key=lambda poj_zadanie: poj_zadanie.ile_dni)
    for zadanie in lista_zadan:
        result += zadanie.sendStatement()
    return result, najw_index


def loginTry(uzytkownik, stored_password, salt):
    # salt = bcrypt.gensalt()
    # stored_password = bcrypt.hashpw(database_hash.encode(), salt)
    # print(stored_password)
    # stored_password = database_hash
    input_password = bcrypt.hashpw(uzytkownik.haslo.encode(), salt.encode())

    return hmac.compare_digest(input_password, stored_password.encode())


def hashPassword(haslo):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(haslo.encode(), salt)
    return hashed_password, salt
