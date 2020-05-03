import datetime
import calendar


def when_easter(year):
    a = year % 19
    b = int(year / 100)
    c = year % 100
    d = int(b / 4)
    e = b % 4
    f = int((b + 8) / 25)
    g = int((b - f + 1) / 3)
    h = (19 * a + b - d - g + 15) % 30
    i = int(c / 4)
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = int((a + 11 * h + 22 * l) / 451)
    p = (h + l - 7 * m + 114) % 31
    day = p + 1
    month = int((h + l - 7 * m + 114) / 31)

    return day, month


def polish_holidays(year):

    day, month = when_easter(year)

    wielkanoc = datetime.date(year, month, day)
    poniedzialek_wielkanocny = wielkanoc + datetime.timedelta(days=1)
    boze_cialo = wielkanoc + datetime.timedelta(days=60)
    nowy_rok = datetime.date(year, 1, 1)
    trzech_kroli = datetime.date(year, 1, 6)
    swieto_pracy = datetime.date(year, 5, 1)
    konstytucji_3maja = datetime.date(year, 5, 3)
    wniebowziecie = datetime.date(year, 8, 15)
    wszystkich_swietych = datetime.date(year, 11, 1)
    swieto_niepodleglosci = datetime.date(year, 11, 11)
    boze_narodzenie1 = datetime.date(year, 12, 25)
    boze_narodzenie2 = datetime.date(year, 12, 26)

    polish_holidays_list = {
        nowy_rok: "Nowy Rok",
        trzech_kroli: "Święto Trzech Króli",
        wielkanoc: "Wielkanoc",
        poniedzialek_wielkanocny: "Poniedziałek wielkanocny",
        swieto_pracy: "Święto Pracy",
        konstytucji_3maja: "Święto Konstytucji 3 Maja",
        boze_cialo: "Boże Ciało",
        wniebowziecie: "Wniebowzięcie NMP",
        wszystkich_swietych: "Dzień Wszystkich Świętych",
        swieto_niepodleglosci: "Święto Niepodległości",
        boze_narodzenie1: "Boże narodzienie",
        boze_narodzenie2: "Boże narodzenie (drugi dzień)",
    }
    return polish_holidays_list


def days_for_calendar(year):
    days_for_calendar = calendar.Calendar().yeardayscalendar(year)

    january = days_for_calendar[0][0]
    february = days_for_calendar[0][1]
    march = days_for_calendar[0][2]
    april = days_for_calendar[1][0]
    may = days_for_calendar[1][1]
    june = days_for_calendar[1][2]
    july = days_for_calendar[2][0]
    august = days_for_calendar[2][1]
    september = days_for_calendar[2][2]
    october = days_for_calendar[3][0]
    november = days_for_calendar[3][1]
    december = days_for_calendar[3][2]

    months_for_calendar = {
        "January": january,
        "February": february,
        "March": march,
        "April": april,
        "May": may,
        "June": june,
        "July": july,
        "August": august,
        "September": september,
        "October": october,
        "November": november,
        "December": december,
    }

    return months_for_calendar


def replace_polish_characters(word):
    polish_characters = {
        'ą':'a',
        'ć':'c',
        'ę':'e',
        'ł':'l',
        'ń':'n',
        'ó':'o',
        'ś':'s',
        'ź':'z',
        'ż':'Z',
        'Ą':'A',
        'Ć':'C',
        'Ę':'E',
        'Ł':'L',
        'Ń':'N',
        'Ó':'O',
        'Ś':'S',
        'Ź':'Z',
        'Ż':'Z',
    }
    new_word = ''
    for letter in word:
        new_letter = polish_characters.get(letter, letter)
        new_word += new_letter
    return new_word