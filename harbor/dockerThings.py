#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : Xie Chuyu
# @Software: PyCharm
import docker
import os

from harbor.harborOperat import Harbor
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
        total_count, point = len(images_list), 0

        for line in images_list:
            line = line.replace("\n", "")
            point += 1
            try:
                print("--deal with {0}, less {1} to download, total percent {2:.2f}%--"
                      .format(line, str(total_count - point), point / total_count * 100))
                if not harbor.check_image(line):
                    image = pull(line)
                    push(image, line)
                    client.images.remove(image=image)
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
    except Exception:
        with open("out/dockerDomainList.txt", 'w') as file:
            lines = set(file.readlines())
            line = '25.6.204.3 ' + image_name.split("/")[0] + "\n"
            if line not in lines:
                file.write(line)
        print("docker {0} is not found, maybe is net issue, retrying".format(image_name))
        return pull(image_name, retry_time=retry_time - 1)


def push(image, name_str):
    project_name = harbor.pre_push(name_str)
    image.tag(project_name)
    client.images.pre_push(project_name)
    print("push " + name_str + " finish")


def clear_trash():
    """
    remove the image what has been push to harbor

    :return:
    """

    print('start to clear trash')
    id_list = filter_images(config['harbor_url'])
    if not id_list:
        print('no trash to clear')
        return
    for docker_id in id_list:
        print('removing ' + docker_id)
        os.popen('docker rmi ' + docker_id)


def filter_images(keyword_str):
    """
    filter all the image by the keyword, return theirs name:tag

    :param keyword_str:
    :return:
    """

    res = os.popen('docker images | grep ' + keyword_str)
    lines = res.readlines()
    docker_list = []
    for line in lines:
        point, part, length, docker_name = -1, 0, len(line), ''
        while point < length - 1:
            point += 1
            point_char, pre_char = line[point], line[point - 1] if point is not 0 else ' '

            # if there is new part
            if point_char != ' ' and pre_char == ' ':
                part += 1
                part_content = ''.join(line[point:]).split(' ')[0]
                # if in part1(name part), get id
                if part is 1:
                    docker_name = part_content
                elif part is 2:
                    docker_name += ':' + part_content
                else:
                    break
        docker_list.append(docker_name)
    return docker_list


if __name__ == '__main__':
    clear_trash()
