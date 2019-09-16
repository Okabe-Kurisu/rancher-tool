#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/9/12 上午10:33
# @Author  : Xie Chuyu
# @File    : categories.py
# @Software: PyCharm
import yaml
import os
from config import config
from yaml import Loader, Dumper
from chart.gitOperat import get_git as git
import time

categories = [
    'server',
    'application',
    'database',
    'web',
    'ingress',
    'sql',
    'cms',
    'dns',
    'prometheus',
    'cluster',
    'message queue',
    'dns',
    'platform',
    'network',
    'bug tracking',
    'code review',
    'git',
    'storage',
    'messaging',
    'CRM',
    'idm',
    'object-storage',
    'iam',
    'monitoring',
    'kubernetes',
    'logging',
    'mysql',
    'metrics',
    'security',
    'wiki',
    'slack',
    'blockchain',
    'mail',
    'issue tracker',
    'deploy',
    'stackdriver',
]
no_category_list = {}


def read_chart(chart_path):
    print('reading ' + chart_path)
    with open(chart_path, encoding='utf-8') as chart:
        chart_yaml = yaml.load(stream=chart, Loader=Loader)
        keywords = chart_yaml.get('keywords')
        if not keywords or not list(set(keywords) & set(categories)):
            print(chart_path + 'has no categories')
            no_category_list[chart_path] = keywords if keywords else 1
            return

        question_yaml_path = chart_path.replace('Chart.yaml', 'questions.yml')
        with open(question_yaml_path, 'w') as file:
            content = {
                'categories': list(set(keywords) & set(categories))
            }
            print('{} categories is {}'.format(
                chart_path, content['categories']
            ))
            yaml.dump(content, file, Dumper)


def get_all_keyword():
    for file_name in os.listdir(config['path']):
        if os.path.isfile(config['path'] + file_name):
            continue
        for pkg_name in os.listdir(config['path'] + file_name + "/"):
            chart_path = config['path'] + file_name + "/"
            chart_name = chart_path + pkg_name + "/Chart.yaml"
            if os.path.isfile(chart_name):
                try:
                    read_chart(chart_name)
                except Exception as e:
                    continue

    with open("out/NullList/noCategoryList.txt", "w") as file:
        for line in no_category_list:
            file.write(line.replace(config['path'], '') + "\n" + str(no_category_list[line]) + "\n")

    os.system('cd {} && git add templates'.format(config['git_path']))
    git().commit(':label: add categories at {}'.
                 format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                 )
