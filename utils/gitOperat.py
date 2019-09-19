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

git = None


class Git(object):
    repo = None
    git_path = None

    def __init__(self, git_path):
        self.git_path = git_path
        self.repo = self.get_repo()

    def get_repo(self):
        dot_git_path = self.git_path + '.git'
        if not os.path.isdir(dot_git_path):
            os.popen('git config credential.helper store')

            print('init git path')
            repo = Repo.init(self.git_path)
            repo.create_head('master')
            gitignore = "*.tgz\ntemplates/*.tgz\n"
            with open(config['git_path'] + '.gitignore', 'w') as f:
                f.write(gitignore)
            if not os.path.isdir(self.git_path + 'templates/'):
                os.mkdir('templates/')
        else:
            repo = Repo(self.git_path)

        return repo

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

    def push(self, target):
        if not self.repo.remotes:
            self.repo.create_remote(name='target', url=target)
        target = self.repo.remotes.target

        target.fetch()
        target.push(self.repo.heads.master)
        print('push to {} success'.format(target))

    def tag(self, name_str):
        return self.repo.create_tag(name_str)


def get_git(git_path=config['git_path']):
    global git
    if not git:
        git = Git(git_path)
    return git

