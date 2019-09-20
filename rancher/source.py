#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/9/20 上午8:45
# @Author  : Xie Chuyu
# @File    : source.py
# @Software: PyCharm
import os

from config import config
from utils.gitOperat import Git


def get_source(origin_url, target_url):
    name = origin_url.split('/')[-1].replace('.git', '')
    git_path = '../' + name + '/'
    print('start to sync ' + name)
    target_git = Git(git_path=git_path, git_url=origin_url)
    target_git.pull(name='github', url=target_url)
    target_git.push(name='upstream', url=target_url, target='upstream')
    print(name + ' is synced')


def sync_all():
    for (origin_url, target_url) in config['wait_sync'].items():
        get_source(origin_url, target_url)
