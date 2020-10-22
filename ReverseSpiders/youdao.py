import hashlib
import json
import random
import time

import requests


def youdao_trans(word):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
        'Host': 'fanyi.youdao.com',
        'Origin': 'http://fanyi.youdao.com',
        'Referer': 'http://fanyi.youdao.com/',
        'cookie': '''OUTFOX_SEARCH_USER_ID=22609499@10.169.0.82;'''
    }

    # 固定参数
    datas = {
        'from': 'AUTO',    # 自动检测输入
        'to': 'AUTO',      # 自动检测输出
        'smartresult': 'dict',    # 响应格式 fixed
        'client': 'fanyideskweb',   # 客户端标识  fixed
        'doctype': 'json',    # fixed
        'version': 2.1,       # fixed
        'keyfrom': 'fanyi.web',   # fixed
        'action': 'FY_BY_CLICKBUTTION',   # fixed 动态 ajax 或者 捕获点击事件
        'bv': '06f98cf82d0c5619ee1ce529a71d378a',
    }

    salt = int(time.time() * 1000)
    flower_str = "]BjuETDhU)zqSxf-=B#7m"
    sign = hashlib.md5(('fanyideskweb' + word + str(salt) + flower_str).encode('utf-8')).hexdigest()

    # 可变部分
    datas.update({
        'salt': salt,  # l = (new Date).getTime()
        'i': word,
        'sign': sign,
        'lts': salt + random.randint(1, 10),
    })
    post_api = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
    resp = requests.post(post_api, headers=headers, data=datas)

    if resp and resp.status_code == 200:
        body = resp.text
        py_data = json.loads(body)
        try:
            ret = py_data.get("translateResult")[0][0].get("tgt")
        except:
            return None
        return ret
    else:
        return None


if __name__ == '__main__':
    # test

    print(youdao_trans('你好'))
    print(youdao_trans('talk is cheap'))
