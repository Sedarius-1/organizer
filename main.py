from datetime import date

import mysql.connector
import password_base

class Uzytkownik:
    nazwa = ""
    haslo = ""

    def __init__(self, nazwa, haslo):
        self.nazwa = nazwa
        self.haslo = haslo

    def logTry(self, nazwa, haslo):
        if nazwa == self.nazwa and haslo == self.haslo:
            return True
        else:
            return False


class Zadanie:
    przedmiot = ""
    nazwa_zadania = ""
    oddanie_data = ""
    ile_dni = 0

    def __init__(self, przedmiot, nazwa_zadania, oddanie_data, skonczone, przeslane):
        self.przedmiot = przedmiot
        self.nazwa_zadania = nazwa_zadania
        self.oddanie_data = oddanie_data
        self.ile_dni = self.getDayDiff().days
        self.skonczone = skonczone
        self.przeslane = przeslane

    def parseDate(self):
        data = self.oddanie_data.split('-')
        return date(year=int(data[0]), month=int(data[1]), day=int(data[2]))

    def getDayDiff(self):
        return self.parseDate() - date.today()

    def sendStatement(self):
        if self.ile_dni<0:
            return ""
        else:
            if self.przeslane == 1:
                return f"<div class='tile-sent'><p>" \
                       f"Przedmiot: {self.przedmiot} <br>" \
                       f"Zadanie: {self.nazwa_zadania} <br>" \
                       f"Zakończono!<br>"\
                       f"</p></div>"
            elif self.skonczone == 1:
                return f"<div class='tile-finished'><p>" \
                       f"Przedmiot: {self.przedmiot} <br>" \
                       f"Zadanie: {self.nazwa_zadania} <br>" \
                       f"Data oddania: {self.oddanie_data} <br>" \
                       f"Do oddania zostało: {self.ile_dni} dni.<br>" \
                       f"PAMIĘTAJ O WYSŁANIU<br>" \
                       f"</p></div>"
            elif self.getDayDiff().days > 14:
                return f"<div class='tile-unfinished'><p>" \
                       f"Przedmiot: {self.przedmiot} <br>" \
                       f"Zadanie: {self.nazwa_zadania} <br>" \
                       f"Data oddania: {self.oddanie_data} <br>" \
                       f"Do oddania zostało: {self.ile_dni} dni.<br>" \
                       f"</p></div>"
            else:
                return f"<div class='tile-urgent'><p>" \
                   f"Przedmiot:{self.przedmiot} <br>" \
                   f"Zadanie: {self.nazwa_zadania} <br>" \
                   f"Data oddania: {self.oddanie_data} <br>" \
                   f"Do oddania zostało: {self.ile_dni} dni.<br>" \
                   f"</p></div>"



mydb = mysql.connector.connect(
    host=password_base.host,
    user=password_base.user,
    password=password_base.password
)


def establishConnection():
    my_database = mysql.connector.connect(
        host=password_base.host,
        user=password_base.user,
        password=password_base.password
    )
    return my_database


def fetchDays(my_database, uzytkownik):
    mycursor = my_database.cursor()
    mycursor.execute("use sql7602526")
    mycursor.execute(f"SELECT * FROM lista_zadan where user_id='{uzytkownik}'")
    myresult = mycursor.fetchall()
    return myresult


def prepareList(myresult):
    lista_zadan = []
    result=""
    for x in myresult:
        lista_zadan.append(Zadanie(przedmiot=x[1], nazwa_zadania=x[2], oddanie_data=x[3], skonczone=int(x[4]), przeslane=int(x[5])))

    lista_zadan.sort(key=lambda poj_zadanie: poj_zadanie.ile_dni)
    for zadanie in lista_zadan:
        result += zadanie.sendStatement()
    return result

# for zadanie in listaZadan:
#     print(zadanie.getData())
