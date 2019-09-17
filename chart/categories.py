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

type_dict = {
    'Application': ['elasticsearch', 'phpbb', 'mercure', 'osclass', 'blog', 'game', 'moodle', 'e-commerce',
                    'home-assistant', 'human resources', 'reporting'],
    'WebIDE': ['nodered'],
    'Mobile': [],
    'Spider': [],
    'DataBase': ['database', 'sql', 'quality', 'sqlproxy', 'mariadb', 'mysqldump', 'hazelcast', 'percona', 'mysql',
                 'keyvalue', 'mongodb', 'postgresql', 'nosql', 'replication', 'redis'],
    'Cloud': ['cluster', 'metallb', 'envoy', 'opa', 'aws', 'distributed', 'zookeeper', 'kubernetes deployment',
              'serverless',
              'kube-lego',
              'stackdriver'],
    'BlockChain': ['blockchain', 'hyperledger', 'ethereum', 'fabric', 'openiban'],
    'Contain': ['kubernetes', 'k8s-spot-rescheduler', 'metallb', 'kubernetes deployment', 'kube-lego', 'docker',
                'helm release',
                'helm-exporter', 'cluster-autoscaler'],
    'BigData': ['timeseries', 'big-data', 'hadoop', 'elasticsearch', 'spark'],
    'Workflow': ['jenkins', 'workflow', 'terraform', 'jfrog', 'ci', 'testing', 'drone', 'ci/cd'],
    'Auth': ['authentication', 'sso', 'oidc', 'oauth', 'oauth2', 'iam', 'ldap', 'openid connect'],
    'MQ': ['rabbitmq', 'dns', 'nats', 'message queue'],
    'Middleware': ['cache', 'kafka', 'zookeeper', 'centrifugo', 'event'],
    'ProjectManage': ['jenkins', 'wiki', 'crm', 'qa', 'chaos-engineering', 'task management', 'issue tracker',
                      'project management', 'cms', 'code review', 'troubleshooting'],
    'Network': ['proxy', 'nginx', 'ingress', 'network'],
    'Monitoring': ['monitoring', 'prometheus-operator', 'fluentd', 'couchdb-exporter', 'hpa', 'pushgateway', 'syslog',
                   'sensu', 'observability', 'logs', 'stackdriver',
                   'metrics', 'logging', 'metric', 'alerting'],
    'Security': ['security', 'letsencrypt', 'kube-lego'],
    'Storage': ['storage', 'nfs', 'ipfs', 'object-storage', ],
    'Teamwork': ['slack', 'smtp', 'chat', 'quassel', 'mail', 'mattermost', 'email', 'pop3']
}
wait_check = ['http', 'web', 'event', 'operator', 'dashboard', 'php', 'exporter', 'git', 'nodejs']

no_category_list = {}


def classify(chart_path):
    # print('reading ' + chart_path)
    with open(chart_path, encoding='utf-8') as chart:
        chart_yaml = yaml.load(stream=chart, Loader=Loader)
        name = chart_path.replace(config['path'], '').split('/')[0]
        keywords = [name]
        keywords.extend(chart_yaml.get('keywords'))

        categories = set()
        for keyword in keywords:
            for line in type_dict:
                for TYPE in type_dict[line]:
                    keyword_lower = keyword.lower()
                    if keyword_lower == TYPE or keyword_lower in TYPE or TYPE in keyword_lower:
                        categories.add(line)
                        break

        if categories:
            print('{} categories is {}'.format(
                name, categories
            ))
        else:
            print(name + ' no categories')

        with open(chart_path.replace('Chart.yaml', 'questions.yml'), 'w') as file:
            content = {
                'categories': list(categories)
            }
            yaml.dump(content, file, Dumper)


keywords_dict = {}
has_added = {}


def show(chart_path):
    with open(chart_path, encoding='utf-8') as chart:
        chart_yaml = yaml.load(stream=chart, Loader=Loader)
        keywords = chart_yaml.get('keywords')
        name = chart_path.replace(config['path'], '').split('/')[0]
        if not keywords:
            no_category_list[name] = keywords if keywords else 1
            return
        if name in has_added:
            return
        has_added[name] = 1
        for x in keywords:
            if x not in keywords_dict:
                keywords_dict[x] = 1
            else:
                keywords_dict[x] += 1


def get_all_keyword():
    for file_name in os.listdir(config['path']):
        if os.path.isfile(config['path'] + file_name):
            continue
        for pkg_name in os.listdir(config['path'] + file_name + "/"):
            chart_path = config['path'] + file_name + "/"
            chart_name = chart_path + pkg_name + "/Chart.yaml"
            if os.path.isfile(chart_name):
                try:
                    classify(chart_name)
                    # show(chart_name)
                except Exception as e:
                    continue

    if no_category_list:
        with open("out/NullList/noCategoryList.txt", "w") as file:
            for line in no_category_list:
                file.write(line.replace(config['path'], '') + "\n" + str(no_category_list[line]) + "\n")

    os.system('cd {} && git add templates'.format(config['git_path']))
    git().commit(':label: add categories at {}'.
                 format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                 )

    # items = sorted([(value, key) for (key, value) in keywords_dict.items()])
    # items.reverse()
    # print(items)
    # print(no_category_list)


if __name__ == '__main__':
    get_all_keyword()
