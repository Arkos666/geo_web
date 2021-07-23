import re

from django.shortcuts import render
from django.utils.safestring import mark_safe
from geopy.geocoders import Nominatim
import json
import datetime
import calendar

cities = []


class CustomHTMLCal(calendar.HTMLCalendar):
    # custom class for calendar.HTML create
    cssclasses = ["lun", "mar", "mie", "jue", "vie", "sab", "dom"]
    cssclass_month_head = "text-center month-head"
    cssclass_month = "text-center month"
    cssclass_year = "text-italic lead"


def normalize(s):
    # function to delete accent mark to avoid problems

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
    # In this function we'll search the city in the json scrapped
    # The function will return a dict with 'month':('holidays')
    # None if city is not found

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
    # We leave the rest of variables for future
    city = address.get('city', '')
    state = address.get('state', '')
    country = address.get('country', '')
    code = address.get('country_code')
    zipcode = address.get('postcode')
    return city


# we render locate_all.html
def index(request):
    return render(request, "website/locate_all.html")


def locate_get(request):
    # main website return

    # We will get the parameters
    location = request.GET

    city = ""
    if 'city' in location:  # The objective is to get the city
        city = location['city']
    else:  # If we have long and lat then we search the city
        city = getcity(location['long'], location['lat'])
    result = find_holiday(normalize(city))  # We delete accent marks
    result = {int(k): v for k, v in result.items()}  # In this case it's easier to manipulate int than str in dict

    now = datetime.datetime.now()
    year = now.year
    month = now.month
    day = now.day

    next_day_hol = 0  # Initialize next_day_hol that have the day

    if not result[month] == []:  # If we have holidays in that month
        next_day_hol = max(result[month])
        next_month_hol = month

    december = 12

    print (day)
    print(max({int(v) for v in result[december]}))

    # If month is not december and next
    if int(next_day_hol) <= day and not month == december:
        for i in range(month + 1, december):
            if not result[i] == []:
                next_day_hol = min(result[i])
                next_month_hol = i
                break
    # If month is december and we passed the last holiday, next holiday is new year
    elif month == december and day >= max({int(v) for v in result[december]}):
        next_day_hol = 1
        next_month_hol = 1

    cal = CustomHTMLCal()  #Prepare calendar with custom CSS
    str_cal = change_lang(cal.formatmonth(year, month)) # change lang
    str_cal = class_holiday(str_cal, result[month]) # modify holidays classes with danger bg

    return render(request, "website/locate_get.html", {
        "city": city,
        "holiday": str(day) in result[month],
        "next_hol": str(next_day_hol) + "/" + str(next_month_hol),
        "cities": sorted(cities),
        "cal": mark_safe(str_cal)
    })


# We change the bg of holidays in calendar with re
def class_holiday(html_string, holidays):
    for i in holidays:
        pattern = r'(<td class="[a-z]{3}">' + str(i) + '<\/td>)'
        x = re.search(pattern, html_string)
        new_class = (x.group(0).split('">', 1)[0] + ' bg-danger" >' + x.group(0).split('">', 1)[1])
        html_string = html_string.replace(x.group(0), new_class)
    return html_string


# change lang days and months to Spanish
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
