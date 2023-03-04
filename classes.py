from datetime import date


class Uzytkownik:
    nazwa = ""
    haslo = ""

    def __init__(self, nazwa, haslo):
        self.nazwa = nazwa
        self.haslo = haslo


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
        if self.ile_dni < 0:
            return ""
        else:
            if self.przeslane == 1:
                return f"<div class='tile-sent'><p>" \
                       f"Przedmiot: {self.przedmiot} <br>" \
                       f"Zadanie: {self.nazwa_zadania} <br>" \
                       f"Zakończono!<br>" \
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
