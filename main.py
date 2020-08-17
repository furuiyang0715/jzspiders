# coding=utf8
import functools
import os
import sys
import time
import traceback

import docker
import schedule
import utils

cur_path = os.path.split(os.path.realpath(__file__))[0]
file_path = os.path.abspath(os.path.join(cur_path, ".."))
sys.path.insert(0, file_path)

from daemon import Daemon
from configs import LOCAL
from base_spider import logger, SpiderBase
from spiders_cfg import spiders_config


def catch_exceptions(cancel_on_failure=False):
    def catch_exceptions_decorator(job_func):
        @functools.wraps(job_func)
        def wrapper(*args, **kwargs):
            try:
                return job_func(*args, **kwargs)
            except:
                logger.warning(traceback.format_exc())
                # sentry.captureException(exc_info=True)
                if cancel_on_failure:
                    logger.warning("异常 任务结束: {}".format(schedule.CancelJob))
                    schedule.cancel_job(job_func)
                    return schedule.CancelJob
        return wrapper
    return catch_exceptions_decorator


class DockerSwith(SpiderBase, Daemon):
    def __init__(self, *args, **kwargs):
        super(DockerSwith, self).__init__()    # init SpiderBase
        super(SpiderBase, self).__init__(*args, **kwargs)     # init Daemon
        self.docker_client = docker.from_env()
        self.docker_containers_col = self.docker_client.containers

    def ding_crawl_information(self):
        self._spider_init()
        msg = ''
        for table, info in spiders_config.items:
            dt_benchmark = info[-2]
            sql = '''SELECT count(id) as inc_count FROM {} WHERE {} > date_sub(CURDATE(), interval 1 day);'''.format(table, dt_benchmark)
            inc_count = self.spider_client.select_one(sql).get("inc_count")
            msg += '{} 今日新增 {}\n'.format(table, inc_count)
        if not LOCAL:
            self.ding(msg)
        else:
            print(msg)

    def docker_run_spider(self, spider_name, spider_file_path, restart=False):
        local_int = 1 if LOCAL else 0
        try:
            spider_container = self.docker_containers_col.get(spider_name)
        except:
            spider_container = None

        if spider_container:
            spider_status = spider_container.status
            logger.info("{} spider status: {}".format(spider_name, spider_status))
            if spider_status in ("exited",):
                spider_container.start()
            elif spider_status in ("running",):
                if restart:
                    spider_container.restart()
            else:
                logger.warning("other status: {}".format(spider_status))
        else:
            self.docker_containers_col.run(
                "registry.cn-shenzhen.aliyuncs.com/jzdev/jzdata/jzspi:v1",
                environment={"LOCAL": local_int},
                name='{}'.format(spider_name),
                command='python {}'.format(spider_file_path),
                detach=True,    # 守护进程运行
            )
            print("start success")

    def start_task(self, spider_name, spider_file_path, dt_str, restart=False):
        """
        使用定时任务每天固定时间启动 docker 进程
        :param spider_name: 爬虫名称/容器名
        :param spider_file_path: 爬虫文件路径
        :param dt_str: 定时任务时间字符串
        :param restart: 如果前一个任务的容器还在运行 是否进行重启
        :return:
        """
        @catch_exceptions(cancel_on_failure=True)
        def task():
            self.docker_run_spider(spider_name, spider_file_path, restart)
        schedule.every().day.at(dt_str).do(task)

    def interval_start_task(self, spider_name, spider_file_path, interval, restart=True):
        """
        使用定时任务固定间隔启动 docker 进程
        :param spider_name:
        :param spider_file_path:
        :param interval: 元组（间隔时间, 间隔单位）eg. (10, "minutes"), 每 10 分钟运行一次
        :param restart:
        :return:
        """
        @catch_exceptions(cancel_on_failure=True)
        def task():
            self.docker_run_spider(spider_name, spider_file_path, restart)
        sche = schedule.every(interval[0])
        assert interval[1] in ('seconds', 'minutes', 'hours', 'days', 'weeks')
        sche.unit = interval[1]
        sche.do(task)

    def run(self):
        for name, info in spiders_config.items():
            file_path = info[0]
            start_method = info[1]
            start_params = info[2]

            print(file_path)
            print(start_method)
            print(start_params)

            self.docker_run_spider(name, file_path)
            if start_method == 'interval':
                self.interval_start_task(name, file_path, start_params)
            else:
                pass

        self.ding_crawl_information()
        schedule.every(10).hours.do(self.ding_crawl_information)

        while True:
            schedule.run_pending()
            time.sleep(10)


if __name__ == "__main__":
    utils.clear_all_containers()
    utils.build_docker_image()

    pid_file = os.path.join(cur_path, 'main.pid')
    log_file = os.path.join(cur_path, 'main.log')
    worker = DockerSwith(
        pidfile=pid_file,
        stdout=log_file,
        stderr=log_file
    )

    if len(sys.argv) >= 2:
        if 'start' == sys.argv[1]:
            worker.start()
        elif 'stop' == sys.argv[1]:
            worker.stop()
        elif 'restart' == sys.argv[1]:
            worker.restart()
        elif 'status' == sys.argv[1]:
            worker.status()
        else:
            sys.stderr.write("Unknown command\n")
            sys.exit(2)
        sys.exit(0)
    else:
        sys.stderr.write("usage: %s start|stop|restart\n" % sys.argv[0])
        sys.exit(2)
