#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/9/5 上午9:01
# @Author  : Xie Chuyu
# @File    : harborOperat.py
# @Software: PyCharm
import requests
import urllib3
import json
import docker
from config import config


class Harbor(object):
    urllib3.disable_warnings()
    session = requests.session()
    base_url = ('https://' if config['harbor_tls'] else 'http://') + config['harbor_url'] + '/api/'
    client = docker.from_env()
    client.login(username=config['harbor_username'],
                 password=config['harbor_password'],
                 registry=config['harbor_url'])
    json_headers = {'Content-Type': 'application/json'}

    def login_harbor(self):
        print('trying to login harbor')
        login_url = self.base_url.replace('/api', '') + 'c/login'
        data = {
            'principal': config['harbor_username'],
            'password': config['harbor_password'],
        }
        res = self.session.post(url=login_url, data=data, verify=False,
                                headers={"Content-Type": "application/x-www-form-urlencoded"})

        assert 200 <= res.status_code < 300, 'login failed, please check the harbor config'
        print('login success')
        return

    def _check_project(self, project_name_str):
        """
        check if project exist,return bool

        :param project_name_str:
        :return:
        """
        check_project_url = self.base_url + "projects?project_name=" + project_name_str
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

        print('trying to create project ' + project_name_str)
        create_project_url = self.base_url + "projects"
        data = json.dumps({
            "project_name": project_name_str,
            "metadata": {
                "public": "true"
            }
        })
        res = self._post_with_auth(create_project_url, data=data)

        assert 300 > res.status_code >= 200, 'create project failed ' + str(res.status_code)
        print('create project {0} success'.format(project_name_str))

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

    def _get_with_auth(self, url):
        """
        make sure get request has auth

        :param url:
        :return:
        """

        response = self.session.get(url, verify=False, headers=self.json_headers)
        if response.status_code == 401:
            self.login_harbor()
            return self._get_with_auth(url)
        return response

    def _post_with_auth(self, url, data=None):
        """
        make sure post request has auth

        :param url:
        :return:
        """

        response = self.session.post(url, verify=False, headers=self.json_headers, data=data)
        if response.status_code == 401:
            self.login_harbor()
            return self._post_with_auth(url, data=data)
        return response

    def mv_image(self, origin_name_str, target_name_str):
        """
        move a image from a project to another project or just rename it

        :param origin_name_str:
        :param target_name_str:
        :return:
        """

        print("move {0} to {1}".format(origin_name_str, target_name_str))
        image = self.client.images.pull(config['harbor_url'] + "/" + origin_name_str)
        image_name = self.push(target_name_str)
        image.tag(image_name)
        self.client.images.push(image_name)

        repository_name, tag = origin_name_str.split(':')[0], origin_name_str.split(':')[1]
        delete_url = "{0}repositories/{1}/tags/{2}".format(self.base_url, repository_name, tag)
        self.session.delete(delete_url, verify=False, headers=self.json_headers)

    def decorticate(self, project_name_str):
        """
        make wrong name right, for exp, /library/project/name => /project/name

        :return:
        """

        project_url = "{0}projects?name={1}".format(self.base_url, project_name_str)
        projects_response = self._get_with_auth(project_url)
        projects, project_id = projects_response.json(encoding='utf-8'), 0
        assert projects, 'project is not exist'
        if len(projects) is 1:
            project_id = projects[0]['project_id']
        else:
            for project in projects:
                if project['name'] == project_name_str:
                    project_id = project['project_id']
        assert project_id, 'project is not exist'

        repositories_url = "{0}repositories?project_id={1}".format(self.base_url, project_id)
        repositories_response = self._get_with_auth(repositories_url)
        repositories = repositories_response.json(encoding='utf-8')
        wait_to_decorticate = [x['name'] for x in repositories if len(x['name'].split('/')) > 1]
        for x in wait_to_decorticate:
            target = '/'.join(x.split('/')[:-2])
            self.mv_image(x, target)

    def check_image(self, line):
        # todo
        pass


if __name__ == '__main__':
    harbor = Harbor()
    harbor.login_harbor()
    # harbor.decorticate('kibana')
