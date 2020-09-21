# 自选股查询
import datetime
import json
import pprint

import requests

url = '''http://www.cninfo.com.cn/new/userAnnouncement/getUserAnnouncementsList'''


def get_user_list():
    '''
    stock: 000651,gssz0000651;002841,9900029752
    searchkey:
    seDate: 2000-01-01~2020-09-21
    sortName: time
    sortType: desc
    tabName: qw
    pageNum: 1
    pageSize: 20
    '''
    post_data = {
        'stock': '000651,gssz0000651;002841,9900029752',
        'searchkey': '',
        'seDate': '2000-01-01~2020-09-21',
        'sortName': 'time',
        'sortType': 'desc',
        'tabName': 'qw',
        'pageNum': 1,
        'pageSize': 20,
    }

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Length': '149',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'www.cninfo.com.cn',
        'Origin': 'http://uc.cninfo.com.cn',
        'Pragma': 'no-cache',
        'Referer': 'http://uc.cninfo.com.cn/user/optionalNotice',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',

    }

    resp = requests.post(url, data=post_data, headers=headers)
    text = resp.text
    py_data = json.loads(text)
    ants = py_data.get("announcements")
    for ant in ants:
        item = dict()
        item['SecuCode'] = ant.get("secCode")
        item['SecuAbbr'] = ant.get("secName")
        item['AntTitle'] = ant.get("announcementTitle")
        time_stamp = ant.get("announcementTime") / 1000
        ant_time = datetime.datetime.fromtimestamp(time_stamp)
        item['AntTime'] = ant_time
        item['AntDoc'] = "http://static.cninfo.com.cn/" + ant.get("adjunctUrl")
        print(item)
        '''
        {
        'adjunctSize': 320,
        'adjunctType': 'PDF',
        'adjunctUrl': 'finalpage/2020-09-17/1208450211.PDF',
        'announcementContent': '',
        'announcementId': '1208450211',
        'announcementTime': 1600272000000,
        'announcementTitle': '关于2018年限制性股票激励计划首次授予限制性股票第二个解除限售期解除限售股份上市流通的提示性公告',
        'announcementType': '01010503||010112||010114||01130340||012325',
        'announcementTypeName': None,
        'associateAnnouncement': None,
        'batchNum': None,
        'columnId': '01010301||01010302||01010411||09020202||250201||251302||2705',
        'id': None,
        'important': None,
        'orgId': '9900029752',
        'orgName': None,
        'pageColumn': 'SZZX',
        'secCode': '002841',
        'secName': '视源股份',
        'storageTime': None, 
        }
        
        '''


if __name__ == '__main__':
    get_user_list()
