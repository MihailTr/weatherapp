# -*- coding: utf-8 -*-
"""
weatherapp.py
"""
from urllib.request import urlopen, Request
import html

ACCU_URL = "https://www.accuweather.com/ru/ua/vinnytsia/326175/weather-forecast/326175"
ACCU_TEGS = ('<span class="local-temp">', '<span class="cond">')
tags_ad = ('')

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
    tags1=[]
    for tag in tags:
        x = page_content.count(tag)
        if x == 1:
            tags1.append(tag)
        else:
            for ttags in ttags_ad:
                tag1 = ttags + tag
                tags1.append(tag1)
        print(tags1)
    return tuple([get_tag_content(page_content, tag) for tag in tags1])


def produce_output(provider_name, temp, condition):
    print((f'\n {provider_name}'))
    print(f'Temperature: {html.unescape(temp)}\n')
    print(f'Condition: {condition}\n')


def main():
    """
    main entry point
    """
    weather_sites = {"AccuWeather": (ACCU_URL, ACCU_TEGS)}
    for name in weather_sites:
        url, tags = weather_sites[name]
        content = get_page_source(url)
        temp, condition = get_weather_info(content, tags, tags_ad)
        produce_output(name, temp, condition)


if __name__ == '__main__':
    main()
