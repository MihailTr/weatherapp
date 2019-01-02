# -*- coding: utf-8 -*-
"""
weatherapp.py
"""

import sys
import argparse
import html
from urllib.request import urlopen, Request

ACCU_URL = "https://www.accuweather.com/ru/ua/vinnytsia/326175/weather-forecast/326175"
ACCU_TEGS = ('<span class="local-temp">', '<span class="cond">')
tags_ad = ('')

RP5_URL = ('http://rp5.ua/%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_%D0%B2_%D0'
           '%92%D0%B8%D0%BD%D0%BD%D0%B8%D1%86%D0%B5')
rp5_Cond_f = '<div class="cn3" onmouseover="tooltip(this,' + " '<b>"
RP5_TEGS = (
    '<div id="ArchTemp"><span class="t_0" style="display: block;">', rp5_Cond_f)

RP5tags_ad = ('')


def get_request_headers():
    return {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:63.0)'}


def get_page_source(url):
    request = Request(url, headers=get_request_headers())
    page_source = urlopen(request).read()
    return page_source.decode('utf-8')


def get_tag_content(page_content, tag):
    """

    :param page_content:
    :param tag:
    :return:
    """
    tag_index = page_content.find(tag)
    tag_size = len(tag)
    value_start = tag_index + tag_size

    content = ''
    for c in page_content[value_start:]:
        if c != '<':
            content += c
        else:
            break
    return content


def get_weather_info(page_content, tags, *ttags_ad):
    """
    """

    tags1 = []
    for tag in tags:
        x = page_content.count(tag)
        if x == 1:
            tags1.append(tag)
        else:
            for ttags in ttags_ad:
                tag1 = ttags + tag
                tags1.append(tag1)
    return tuple([get_tag_content(page_content, tag) for tag in tags1])


def produce_output(provider_name, temp, condition):
    print((f'\n {provider_name}'))
    print(f'Temperature: {html.unescape(temp)}\n')
    print(f'Condition: {condition}\n')


def main(argv):
    """
    main entry point
    """

    KNOWN_COMMANDS = {'accu': 'AccuWeather', 'rp5': 'RP5'}

    parser = argparse.ArgumentParser()
    parser.add_argument('command', help='Service name', nargs=1)
    params = parser.parse_args(argv)

    weather_sites = {
        "AccuWeather": (ACCU_URL, ACCU_TEGS),
        "RP5": (RP5_URL, RP5_TEGS)
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
        url, tags = weather_sites[name]
        content = get_page_source(url)
        if weather_sites[name] == "AccuWeather":
            temp, condition = get_weather_info(content, tags, tags_ad)
        else:
            temp, condition = get_weather_info(content, tags, RP5tags_ad)
        produce_output(name, temp, condition)


if __name__ == '__main__':
    main(sys.argv[1:])
