#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : Xie Chuyu
# @Software: PyCharm
import os
import yaml
from utils.request import auto_retry_get

from utils import fakeUA
from yaml import Loader, Dumper
from config import config
from chart.gitOperat import get_git as git
import time

# if value is 0 mean this dir has logo, else no
no_icon_dict = {}
headers = {
    'user-agent': fakeUA.random_UA()
}


def get_icon(chart_name_str, chart_path_str):
    print("downloading " + chart_path_str + "'s logo")

    icon_name = ''
    # check if icon has been put by human
    for file_name in os.listdir(chart_path_str):
        if file_name.startswith('icon.'):
            icon_name = '/' + file_name

    with open(chart_name_str, encoding='utf-8') as chart:
        chart_yaml = yaml.load(stream=chart, Loader=Loader)
        if icon_name:
            print("this logo has already exist, pass it")
        else:
            img_url = chart_yaml.get("icon")

            if not img_url:
                print(chart_path_str + ' is no logo, pass it')
                if chart_path_str not in no_icon_dict or no_icon_dict[chart_path_str] is not 0:
                    no_icon_dict[chart_path_str] = 1
                    return
            # github's icon cannot get from the url
            elif img_url.startswith('https://github.com'):
                img_url = img_url \
                    .replace('/blob/', '/raw/')
            # if this logo is exist, pass it
            elif img_url.startswith('file://'):
                print("this logo has already exist, pass it")
                no_icon_dict[chart_path_str] = 0
                return

            ext_name = img_url.split(".")[-1] if img_url else ''
            if len(ext_name) < 5:
                icon_name = "/icon." + ext_name
            else:
                icon_name = "/icon.png"

            print("trying to download logo from:" + img_url)
            img_response = auto_retry_get(img_url, headers=headers, timeout=5, retry_time=3)

            if img_response and img_response.headers['Content-Type'] != "text/html; charset=utf-8":
                with open(chart_path_str + icon_name, "wb") as f:
                    f.write(img_response.content)
                print(chart_path_str + "'s logo has been downloaded already")
            elif chart_path_str not in no_icon_dict or no_icon_dict[chart_path_str] is not 0:
                no_icon_dict[chart_path_str] = 1
                print(chart_path_str + "'s logo downloaded fail")
                return

        with open(chart_name_str, 'w', encoding="utf-8") as file:
            no_icon_dict[chart_path_str] = 0

            # make yaml's icon from web url to local url
            chart_yaml['icon'] = "file://.." + icon_name
            yaml.dump(chart_yaml, file, Dumper)


def get_all_icon():
    print("-----------start downloading icon ---------------")
    for file_name in os.listdir(config['path']):
        if os.path.isfile(config['path'] + file_name):
            continue
        for pkg_name in os.listdir(config['path'] + file_name + "/"):
            chart_path = config['path'] + file_name + "/"
            chart_name = chart_path + pkg_name + "/Chart.yaml"
            if os.path.isfile(chart_name):
                try:
                    get_icon(chart_name, chart_path)
                except Exception as e:
                    raise e
                    continue

    with open("out/NullList/noIconList.txt", "w") as file:
        for line in no_icon_dict:
            if no_icon_dict[line] is 1:
                file.write(line.replace(config['path'], '') + "\n")

    os.system('cd {} && git add templates'.format(config['git_path']))
    git().commit(':lipstick: update icon at {0}, last {1} charts has no icon'.format(
        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        len([x for x in no_icon_dict if no_icon_dict[x] is 1]))
    )


if __name__ == '__main__':
    get_all_icon()
