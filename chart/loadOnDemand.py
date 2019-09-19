#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/9/19 上午9:00
# @Author  : Xie Chuyu
# @File    : loadOnDemand.py
# @Software: PyCharm
import os
import shutil
import time

from config import config
from utils.gitOperat import get_git as git

son_templates_path = config['son_git_path'] + 'templates/'


def init():
    """
    init the son git

    :return:
    """
    if not os.path.exists(config['son_git_path']):
        os.mkdir(config['son_git_path'])
        os.mkdir(son_templates_path)

    for filename in [x for x in os.listdir(config['path']) if os.path.isdir(config['path'] + x)]:
        copy_chart(filename)


def copy_chart(name, version='latest'):
    """
    copy chart from helm-stable to son_git_path

    :param name:
    :param version:
    :return:
    """
    print("copying the {}'s {} from the helm stable".format(name, version))
    assert os.path.exists(config['path'] + name), '目标chart{}不存在，检查输入或者更新helm stable目录'.format(name)
    latest, icon = pick_latest_version(config['path'] + name)
    target_version = latest if version == 'latest' else version
    origin_path, target_path = config['path'] + name, son_templates_path + name

    assert os.path.exists(origin_path + '/' + target_version), '{}的目标版本{}不存在，检查输入或者更新helm stable目录'. \
        format(name, str(target_version))
    if not os.path.exists(target_path):
        os.mkdir(target_path)
    if not os.path.exists(target_path + '/' + icon):
        shutil.copyfile(origin_path + '/' + icon, target_path + '/' + icon)
    if not os.path.exists(target_path + '/' + target_version):
        shutil.copytree(origin_path + '/' + target_version, target_path + '/' + target_version)


def pick_latest_version(pkg_path_str=None):
    """
    find the latest version num form a lot of version

    :param version_list:
    :return:
    """
    if not pkg_path_str:
        return None

    version_list = os.listdir(pkg_path_str)

    version_list.sort(reverse=True)
    latest, icon = version_list[0], ''
    if latest.startswith('icon'):
        icon = latest
        latest = version_list[1]
    else:
        for version in version_list:
            if version.startswith('icon'):
                icon = version
                break

    return latest, icon


if __name__ == '__main__':
    init()
