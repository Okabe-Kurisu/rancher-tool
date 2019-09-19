#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : Xie Chuyu
# @Software: PyCharm
from chart import getIcon, getImages, tarThings, getAllCharts, categories, loadOnDemand
from utils import gitOperat
from harbor import dockerThings, harborOperat
import os
import sys
from config import config


def init():
    """
    make sure the dir we need is exist

    :return:
    """
    if not os.path.isdir('out'):
        os.mkdir('out')
    if not os.path.isdir('out/NullList/'):
        os.mkdir('out/NullList/')
    if not os.path.isdir(config['path']):
        os.mkdir(config['path'])
    if not os.path.isfile('out/domainList.txt') or not os.path.isfile('out/requestFail.txt') or not os.path.isfile(
            'out/dockerDomainList.txt'):
        open('out/domainList.txt', 'w')
        open('out/requestFail.txt', 'w')
        open('out/dockerDomainList.txt', 'w')


version = '1.40'
help_text = """
RancherTool version{0}
与rancher相关的小工具合集

用法
    python main.py [--flag] flag可以写多个

选项
    --help              获取使用方法
    --gat               从谷歌上得到held chart列表。并保存在out/tar.txt。然后会
    将列表中的全部chart的压缩包下载下来，如果遇到已经下载过的，则会跳过
    --fut               将已经下载下来的包解压并且按照项目名称对于多个版本进行合并
    --gai               从已经下载下来的包中得到全部需要的docker镜像，并存储
    在out/images.txt中
    --gaicon            为所有的包下载图标
    --ppa               从out/image.txt中逐个拉取镜像，并且推送到harbor中
    --config            输出全部配置信息
    耗时及其长，不建议使用
    --clear             会清空全部带有harbor地址标记的镜像。同id的全删，谨慎使用。
    --skin [project]    会将[project]中多层项目名包裹的image剥离出来
    --git               提交helm-stable仓的全部commit
    --gac               为全部项目增加question.yaml文件，并且对项目进行分类
    --tran [name] [ver] 将helm-stable中名为[name]版本为[ver]的chart移动
    到helm-stable-lightly中并提交，如果不输入版本号，则默认为最新的版本，如果输入
    的参数超过三个，就会将参数全部视为目标chart名称，版本号全部使用最新版本。如果不
    填写参数，则会将helm-stable中全部项目的最新版本创建到配置文件中的son_git_path
    路径，并在路径中初始化git仓
""".format(version)


def start():
    args = sys.argv[1:]
    if not len(args) or "--help" in args:
        return print(help_text)
    if "--skin" in args:
        harbor = harborOperat.get_harbor()
        return harbor.decorticate(args[-1])
    elif "--config" in args:
        return print(config)
    elif "--clear" in args:
        return dockerThings.clear_trash()
    elif "--tran" in args:
        if len(args) == 2:
            return loadOnDemand.copy_chart(name=args[-1])
        elif len(args) == 3:
            return loadOnDemand.copy_chart(name=args[-2], version=args[-1])
        elif len(args) == 1:
            return loadOnDemand.init()
        else:
            for x in args[1:]:
                loadOnDemand.copy_chart(name=x)
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
            gitOperat.push()
        elif arg == "--gac":
            categories.get_all_keyword()
        elif not arg:
            continue
        else:
            print('wrong input')
            print(help_text)
            return


if __name__ == '__main__':
    start()
