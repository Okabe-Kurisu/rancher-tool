#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : Xie Chuyu
# @Software: PyCharm
import os
import shutil
import tarfile
from config import config
from utils.gitOperat import get_git as git
import time


def un_tar(file_name_str):
    print("-------------untaring " + file_name_str + "-------------")

    tar_obj = tarfile.open(file_name_str)

    # split the name and version
    file_name_split = file_name_str.split("-")
    name, version = '', ''
    # find version
    for s in file_name_split[:-1]:
        if s.replace('.', '').replace('v', '').isdigit():
            version += s + '-'
        elif s.replace('.', '').replace('rc', '').isdigit():
            version += s + '-'
        else:
            name += s + '-'
    version = version + file_name_split[-1].replace('.tgz', '')
    name = ''.join(name[:-1])

    pkg_name = name + "/" + version

    if not os.path.isdir(name):
        os.mkdir(name)
    if not os.path.isdir(pkg_name):
        os.mkdir(pkg_name)
    for tar_name in tar_obj.getnames():
        tar_obj.extract(tar_name, pkg_name + "/")
    tar_obj.close()

    format_pkg(pkg_name, name.replace(config['path'], ''))
    print(file_name_str + " has been untared already")


def format_pkg(pkg_name_str, name_str):
    """
    move file to right place

    :param pkg_name_str:
    :param name_str:
    :return:
    """
    for file_name in os.listdir(pkg_name_str + "/" + name_str):
        if not os.path.exists(pkg_name_str + "/" + file_name):
            shutil.move(pkg_name_str + "/" + name_str + "/" + file_name,
                        pkg_name_str + "/")
    if os.path.isdir(pkg_name_str + "/" + name_str + "/"):
        shutil.rmtree(pkg_name_str + "/" + name_str + "/")


def find_and_un_tar():
    print("-----------start unpack tar or tgz ---------------")
    for file_name in os.listdir(config['path']):
        # if it not a tar file, ignore it
        if not (file_name.endswith("tgz") or file_name.endswith("tar")) \
                or os.path.isdir(config['path'] + file_name):
            continue
        un_tar(config['path'] + file_name)


if __name__ == '__main__':
    find_and_un_tar()
