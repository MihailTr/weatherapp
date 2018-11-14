# -*- coding: utf-8 -*-
"""
weatherapp.py
"""
from urllib.request import urlopen, Request
import html

acco_url = "https://www.accuweather.com/ru/ua/vinnytsia/326175/weather-forecast/326175"
headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:63.0)"}
acco_request=Request(acco_url, headers=headers)
acco_page = urlopen(acco_request).read()
acco_page=str(acco_page.decode())

"""
Temperature
"""
acco_teg_f='<span class="large-temp">'
acco_teg_f_size=len(acco_teg_f)
acco_teg_f_index=acco_page.find(acco_teg_f)
acco_teg_f_start=acco_teg_f_index+acco_teg_f_size
acco_teg=''

for char in acco_page[acco_teg_f_start:]:
    if char != '<':
        acco_teg+=char
    else:
        break

"""
Cond
"""
acco_Cond_f = '<span class="cond">'
acco_Cond_f_size = len(acco_Cond_f)
acco_Cond_f_index = acco_page.find(acco_Cond_f)
acco_Cond_f_start = acco_Cond_f_index + acco_Cond_f_size
acco_Cond = ''

for char in acco_page[acco_Cond_f_start:]:
    if char != '<':
        acco_Cond += char
    else:
        break


"""
Current_city
"""
acco_Current_city_f = '<span class="current-city"><h1>'
acco_Current_city_f_size = len(acco_Current_city_f)
acco_Current_city_f_index = acco_page.find(acco_Current_city_f)
acco_Current_city_f_start = acco_Current_city_f_index + acco_Current_city_f_size
acco_Current_city = ''

for char in acco_page[acco_Current_city_f_start:]:
    if char != '<':
        acco_Current_city += char
    else:
        break


acco_teg=html.unescape(acco_teg)

print("Accuweather for: ", acco_Current_city, "\n")
print("Temperature:     ",acco_teg,"\n")
print("Cond:            ",acco_Cond,"\n")
