# -*- coding: utf-8 -*-
"""
Написати програму яка виведе всі країни зображені на цій сторінці
http://example.webscraping.com/ (лише на першій сторінці)
"""

from urllib.request import urlopen, Request
import html

acco_url = "http://example.webscraping.com/"
headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:63.0)"}
acco_request=Request(acco_url, headers=headers)
acco_page = urlopen(acco_request).read()
acco_page=str(acco_page.decode())
acco_page_len=len(acco_page)
#print(acco_page)
"""
Temperature
"""
acco_teg_f='.png" />'
acco_teg_f_size=len(acco_teg_f)
acco_teg_f_index=acco_page.find(acco_teg_f)
acco_teg_f_start=acco_teg_f_index +acco_teg_f_size
acco_teg=''

#for i in range(acco_page_len):
for char in acco_page[acco_teg_f_start:]:
        if char != '<':
            acco_teg+=char
        else:
            break


print("for: ", acco_teg, "\n")