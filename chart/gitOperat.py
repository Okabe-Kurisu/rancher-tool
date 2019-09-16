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

    def __init__(self):
        self.repo = self.get_repo()

    def get_repo(self):
        # assert config['git_url'] and config['git_username'] and config[
        #     'git_password'], 'git is not config complete in config.py'

        git_path = config['git_path'] + '.git'
        if not os.path.isdir(git_path):
            os.popen('git config --global credential.helper store')

            print('init git path')
            repo = Repo.init(config['git_path'])
            gitignore = "*.tgz\ntemplates/*.tgz\n"
            with open(config['git_path'] + '.gitignore', 'w') as f:
                f.write(gitignore)
            if not os.path.isdir(config['git_path'] + 'templates/'):
                os.mkdir(config['git_path'] + 'templates/')
        else:
            repo = Repo(config['git_path'])

        if not repo.remotes.origin:
            origin = repo.create_remote('origin', config['git_url'])
            origin.fetch()
            repo.create_head('master', origin.refs.master)
            repo.heads.master.set_tracking_branch(origin.refs.master)
            repo.heads.master.checkout()
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

    def push(self):
        origin = self.repo.remotes.origin
        origin.fetch()
        origin.push()

    def tag(self, name_str):
        return self.repo.create_tag(name_str)


def get_git():
    global git
    if not git:
        git = Git()
    return git


def push():
    return get_git().push()
