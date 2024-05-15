
import time
import random

import requests

from utils import Doc


def _web_scrape_interval_time(wait):
    match wait:
        case False:
            pass
        case int():
            time.sleep(2*wait*random.random())
        case _:
            raise ValueError


def _web_scrape_get_response(url, headers):
    response = requests.get(url, headers=headers)
    print(response.status_code, url)
    if response.status_code == 200:
        return response
    return 0


def _web_scrape_try_get_response(url, headers, tries):
    for i in range(tries):
        try:
            response = _web_scrape_get_response(url, headers=headers)
            if response:
                return response
            else:
                print(f"请求{url}第{i}次失败")
        except:
            print(f"请求{url}第{i}次出错")
        time.sleep(5)


def _web_scrape_get_html(url, headers, tries, wait):
    _web_scrape_interval_time(wait)
    response = _web_scrape_try_get_response(url, headers=headers, tries=tries)
    if not response:
        Doc("./log/get_html.log").log(url)
        return 0
    else:
        html = response.text
    return html


def get_html(url, headers=0, tries=5, wait=1):

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    } if headers == 0 else headers

    return _web_scrape_get_html(url, headers=headers, tries=tries, wait=wait)
