#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : Xie Chuyu
# @Software: PyCharm
config = {
    # http and https proxies
    'proxies': {'http': 'http://127.0.0.1:1081', 'https': 'http://127.0.0.1:1081'},
    # docker retry time
    'docker_retry_times': 3,
    # download file retry times
    'download_retry_times': 3,

    # file path
    # 'path': "./pkg/",
    'path': "/home/amadeus/Documents/hubtgz/",

    # harbor config
    # 'harbor_url': "localhost",
    'harbor_tls': True,
    'harbor_url': "172.20.10.2",
    'harbor_username': 'admin',
    'harbor_password': 'admin',
}
