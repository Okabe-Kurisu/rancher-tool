#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : Xie Chuyu
# @Software: PyCharm
import docker

from harbor.harborOperat import Harbor
from docker.errors import ImageNotFound
from config import config

client = docker.from_env()
client.login(username=config['harbor_username'],
             password=config['harbor_password'],
             registry=config['harbor_url'])
harbor = Harbor()


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


def pull(image_name, retry_time=config['docker_retry_times']):
    """
    pull image and auto retry

    :param retry_time:
    :param image_name:
    :return:
    """

    print("pulling " + image_name)
    try:
        return client.images.pull(image_name)
    except ImageNotFound:
        print("docker {0} is not found, maybe is net issue, retrying".format(image_name))
        return pull(image_name, retry_time=retry_time - 1)


def push(image, name_str):
    project_name = harbor.push(name_str)
    image.tag(project_name)
    client.images.push(project_name)
    print("push " + name_str + " finish")


if __name__ == '__main__':
    pull("asfb")
    # pull_and_push_all()
    # login_harbor()
    # print(client.images.list())
