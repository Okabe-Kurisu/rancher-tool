#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : Xie Chuyu
# @Software: PyCharm
from chart import getIcon, getImages, tarThings, getAllCharts
from harbor import dockerThings
import os
from config import config


def init():
    """
    make sure the dir we need is exist

    :return:
    """
    print('initializing env')
    if not os.path.isdir('out'):
        os.mkdir('out')
    if not os.path.isdir(config['path']):
        os.mkdir(config['path'])
    if not os.path.isfile('out/domainList.txt') or not os.path.isfile('out/requestFail.txt'):
        open('out/domainList.txt', 'w')
        open('out/requestFail.txt', 'w')


if __name__ == '__main__':
    init()
    # getAllCharts.get_all_tgz_url()
    # getAllCharts.get_all_tgz()
    # tarThings.find_and_un_tar()
    getIcon.find_all_chart()
    # getImages.list_all_image()
    # dockerThings.pull_and_push_all()
