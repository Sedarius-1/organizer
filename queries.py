import password_base


def getAllTasksQuery(database_cursor, uzytkownik):
    database_cursor.execute(f"use {password_base.user}")
    database_cursor.execute(f"SELECT * FROM lista_zadan where user_id='{uzytkownik}'")
    result = database_cursor.fetchall()
    return result


def selectUserQuery(database_cursor, uzytkownik):
    database_cursor.execute(f"use {password_base.user}")
    database_cursor.execute(f"SELECT * FROM uzytkownicy WHERE NAZWA='{uzytkownik.nazwa}'")
    result = database_cursor.fetchall()
    return result


def addTaskQuery(zadanie, database_cursor, database, uzytkownik):
    database_cursor.execute(f"use {password_base.user}")
    database_cursor.execute(
        f"INSERT INTO lista_zadan (przedmiot, nazwa_zadania, oddanie_data, skonczone,przeslane,user_id) VALUES ('{zadanie.przedmiot}','{zadanie.nazwa_zadania}','{zadanie.oddanie_data}','0','0','{uzytkownik}')")
    database.commit()