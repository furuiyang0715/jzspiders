# 单独部署巨潮资讯全网
import os
import sys
import time

import schedule

cur_path = os.path.split(os.path.realpath(__file__))[0]
file_path = os.path.abspath(os.path.join(cur_path, ".."))
sys.path.insert(0, file_path)

from Juchaodaynews.jcspider import JuchaoDayNews
from Juchaodaynews.juchao_info import JuChaoInfo


def module_start():
    # 巨潮快讯
    JuchaoDayNews().start()
    # 巨潮 AI 资讯
    # JuChaoInfo().start()

    print("hello ~~ ")


if __name__ == '__main__':
    module_start()

    # schedule.every(10).seconds.do(module_start)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(10)
