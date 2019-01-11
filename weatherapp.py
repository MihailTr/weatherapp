# -*- coding: utf-8 -*-
"""
weatherapp.py
"""

import sys
import argparse
import re
import html
from urllib.request import urlopen, Request
import configparser
from pathlib import Path

from bs4 import BeautifulSoup


ACCU_URL = ("https://www.accuweather.com/ru/ua/vinnytsia/326175/weather"
            "-forecast/326175")

RP5_URL = ('http://rp5.ua/%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_%D0%B2_%D0'
           '%92%D0%B8%D0%BD%D0%BD%D0%B8%D1%86%D0%B5')
DEFAULT_NAME = 'vinnytsia'
DEFAULT_URL = ("https://www.accuweather.com/ru/ua/vinnytsia/326175/weather"
            "-forecast/326175")
ACCU_BROWSE_LOCATIONS = 'https://www.accuweather.com/uk/browse-locations'
CONFIG_LOCATION = 'Location'
CONFIG_FILE = 'weatherapp.ini'


def get_request_headers():
    return {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:63.0)'}


def get_page_source(url):
    request = Request(url, headers=get_request_headers())
    page_source = urlopen(request).read()
    return page_source.decode('utf-8')


def get_locations(locations_url):
    locations_page = get_page_source(locations_url)
    soup = BeautifulSoup(locations_page, 'html.parser')

    locations = []
    for location in soup.find_all('li', attrs={'class': 'drilldown cl'}):
        url = location.find('a').attrs['href']
        location = location.find('em').text
        locations.append((location, url))
    return locations


def get_configuration_file():
    return Path.home() / CONFIG_FILE


def save_configuration(name, url):
    parser = configparser.ConfigParser()
    parser[CONFIG_LOCATION] = {'name': name, 'url': url}
    with open(get_configuration_file(), 'w') as configfile:
        parser.write(configfile)

def get_configuration():
    name = DEFAULT_NAME
    url = DEFAULT_URL

    parser = configparser.ConfigParser()
    parser.read(get_configuration_file())

    if CONFIG_LOCATION in parser.sections():
        config = parser[CONFIG_LOCATION]
        name, url = config['name'], config['url']
    return name, url


def configurate():
    locations = get_locations(ACCU_BROWSE_LOCATIONS)
    while locations:
        for index, location in enumerate(locations):
            print(f'{index + 1}, {location[0]}')
        selected_index = int(input('Select:  '))
        location = locations[selected_index - 1]
        locations = get_locations(location[1])

    save_configuration(*location)

def get_weather_info(page_content):
    """
    """
    #if name == "AccuWeather":
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

    # if name == "RP5":
    #     city_page = BeautifulSoup(page_content, 'html.parser')
    #     current_day_rp5 = city_page.find('div', attrs={'id': 'content'})
    #
    #     weather_info = {}
    #     temp_rp5 = current_day_rp5.find('div', attrs={'id': 'ArchTemp'})
    #     temp_rp5 = temp_rp5.find('span', class_='t_0')
    #     if temp_rp5:
    #         weather_info['temp'] = temp_rp5.text
    #     feal_temp_rp5 = current_day_rp5.find('div', class_='ArchiveTempFeeling')
    #     for span in feal_temp_rp5.find_all('span', {'class': 't_1'}):
    #         span.decompose()
    #     if feal_temp_rp5:
    #         weather_info['feal_temp'] = feal_temp_rp5.text
    #     feal_info_rp5 = current_day_rp5.find('div', class_='ArchiveInfo')
    #     for span in feal_info_rp5.find_all('span', {'class': 't_1'}):
    #         span.decompose()
    #     for span in feal_info_rp5.find_all(
    #             'span', {'class': re.compile('wv_([1234])')}):
    #         span.decompose()
    #     if feal_info_rp5:
    #         weather_info['Info'] = feal_info_rp5.text
    return weather_info


def produce_output(city_name, info):

    print((f'\n {city_name}'))
    print('-' * 20)

    for key, value in info.items():
        print(f'{key}: {html.unescape(value)}')

def get_accu_weather_info():
    city_name, city_url = get_configuration()
    content = get_page_source(city_url)
    produce_output(city_name, get_weather_info(content))


def main(argv):
    """
    main entry point
    """

    KNOWN_COMMANDS = {'accu': get_accu_weather_info,
                      'rp5': 'RP5',
                      'config': configurate}

    parser = argparse.ArgumentParser()
    parser.add_argument('command', help='Service name', nargs=1)
    params = parser.parse_args(argv)

    #weather_sites = {
    #     "AccuWeather": (ACCU_URL),
    #     "RP5": (RP5_URL)
    # }

    if params.command:
        command = params.command[0]
        if command in KNOWN_COMMANDS:
            KNOWN_COMMANDS[command]()
            # weather_sites = {
            #     KNOWN_COMMANDS[command]: weather_sites[KNOWN_COMMANDS[command]]
            # }
        else:
            print("Unknown command provider")
            sys.exit(1)



if __name__ == '__main__':
    main(sys.argv[1:])
