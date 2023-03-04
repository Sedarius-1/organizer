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
        lista_zadan.append(classes.Zadanie(przedmiot=x[1], nazwa_zadania=x[2], oddanie_data=x[3], skonczone=int(x[4]),
                                           przeslane=int(x[5])))

    lista_zadan.sort(key=lambda poj_zadanie: poj_zadanie.ile_dni)
    for zadanie in lista_zadan:
        result += zadanie.sendStatement()
    return result


def loginTry(uzytkownik, database_hash):
    stored_password = bcrypt.hashpw(database_hash.encode(), bcrypt.gensalt())

    input_password = uzytkownik.haslo.encode()

    return hmac.compare_digest(bcrypt.hashpw(input_password, stored_password), stored_password)
