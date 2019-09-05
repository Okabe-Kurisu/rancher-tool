#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/9/3 下午6:11
# @Author  : Xie Chuyu
# @File    : getAllCharts.py
# @Software: PyCharm
from utils.request import auto_retry_get
import os
from config import config


def get_all_tgz_url():
    print('downloading all tgz list')
    with open('out/tar.yaml', 'wb') as file:
        response = auto_retry_get('https://kubernetes-charts.storage.googleapis.com/index.yaml')
        file.write(response.content)
    res = os.popen('cat out/tar.yaml | grep -o "http.*.tgz"')
    lines = res.readlines()
    with open('out/tar.txt', 'w') as file:
        for line in lines:
            file.write(line)
    os.remove('out/tar.yaml')
    print('download complete')


def get_all_tgz():
    with open('out/tar.txt') as tar_list:
        lines = tar_list.readlines()
        for line in lines:
            line = line.replace("\n", "")
            file_name = line.split("/")[-1]
            print("downloading " + file_name)

            # if tar exist, continue
            if os.path.isfile(config['path'] + file_name):
                print(file_name + ' is exist, pass it')
                continue

            res = auto_retry_get(line)
            if not res or res.headers['content-type'] != 'application/x-tar':
                print('download ' + file_name + ' is fail')
                with open('out/failDownloadChart.txt', 'a') as file:
                    file.write(line + "\n")
                continue
            with open(config['path'] + file_name, 'wb') as file:
                file.write(res.content)
                print('download ' + file_name + ' is completed')


if __name__ == '__main__':
    get_all_tgz()
