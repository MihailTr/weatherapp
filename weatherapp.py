"""
weatherapp.py
"""
from urllib.request import urlopen, Request
import html

acco_url = "https://www.accuweather.com/ru/ua/vinnytsia/326175/weather-forecast/326175"
headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:63.0)"}
acco_request=Request(acco_url, headers=headers)
acco_page = urlopen(acco_request).read()
acco_page=str(acco_page)

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

acco_teg=html.unescape(acco_teg)
print("Accuweather: \n")
print("Temperature: ",acco_teg,"\n")