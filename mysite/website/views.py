import re

from django.shortcuts import render
from django.utils.safestring import mark_safe
from geopy.geocoders import Nominatim
import json
import datetime
import calendar

cities = []


class CustomHTMLCal(calendar.HTMLCalendar):
    cssclasses = ["lun", "mar", "mie", "jue", "vie", "sab", "dom"]
    cssclass_month_head = "text-center month-head"
    cssclass_month = "text-center month"
    cssclass_year = "text-italic lead"


def normalize(s):
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
        ("Á", "A"),
        ("É", "E"),
        ("Í", "I"),
        ("Ó", "O"),
        ("Ú", "U"),
    )
    for a, b in replacements:
        s = s.replace(a, b).replace(a.upper(), b.upper())
    return s


def find_holiday(city):
    # We're trying to found the city in the json scrapped
    # The function will return a dict with 'month':('holidays')
    # non if city is not found
    f = open('holidays_spain.json', "r")

    # Reading from file
    data = json.loads(f.read())
    f.close()

    global cities
    cities = []
    ret = None
    for key in data:
        cities = cities + [key, ]
        if normalize(str(key).upper()) == str(city).upper():
            now = datetime.datetime.now()
            ret = data[key]
    return ret


def getcity(long, lat):
    # this function will return the name of the city from coordinates given by navigator
    # initialize Nominatim API
    geolocator = \
        Nominatim(user_agent="geoapiExercises")
    # latitude & longitude input
    latitude = lat
    longitude = long

    location = geolocator.reverse(latitude + "," + longitude)

    # Display
    address = location.raw['address']

    # traverse the data
    city = address.get('city', '')
    state = address.get('state', '')
    country = address.get('country', '')
    code = address.get('country_code')
    zipcode = address.get('postcode')
    return city


def index(request):
    return render(request, "website/locate_all.html")


def locate_get(request):
    location = request.GET
    city = ""
    if 'city' in location:
        city = location['city']
    else:
        city = getcity(location['long'], location['lat'])
    result = find_holiday(normalize(city))
    result = {int(k): v for k, v in result.items()}

    now = datetime.datetime.now()
    year = now.year
    month = now.month
    day = now.day

    next_holiday = 0
    print(result[month])
    if not result[month] == []:
        next_holiday = max(result[month])
        next_month_hol = month

    if int(next_holiday) <= day and not month == 12:
        for i in range(month + 1, 12):
            if not result[i] == []:
                next_holiday = min(result[i])
                next_month_hol = i
                break
    elif month == 12 and day >= 25:
        next_holiday = 1
        next_month_hol = 1

    cal = CustomHTMLCal() # init
    str_cal = change_lang(cal.formatmonth(year, month)) # change lang
    str_cal = class_holiday(str_cal, result[month]) # modify holidays classes

    return render(request, "website/locate_get.html", {
        "city": city,
        "holiday": str(day) in result[month],
        "next_hol": str(next_holiday) + "/" + str(next_month_hol),
        "cities": sorted(cities),
        "cal": mark_safe(str_cal)
    })


def holiday(request):
    return render(request, "website/holiday.html")


def class_holiday(html_string, holidays):
    print(holidays)
    for i in holidays:
        pattern = r'(<td class="[a-z]{3}">' + str(i) + '<\/td>)'
        x = re.search(pattern, html_string)
        new_class = (x.group(0).split('">', 1)[0] + ' bg-danger" >' + x.group(0).split('">', 1)[1])
        html_string = html_string.replace(x.group(0), new_class)
    return html_string


def change_lang(str_cal):
    str_cal = str_cal.replace("mon", "lu")
    str_cal = str_cal.replace("Mon", "Lu")
    str_cal = str_cal.replace("tue", "ma")
    str_cal = str_cal.replace("Tue", "Ma")
    str_cal = str_cal.replace("wed", "mi")
    str_cal = str_cal.replace("Wed", "Mi")
    str_cal = str_cal.replace("thu", "ju")
    str_cal = str_cal.replace("Thu", "Ju")
    str_cal = str_cal.replace("fri", "vi")
    str_cal = str_cal.replace("Fri", "Vi")
    str_cal = str_cal.replace("sat", "sa")
    str_cal = str_cal.replace("Sat", "Sa")
    str_cal = str_cal.replace("sun", "do")
    str_cal = str_cal.replace("Sun", "Do")

    str_cal = str_cal.replace("January", "Enero")
    str_cal = str_cal.replace("February", "Febrero")
    str_cal = str_cal.replace("March", "Marzo")
    str_cal = str_cal.replace("April", "Abril")
    str_cal = str_cal.replace("May", "Mayo")
    str_cal = str_cal.replace("June", "Junio")
    str_cal = str_cal.replace("July", "Julio")
    str_cal = str_cal.replace("August", "Agosto")
    str_cal = str_cal.replace("September", "Septiembre")
    str_cal = str_cal.replace("October", "Octubre")
    str_cal = str_cal.replace("November", "Noviembre")
    str_cal = str_cal.replace("December", "Diciembre")

    str_cal = str_cal.replace("luth", "month w-100")

    return str_cal
