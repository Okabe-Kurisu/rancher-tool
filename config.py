#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : Xie Chuyu
# @Software: PyCharm
config = {
    # http and https proxies, for exp :{'http': 'http://127.0.0.1:1082', 'https': 'http://127.0.0.1:1082'}
    'proxies': None,
    # docker retry time
    'docker_retry_times': 3,
    # download file retry times
    'download_retry_times': 3,

    # file path
    'path': "./pkg/",

    'git_path': "./git/",
    'git_url': "",

    # helm-stable-lightly git config
    'son_git_path': "",
    'son_git_url': "",

    # harbor config
    'harbor_url': "127.0.0.1",
    'harbor_tls': True,
    'harbor_username': 'admin',
    'harbor_password': 'admin',

    # sync source
    'wait_sync': {},

}
