#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/9/9 下午3:00
# @Author  : Xie Chuyu
# @File    : gitOperat.py
# @Software: PyCharm
import os
import time

from git import Repo
from config import config
import shutil


def get_repo():
    # assert config['git_url'] and config['git_username'] and config[
    #     'git_password'], 'git is not config complete in config.py'

    git_path = config['git_path'] + '.git'
    if not os.path.isdir(git_path):
        os.popen('git config --global credential.helper store')

        print('init git path')
        repo = Repo.init(config['git_path'])
        gitignore = "*.tgz\n"
        with open(config['git_path'] + '.gitignore', 'w') as f:
            f.write(gitignore)
        os.mkdir(config['git_path'] + 'templates/')

        origin = repo.create_remote('origin', config['git_url'])
        origin.fetch()
        repo.create_head('master', origin.refs.master)
        repo.heads.master.set_tracking_branch(origin.refs.master)
    else:
        repo = Repo(config['git_path'])
    repo.heads.master.checkout()
    return repo


def merge_repo():
    repo = get_repo()
    print('copying charts')
    template_path = config['git_path'] + 'templates/'

    for path in [config['path'] + x for x in os.listdir(config['path']) if os.path.isdir(config['path'] + x)]:
        for file in ['/' + x for x in os.listdir(path)]:
            origin_name = path + file
            file_name = path.replace(config['path'], '') + file
            target_name = template_path + file_name
            if not os.path.exists(target_name) and os.path.isdir(origin_name):
                shutil.copytree(origin_name, target_name)
            elif not os.path.exists(target_name) and os.path.isfile(origin_name):
                shutil.copy(origin_name, target_name)

            repo.index.add(items=['templates/'])
            info = 'upload {} at {}'.format(file_name, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

            if repo.is_dirty():
                continue
            repo.index.commit(info)
            print(info)
            origin = repo.remotes.origin
            origin.fetch()
            origin.push()
    print('push complete')
