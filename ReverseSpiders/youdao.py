import json
import pprint

import requests


def youdao_trans():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
        'Host': 'fanyi.youdao.com',
        'Origin': 'http://fanyi.youdao.com',
        'Referer': 'http://fanyi.youdao.com/',
        'cookie': 'OUTFOX_SEARCH_USER_ID=22609499@10.169.0.82; OUTFOX_SEARCH_USER_ID_NCOO=630557637.603828; _ga=GA1.2.1032060675.1592288066; _ntes_nnid=23cb853a21d77c5264e28f2c59cc9f2b,1592891475973; JSESSIONID=aaa0eq4z9k1AYfSZl6rux; SESSION_FROM_COOKIE=unknown; ___rl__test__cookies=1603277050695'
    }

    datas = {
        'i': '在',
        'from': 'AUTO',
        'to': 'AUTO',
        'smartresult': 'dict',
        'client': 'fanyideskweb',
        'salt': 16032767568800,
        'sign': 'fab9a8633e875e8b442033e220f0ba73',
        'lts': 1603276756880,
        'bv': '06f98cf82d0c5619ee1ce529a71d378a',
        'doctype': 'json',
        'version': 2.1,
        'keyfrom': 'fanyi.web',
        'action': 'FY_BY_CLICKBUTTION',
    }

    print(pprint.pformat(datas))
    post_api = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
    resp = requests.post(post_api, headers=headers, data=datas)

    if resp and resp.status_code == 200:
        body = resp.text
        py_data = json.loads(body)
        print(py_data)
        ret = py_data.get("translateResult")[0][0].get("tgt")
        return ret
    else:
        print(resp)
        return {}


if __name__ == '__main__':
    print(youdao_trans())
