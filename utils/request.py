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

    with open("out/domainList.txt", 'r') as file:
        lines = set(file.readlines())
        line = '25.6.204.3 ' + url_str.split("/")[2] + "\n"
        if line in lines:
            return None

    if not retry_time:
        with open("out/requestFail.txt", 'r+') as file:
            lines = set(file.readlines())
            line = url_str + "\n"
            if line not in lines:
                file.write(line)
        with open("out/domainList.txt", 'r+') as file:
            lines = set(file.readlines())
            line = '25.6.204.3 ' + url_str.split("/")[2] + "\n"
            if line not in lines:
                file.write(line)
        return None
    try:
        if proxies:
            response = requests.get(url_str, headers=headers, timeout=timeout, verify=False, proxies=proxies)
        else:
            response = requests.get(url_str, headers=headers, timeout=timeout, verify=False)
        assert 200 <= response.status_code < 400
        return response
    except Exception as e:
        print("get request about {0} is fail, retrying".format(url_str))
        # if retry_time is 1 and proxies:
        #     return auto_retry_get(url_str, headers=headers, timeout=timeout, retry_time=config['download_retry_times'],
        #                           proxies=None)
        return auto_retry_get(url_str, headers=headers, timeout=timeout, retry_time=retry_time - 1)
