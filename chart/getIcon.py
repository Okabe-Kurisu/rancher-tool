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

# if value is 0 mean this dir has logo, else no
no_icon_dict = {}


def get_icon(chart_name_str, chart_path_str):
    print("downloading " + chart_path_str + "'s logo")
    with open(chart_name_str, encoding='utf-8') as chart:
        chart_yaml = yaml.load(stream=chart, Loader=Loader)
        img_url = chart_yaml.get("icon")

        if not img_url and (chart_path_str not in no_icon_dict and no_icon_dict[chart_path_str] is not 0):
            no_icon_dict[chart_name_str] = 1
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
            no_icon_dict[chart_name_str] = 0
            print(chart_path_str + "'s logo has been downloaded already")
        else:
            if chart_path_str not in no_icon_dict or no_icon_dict[chart_path_str] is not 0:
                no_icon_dict[chart_path_str] = 1
                print(chart_path_str + "'s logo downloaded fail")


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
    with open("out/noIconList.txt", "w") as file:
        for line in no_icon_dict:
            file.write(line + "\n")


if __name__ == '__main__':
    find_all_chart()
