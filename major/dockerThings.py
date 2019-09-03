#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : Xie Chuyu
# @Software: PyCharm
import docker
import requests
from docker.errors import ImageNotFound

from config import config
import urllib3
import json

urllib3.disable_warnings()
client = docker.from_env()
client.login(username=config['harbor_username'],
             password=config['harbor_password'],
             registry=config['harbor_url'])
session = requests.session()
base_url = ('https://' if config['harbor_tls'] else 'http://') + config['harbor_url']


def pull_and_push_all():
    with open("out/pullOrPushLog.txt", "w") as error_file:
        images_file = open("out/images.txt")
        images_list = images_file.readlines()
        for line in images_list:
            line = line.replace("\n", "")
            try:
                print("--------------pull and push with " + line + "--------------")
                image = pull(line)
                push(image, line)
            except Exception as e:
                print('error with dealing with ' + line + ', plz read out/pullOrPushLog.txt')
                error_file.write("{0}: {1}\n".format(line, str(e)))
            finally:
                print("done with " + line)


def pull(image_name):
    """
    pull image and auto retry

    :param image_name:
    :return:
    """
    print("pulling " + image_name)
    try:
        return client.images.pull(image_name)
    except ImageNotFound:
        print("docker {0} is not found, maybe is net issue, retrying".format(image_name))
        for x in range(config['docker_retry_times']):
            try:
                print("retry " + str(x + 1) + " times")
                return client.images.pull(image_name)
            except Exception:
                pass


def push(image, name_str):
    """
    push image to harbor

    :param image:
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
    pre_push(project_name)

    project_name = config['harbor_url'] + "/" + project_name
    image.tag(project_name)
    client.images.push(project_name)
    print("push " + name_str + " finish")


def login_harbor():
    print('trying to login harbor')
    login_url = base_url + '/c/login'
    data = {
        'principal': config['harbor_username'],
        'password': config['harbor_password'],
    }
    res = session.post(url=login_url, data=data, verify=False)

    assert res.status_code is 200, 'login failed, please check the harbor config'
    print('login success')


def check_project(project_name_str):
    """
    check if project exist,return bool

    :param project_name_str:
    :return:
    """
    check_project_url = base_url + "/api/projects?project_name=" + project_name_str
    res = session.head(check_project_url, verify=False)
    if res.status_code == 200:
        return True
    return False


def pre_push(project_name_str):
    """
    before push a docker, should make sure project is exist

    :param project_name_str:
    :return:
    """
    if "/" in project_name_str:
        project_name_str = project_name_str.split("/")[0]

    # if project is exist ,pass it
    if check_project(project_name_str):
        return

    print('trying to create project' + project_name_str)
    create_project_url = base_url + "/api/projects"
    data = json.dumps({
        "project_name": project_name_str,
        "metadata": {
            "public": "true"
        }
    })
    res = session.post(url=create_project_url, data=data, verify=False,
                       headers={'Content-Type': 'application/json'})

    # if not login
    if res.status_code == 401:
        login_harbor()
        return pre_push(project_name_str)

    assert res.status_code is 201, 'create project failed ' + str(res.status_code)
    print('create project success')


if __name__ == '__main__':
    pull("asfb")
    # pull_and_push_all()
    # login_harbor()
    # print(client.images.list())
