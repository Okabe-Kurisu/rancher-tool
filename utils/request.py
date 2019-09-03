#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/9/3 下午6:11
# @Author  : Xie Chuyu
# @File    : request.py
# @Software: PyCharm
import requests
from requests import ReadTimeout
from config import config


def auto_retry_request(url_str, headers=None, timeout=5, retry_time=config['download_retry_times']):
    """
    auto download and retry when timeout

    FIXME: rebuild this code beauty

    :param url_str:
    :param headers:
    :param timeout:
    :param retry_time:
    :return:
    """
    try:
        return requests.get(url_str, headers=headers, timeout=timeout)
    except ReadTimeout:
        for x in range(retry_time * 2):
            try:
                if x is retry_time:
                    print('trying to use proxies')
                print("retry " + str(x + 1 - (0 if x < retry_time else retry_time)) + " times")
                response = requests.get(url_str, headers=headers, timeout=timeout,
                                        proxies=None if x < retry_time else config['proxies'])
                if response.status_code == 200:
                    return response
            except:
                pass
    return None
