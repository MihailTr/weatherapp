# -*- coding: utf-8 -*-
"""
weatherapp.py
"""
from urllib.request import urlopen, Request
import html

acco_url = "https://www.accuweather.com/ru/ua/vinnytsia/326175/weather-forecast/326175"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:63.0)"}
acco_request = Request(acco_url, headers=headers)
acco_page = urlopen(acco_request).read()
acco_page = str(acco_page.decode())

"""
Temperature
"""
acco_teg_f = '<span class="large-temp">'
acco_teg_f_size = len(acco_teg_f)
acco_teg_f_index = acco_page.find(acco_teg_f)
acco_teg_f_start = acco_teg_f_index + acco_teg_f_size
acco_teg = ''

for char in acco_page[acco_teg_f_start:]:
    if char != '<':
        acco_teg += char
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

"""
http://rp5.ua/
"""
rp5_url = ('http://rp5.ua/%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_%D0%B2_%D0'
           '%92%D0%B8%D0%BD%D0%BD%D0%B8%D1%86%D0%B5')
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:63.0)"}
rp5_request = Request(rp5_url, headers=headers)
rp5_page = urlopen(rp5_request).read()
rp5_page = rp5_page.decode()

"""
Temperature
"""
rp5_teg_f = '<div id="ArchTemp"><span class="t_0" style="display: block;">'
rp5_teg_f_size = len(rp5_teg_f)
rp5_teg_f_index = rp5_page.find(rp5_teg_f)
rp5_teg_f_start = rp5_teg_f_index + rp5_teg_f_size
rp5_teg = ''

for char in rp5_page[rp5_teg_f_start:]:
    if char != '<':
        rp5_teg += char
    else:
        break

"""
Cond
"""
rp5_Cond_f = '<div class="cn3" onmouseover="tooltip(this,' + " '<b>"
rp5_Cond_f_size = len(rp5_Cond_f)
rp5_Cond_f_index = rp5_page.find(rp5_Cond_f)
rp5_Cond_f_start = rp5_Cond_f_index + rp5_Cond_f_size
rp5_Cond = ''

for char in rp5_page[rp5_Cond_f_start:]:
    if char != "<":
        rp5_Cond += char
    else:
        break

acco_teg = html.unescape(acco_teg)
rp5_teg = html.unescape(acco_teg)

print("Accuweather for: ", acco_Current_city, "\n")
print("Temperature:     ", acco_teg, "\n")
print("Cond:            ", acco_Cond, "\n")

print("rp5 for: ")  # , rp5_Current_city, "\n")
print("Temperature:     ", rp5_teg, "\n")
print("Cond:            ", rp5_Cond, "\n")

def get_request_headers():
    return {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:63.0)'}


def main():
    """
    main entry point
    """
    weather_sites={"AccuWeather": (ACCU_URL, ACCU_TEGS)}
    for name in weather_sites:
        url, tags = weather_sites[name]
        content = ger_page_source(url)
        temp, condition=get_weather_info(content, tags)
        produce_output(name, temp, condition)


if __name__ == '__main__':
    main()
