import os

from spiders_cfg import spiders_config


def build_docker_image():
    command = 'docker build -f Dockerfile -t registry.cn-shenzhen.aliyuncs.com/jzdev/jzdata/jzspi:v1 .'
    os.system(command)


def clear_all_containers():
    for contain_name in spiders_config:
        command = 'docker rm -f {}'.format(contain_name)
        os.system(command)
