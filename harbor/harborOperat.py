#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/9/5 上午9:01
# @Author  : Xie Chuyu
# @File    : harborOperat.py
# @Software: PyCharm
import requests
import urllib3
import json
from config import config


class Harbor(object):
    urllib3.disable_warnings()
    session = requests.session()
    base_url = ('https://' if config['harbor_tls'] else 'http://') + config['harbor_url']

    def _login_harbor(self):
        print('trying to login harbor')
        login_url = self.base_url + '/c/login'
        data = {
            'principal': config['harbor_username'],
            'password': config['harbor_password'],
        }
        res = self.session.post(url=login_url, data=data, verify=False)

        assert res.status_code is 200, 'login failed, please check the harbor config'
        print('login success')

    def _check_project(self, project_name_str):
        """
        check if project exist,return bool

        :param project_name_str:
        :return:
        """
        check_project_url = self.base_url + "/api/projects?project_name=" + project_name_str
        res = self.session.head(check_project_url, verify=False)
        if res.status_code == 200:
            return True
        return False

    def _pre_push(self, project_name_str):
        """
        before push a docker, should make sure project is exist

        :param project_name_str:
        :return:
        """
        if "/" in project_name_str:
            project_name_str = project_name_str.split("/")[0]

        # if project is exist ,pass it
        if self._check_project(project_name_str):
            return

        print('trying to create project' + project_name_str)
        create_project_url = self.base_url + "/api/projects"
        data = json.dumps({
            "project_name": project_name_str,
            "metadata": {
                "public": "true"
            }
        })
        res = self.session.post(url=create_project_url, data=data, verify=False,
                                headers={'Content-Type': 'application/json'})

        # if not login
        if res.status_code == 401:
            self._login_harbor()
            return self.pre_push(project_name_str)

        assert res.status_code is 201, 'create project failed ' + str(res.status_code)
        print('create project success')

    def push(self, name_str):
        """
            push image to harbor

            :param name_str:
            :return:
            """

        print("pushing " + name_str)

        # make sure project is exist
        name_split, project_name = name_str.split("/"), name_str
        if '.' in name_split[0]:
            with open("out/domain.txt", "a") as file:
                file.write(name_split[0])
            project_name = "/".join(name_split[1:])
            name_split = project_name.split("/")
        if len(name_split) is 1:
            project_name = 'library/' + name_split[0]

        self._pre_push(project_name)
        return config['harbor_url'] + "/" + project_name
