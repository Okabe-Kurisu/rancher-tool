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


class Git(object):
    repo = None
    git_path = None

    def __init__(self, git_path=config['git_path'], git_url=None):
        self.git_path = git_path
        if not os.path.exists(git_path) and git_url:
            self.repo = Repo.clone_from(git_url, git_path)
        else:
            self.get_repo()

    def get_repo(self):
        dot_git_path = self.git_path + '.git'
        if not os.path.isdir(dot_git_path):
            os.popen('git config --global credential.helper store')

            print('init git path')
            self.repo = Repo.init(self.git_path)

            if self.git_path == config['git_path']:
                gitignore = "*.tgz\ntemplates/*.tgz\n"
                with open(config['git_path'] + '.gitignore', 'w') as f:
                    f.write(gitignore)
                if not os.path.isdir(self.git_path + 'templates/'):
                    os.mkdir('templates/')
        else:
            self.repo = Repo(self.git_path)

    def add(self, path_str=None, path_list=None):
        """
        add files to git

        :param path_list:
        :param path_str:
        :return: if repo dirty
        """
        if path_list:
            self.repo.index.add(items=path_list, force=False)
        elif path_str:
            self.repo.index.add(items=[path_str], force=False)
        # this function result is wrong
        return self.repo.is_dirty()

    def commit(self, info_str):
        print('commit {}'.format(info_str))
        self.repo.index.commit(message=info_str)

    def push(self, name, url, target='master'):
        if name not in self.repo.remotes:
            self.repo.create_remote(name=name, url=url)
        target_remote = self.repo.remotes[name]

        target_remote.fetch()
        os.popen('cd {} && git push {} master:{}'.format(self.git_path, name, target))
        print('push to {} success'.format(target))

    def pull(self, name='origin', url=None):
        try:
            remote = self.repo.remote(name)
        except ValueError:
            remote = self.repo.create_remote(name, url)
        remote.fetch()
        print('pull from {} success'.format(name))

    def tag(self, name_str):
        return self.repo.create_tag(name_str)
