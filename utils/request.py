#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/9/3 下午6:11
# @Author  : Xie Chuyu
# @File    : request.py
# @Software: PyCharm
import requests
from config import config


def auto_retry_get(url_str, headers=None, timeout=10, retry_time=config['download_retry_times'],
                   proxies=config['proxies']):
    """
    auto download and retry when timeout

    :param proxies:
    :param url_str:
    :param headers:
    :param timeout:
    :param retry_time:
    :return:
    """

    if not retry_time:
        with open("out/requestFail.txt", 'r+') as file:
            lines = set(file.readlines())
            url_str = url_str + "\n"
            if url_str not in lines:
                file.write(url_str)
        with open("out/domainList.txt", 'r+') as file:
            lines = set(file.readlines())
            url_str = '25.6.204.3 ' + url_str.split("/")[2] + "\n"
            if url_str not in lines:
                file.write(url_str)
        return None
    try:
        if proxies:
            response = requests.get(url_str, headers=headers, timeout=timeout, proxies=proxies)
        else:
            response = requests.get(url_str, headers=headers, timeout=timeout)
        assert 200 <= response.status_code <= 300
        return response
    except Exception as e:
        print("get request about {0} is fail, retrying".format(url_str))
        # if retry_time is 1 and proxies:
        #     return auto_retry_get(url_str, headers=headers, timeout=timeout, retry_time=config['download_retry_times'],
        #                           proxies=None)
        return auto_retry_get(url_str, headers=headers, timeout=timeout, retry_time=retry_time - 1)
