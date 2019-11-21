from pathlib import Path
import requests
import http_util
import os
import re

from os import sys, path
from importlib import reload
reload(sys)
sys.path.append(path.dirname(path.abspath(__file__)))
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from conf import env_conf
from utils import file_util
from utils import docker_util


def scan_images():
    image_prefix = "{username}/mykubeflow.".format(username=env_conf.global_params['docker']['username'])
    image_list_file = env_conf.root_dir + "/deploy/record.txt"
    images = file_util.read_str_file(image_list_file).strip().split("\n")

    mapping = []
    for image in images:
        image = image.strip()
        new_image = image_prefix + image.replace("/", ".").strip()
        mapping.append({"from": image, "to": new_image})
    record_path = env_conf.root_dir + "/deploy/records.yaml"
    file_util.write_yaml_file(mapping, record_path)


def make_new_deploy():
    mapping_file = env_conf.root_dir + "/deploy/records.yaml"
    mappings = file_util.read_yaml_file(mapping_file)

    di = {}
    for r in mappings:
        for pair in r:
            di[pair['from'].split(":")[0]] = pair['to'].split(":")[0]

    content = file_util.read_str_file(env_conf.root_dir + "/deploy/kfserving.old.yaml")
    for key, value in di.items():
        content = content.replace(key, value)
    file_util.write_str_file(content, env_conf.root_dir + "/deploy/kfserving.yaml")


def diy_docker_images():
    mapping_file = env_conf.root_dir + "/deploy/records.yaml"
    mappings = file_util.read_yaml_file(mapping_file)

    docker_util.login()

    for r in mappings:
        for pair in r:
            image = pair['from']
            new_image = pair['to']
            docker_util.image_pull_v2(image)
            docker_util.image_tag_v2(image, new_image)
            docker_util.image_push_v2(new_image)


if __name__ == '__main__':
    make_new_deploy()
