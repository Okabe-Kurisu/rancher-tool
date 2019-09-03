#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : Xie Chuyu
# @Software: PyCharm
from major import getIcon, getImages, tarThings, dockerThings, getAllCharts

if __name__ == '__main__':
    getAllCharts.get_all_tgz_url()
    getAllCharts.get_all_tgz()
    tarThings.find_and_un_tar()
    getIcon.find_all_chart()
    getImages.list_all_image()
    dockerThings.pull_and_push_all()
