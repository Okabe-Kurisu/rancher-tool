#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : Xie Chuyu
# @Software: PyCharm
from chart import getIcon, getImages, tarThings, getAllCharts, gitOperat
from harbor import dockerThings, harborOperat
import os
import sys
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
    if not os.path.isfile('out/domainList.txt') or not os.path.isfile('out/requestFail.txt') or not os.path.isfile(
            'out/dockerDomainList.txt'):
        open('out/domainList.txt', 'w')
        open('out/requestFail.txt', 'w')
        open('out/dockerDomainList.txt', 'w')


version = '1.10'
help_text = """
RancherTool version{0}
与rancher相关的小工具合集

用法
    python main.py [--flag] flag可以写多个

选项
    --help              获取使用方法
    --gat               从谷歌上得到held chart列表。并保存在out/tar.txt。
    然后会将列表中的全部chart的压缩包下载下来，如果遇到已经下载过的，则会跳过
    --fut               将已经下载下来的包解压并且按照项目名称对于多个版本进行合并
    --gai               从已经下载下来的包中得到全部需要的docker镜像，并存储在out/images.txt中
    --ppa               从out/image.txt中逐个拉取镜像，并且推送到harbor中
    --config            输出全部配置信息
    --init              顺序执行从获取chart列表到推送镜像到harbor之间的全部动作，耗时及其长，不建议使用
    --clear             会清空全部带有harbor地址标记的镜像。同id的全删，谨慎使用。
    --skin [project]    会将[project]中多层项目名包裹的image剥离出来
""".format(version)


def start():
    args = sys.argv[1:]
    if not len(args) or "--help" in args:
        print(help_text)
        return
    elif "--init" in args:
        getAllCharts.get_all_tgz()
        tarThings.find_and_un_tar()
        getIcon.get_all_icon()
        dockerThings.clear_trash()
        getImages.list_all_image()
        dockerThings.pull_and_push_all()
        return
    if "--skin" in args:
        harbor = harborOperat.get_harbor()
        harbor.decorticate(args[-1])
        return
    elif "--config" in args:
        print(config)
        return
    elif "--clear" in args:
        dockerThings.clear_trash()
        return

    init()
    for arg in args:
        if arg == "--gat":
            getAllCharts.get_all_tgz()
        elif arg == "--fut":
            tarThings.find_and_un_tar()
        elif arg == "--gaicon":
            getIcon.get_all_icon()
        elif arg == "--gai":
            getImages.list_all_image()
        elif arg == "--ppa":
            dockerThings.pull_and_push_all()
        elif arg == "--git":
            gitOperat.merge_repo()
        elif not arg:
            continue
        else:
            print('wrong input')
            print(help_text)
            return


if __name__ == '__main__':
    start()
