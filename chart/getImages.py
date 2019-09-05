#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : Xie Chuyu
# @Software: PyCharm
import os
import subprocess

from config import config


def list_all_image():
    print("reading all images")
    images = {}

    with open("out/getImagesListError.txt", "w") as errors_file:
        for file_name in os.listdir(config['path']):
            if not (file_name.endswith(".tgz") or file_name.endswith(".tar")):
                continue
            res = subprocess.Popen(['helm', 'template', config['path'] + file_name, '|', 'grep', 'image:'],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1)

            images_of_chart = 0

            # reading stdout, if contain images, write into file
            while res.poll() is None:
                line = res.stdout.readline().decode('utf-8').replace(" ", "")
                if line.startswith("image:"):
                    line = line.replace("image:", "").replace("\"", "")
                    images[line] = 1
                    images_of_chart += 1

            # if this chart has no image, log it
            if not images_of_chart:
                with open("out/noImagesList.txt", "a") as file:
                    file.write(file_name + '\n')

            # reading stderr, if contain error, write into file
            if res.poll() is not 0:
                err = res.stderr.read().decode('utf-8')
                if err:
                    print('error with dealing with ' + file_name + ', plz read out/getImagesListError.txt')
                    errors_file.write(file_name + ": ")
                    errors_file.write(err)
            else:
                print(file_name + "'s requirement is all get")
    with open("out/images.txt", "w") as images_file:
        for line in images:
            images_file.write(line)

    print("images list has been saved")


if __name__ == '__main__':
    list_all_image()
