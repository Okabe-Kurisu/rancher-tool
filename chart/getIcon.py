#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : Xie Chuyu
# @Software: PyCharm
import os
import requests
import yaml
from utils.request import auto_retry_get

from utils import fakeUA
from yaml import Loader, Dumper
from config import config

no_icon_list = []


def get_icon(chart_name_str, chart_path_str):
    print("downloading " + chart_path_str + "'s logo")
    with open(chart_name_str, encoding='utf-8') as chart:
        chart_yaml = yaml.load(stream=chart, Loader=Loader)
        img_url = chart_yaml.get("icon")

        if not img_url:
            no_icon_list.append(chart_path_str)
            return
        # github's icon cannot get from the url
        elif img_url.startswith('https://github.com'):
            img_url = img_url \
                .replace('/blob/', '/raw/')
        # if this logo is exist, pass it
        elif img_url == "file://../icon.png":
            print("this logo has already exist, pass it")
            return

        headers = {
            'u]ser-agent': fakeUA.random_UA()
        }
        print("trying to download logo from:" + img_url)
        img_response = auto_retry_get(img_url, headers=headers, timeout=5, retry_time=3)

        if img_response and img_response.headers['Content-Type'] != "text/html; charset=utf-8":
            icon_name = "/icon." + img_url.split(".")[-1]
            with open(chart_path_str + icon_name, "wb") as f:
                f.write(img_response.content)
            with open(chart_name_str, 'w', encoding="utf-8") as chart:
                # make yaml's icon from web url to local url
                chart_yaml['icon'] = "file://../icon.png"
                yaml.dump(chart_yaml, chart, Dumper)
                print(chart_path_str + "'s logo has been downloaded already")
        else:
            print(chart_path_str + "'s logo downloaded fail")
            no_icon_list.append(chart_path_str)


def retry_img_download(img_url_str):
    headers = {
        'user-agent': fakeUA.random_UA()
    }
    for x in range(config['icon_retry_times']):
        try:
            print("retry " + str(x + 1) + " times")
            img_response = requests.get(img_url_str, headers=headers, timeout=5)
            if img_response.status_code == 200:
                return img_response
        except:
            pass
    print('trying to use proxies')
    for x in range(config['icon_retry_times']):
        try:
            print("retry " + str(x + 1) + " times")
            img_response = requests.get(img_url_str, headers=headers, timeout=5, proxies=config['proxies'])
            if img_response.status_code == 200:
                return img_response
        except:
            pass
    return None


def find_all_chart():
    print("-----------start downloading icon ---------------")
    for file_name in os.listdir(config['path']):
        if os.path.isfile(config['path'] + file_name):
            continue
        for pkg_name in os.listdir(config['path'] + file_name + "/"):
            chart_path = config['path'] + file_name + "/"
            chart_name = chart_path + pkg_name + "/Chart.yaml"
            if os.path.isfile(chart_name):
                get_icon(chart_name, chart_path)
    if not no_icon_list:
        with open("out/noIconList.txt", "w") as file:
            for line in no_icon_list:
                file.write(line + "\n")


if __name__ == '__main__':
    find_all_chart()
