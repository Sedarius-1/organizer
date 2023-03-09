from datetime import date


class Uzytkownik:
    nazwa = ""
    haslo = ""

    def __init__(self, nazwa, haslo):
        self.nazwa = nazwa
        self.haslo = haslo


class Zadanie:
    id = 0
    przedmiot = ""
    nazwa_zadania = ""
    oddanie_data = ""
    ile_dni = 0

    def __init__(self, id, przedmiot, nazwa_zadania, oddanie_data, skonczone, przeslane):
        self.id = id
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
        if self.ile_dni < 0:
            return ""
        else:
            if self.przeslane == 1:
                return f"<div class='tile-sent'><p>" \
                       f"Task ID: {self.id}<br>" \
                       f"Subject: {self.przedmiot} <br>" \
                       f"Task: {self.nazwa_zadania} <br>" \
                       f"Finished!<br>" \
                       f"</p></div>"
            elif self.skonczone == 1:
                return f"<div class='tile-finished'><p>" \
                       f"Task ID: {self.id}<br>" \
                       f"Subject: {self.przedmiot} <br>" \
                       f"Task: {self.nazwa_zadania} <br>" \
                       f"Due date: {self.oddanie_data} <br>" \
                       f"Days until submission: {self.ile_dni} <br>" \
                       f"REMEMBER ABOUT SUBMISSING IT<br>" \
                       f"</p></div>"
            elif self.getDayDiff().days >= 7:
                return f"<div class='tile-unfinished'><p>" \
                       f"Task ID: {self.id}<br>" \
                       f"Subject: {self.przedmiot} <br>" \
                       f"Task: {self.nazwa_zadania} <br>" \
                       f"Due date: {self.oddanie_data} <br>" \
                       f"Days until submission: {self.ile_dni} <br>" \
                       f"</p></div>"
            else:
                return f"<div class='tile-urgent'><p>" \
                       f"Task ID: {self.id}<br>" \
                       f"Subject: {self.przedmiot} <br>" \
                       f"Task: {self.nazwa_zadania} <br>" \
                       f"Due date: {self.oddanie_data} <br>" \
                       f"Days until submission: {self.ile_dni} <br>" \
                       f"</p></div>"
