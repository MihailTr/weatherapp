# -*- coding: utf-8 -*-
"""
weatherapp.py
"""

import sys
import argparse
import re
from bs4 import BeautifulSoup
import html
from urllib.request import urlopen, Request

ACCU_URL = ("https://www.accuweather.com/ru/ua/vinnytsia/326175/weather"
            "-forecast/326175")

RP5_URL = ('http://rp5.ua/%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_%D0%B2_%D0'
           '%92%D0%B8%D0%BD%D0%BD%D0%B8%D1%86%D0%B5')


def get_request_headers():
    return {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:63.0)'}


def get_page_source(url):
    request = Request(url, headers=get_request_headers())
    page_source = urlopen(request).read()
    return page_source.decode('utf-8')


def get_weather_info(name, page_content):
    """
    """
    if name == "AccuWeather":
        city_page = BeautifulSoup(page_content, 'html.parser')
        current_day_selection = city_page.find(
            'li', class_=re.compile('(day|night) current first cl'))

        weather_info = {}
        if current_day_selection:
            current_day_url = current_day_selection.find('a').attrs['href']
            if current_day_url:
                current_day_page = get_page_source(current_day_url)
                if current_day_page:
                    current_day = \
                        BeautifulSoup(current_day_page, 'html.parser')
                    weather_details = \
                        current_day.find('div', attrs={'id': 'detail-now'})
                    condition = weather_details.find('span', class_='cond')
                    if condition:
                        weather_info['cond'] = condition.text
                    temp = weather_details.find('span', class_='large-temp')
                    if temp:
                        weather_info['temp'] = temp.text
                    feal_temp = weather_details.find('span',
                                                     class_='small-temp')
                    if feal_temp:
                        weather_info['feal_temp'] = feal_temp.text
                    wind_info = weather_details.find_all('li', class_='wind')
                    if wind_info:
                        weather_info['wind'] = \
                            ' '.join(map(lambda t: t.text.strip(), wind_info))

    if name == "RP5":
        city_page = BeautifulSoup(page_content, 'html.parser')
        current_day_rp5 = city_page.find('div', attrs={'id': 'content'})

        weather_info = {}
        temp_rp5 = current_day_rp5.find('div', attrs={'id': 'ArchTemp'})
        temp_rp5 = temp_rp5.find('span', class_='t_0')
        if temp_rp5:
            weather_info['temp'] = temp_rp5.text
        feal_temp_rp5 = current_day_rp5.find('div', class_='ArchiveTempFeeling')
        for span in feal_temp_rp5.find_all('span', {'class': 't_1'}):
            span.decompose()
        if feal_temp_rp5:
            weather_info['feal_temp'] = feal_temp_rp5.text
        feal_info_rp5 = current_day_rp5.find('div', class_='ArchiveInfo')
        for span in feal_info_rp5.find_all('span', {'class': 't_1'}):
            span.decompose()
        for span in feal_info_rp5.find_all(
                'span', {'class': re.compile('wv_(1|2|3|4)')}):
            span.decompose()
        if feal_info_rp5:
            weather_info['Info'] = feal_info_rp5.text
    return weather_info


def produce_output(provider_name, info):
    print((f'\n {provider_name}'))
    for key, value in info.items():
        print(f'{key}: {html.unescape(value)}')


def main(argv):
    """
    main entry point
    """

    KNOWN_COMMANDS = {'accu': 'AccuWeather', 'rp5': 'RP5'}

    parser = argparse.ArgumentParser()
    parser.add_argument('command', help='Service name', nargs=1)
    params = parser.parse_args(argv)

    weather_sites = {
        "AccuWeather": (ACCU_URL),
        "RP5": (RP5_URL)
    }

    if params.command:
        command = params.command[0]
        if command in KNOWN_COMMANDS:
            weather_sites = {
                KNOWN_COMMANDS[command]: weather_sites[KNOWN_COMMANDS[command]]
            }
        else:
            print("Unknown command provider")
            sys.exit(1)

    for name in weather_sites:
        url = weather_sites[name]
        content = get_page_source(url)
        produce_output(name, get_weather_info(name, content))


if __name__ == '__main__':
    main(sys.argv[1:])
