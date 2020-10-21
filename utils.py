import os
import sys

from spiders_cfg import spiders_config


def build_docker_image():
    command = 'sudo docker build -f Dockerfile -t registry.cn-shenzhen.aliyuncs.com/jzdev/jzdata/jzspi:v1 .'
    os.system(command)


def clear_all_containers():
    for contain_name in spiders_config:
        command = 'sudo docker rm -f {}'.format(contain_name)
        os.system(command)


def sync_to_server():
    command = '''rsync -e 'ssh -p 9528' -avz  /Users/furuiyang/gitzip/DjangoDemos/JZSpiders furuiyang@139.9.193.142:/home/furuiyang/ '''
    os.system(command)


def start_main_thread():
    # source /home/furuiyang/jzspi/bin/activate
    command = '''sudo /home/furuiyang/jzspi/bin/python3 main.py start'''
    os.system(command)


def catch_logs():

    pass


if __name__ == '__main__':
    args = sys.argv[1]
    if args == "1":   # 同步到服务器
        sync_to_server()
    elif args == '2':  # 清空容器
        clear_all_containers()
    elif args == '3':  # 构建镜像
        build_docker_image()
    elif args == '4':  # 启动主进程
        start_main_thread()
    elif args == '5':   # 服务器流
        clear_all_containers()
        build_docker_image()
        start_main_thread()


'''部署流程 
（1） 同步到服务器:  python utils.py 1; 检查 .conf 文件中的 LOCAL 为 0; 清理下本地的测试日志;
（2） 激活服务器虚拟环境：  source /home/furuiyang/jzspi/bin/activate 
（3） 清理旧容器、构建、启动: python utils.py 5 


'''