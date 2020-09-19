import pprint

c1 = 'UM_distinctid=174a0a9ce9e9bc-0938a67e9ceea3-31667305-1fa400-174a0a9ce9fb16; CNZZDATA1574657=cnzz_eid%3D1766937287-1600418930-%26ntime%3D1600418930; Hm_lvt_cc6a63a887a7d811c92b7cc41c441837=1600423317; tgbuser=3707036; tgbpwd=788435B9672s589xtktbhcmeck; JSESSIONID=c60096ce-aabd-401f-b4c1-059ce998e465; Hm_lpvt_cc6a63a887a7d811c92b7cc41c441837=1600423321'
c2 = 'tgbuser=3707036; tgbpwd=788435B9672s589xtktbhcmeck; UM_distinctid=174a09f38717dc-0dbb36cdfd7688-31667305-1fa400-174a09f3872ca7; CNZZDATA1574657=cnzz_eid%3D1288858779-1600418930-https%253A%252F%252Fsso.taoguba.com.cn%252F%26ntime%3D1600418930; Hm_lvt_cc6a63a887a7d811c92b7cc41c441837=1600422623; JSESSIONID=a8f41248-de23-46f6-9a20-f33cb7ef431a; Hm_lpvt_cc6a63a887a7d811c92b7cc41c441837=1600422820'

l1 = sorted(c1.split(';'))
l2 = sorted(c2.split(';'))

d1 = {}
for one in l1:
    key, value = tuple(one.split("="))
    key = key.lstrip()
    d1[key] = value

d2 = {}
for one in l2:
    key, value = tuple(one.split("="))
    key = key.lstrip()
    d2[key] = value


print(pprint.pformat(d1))
print(pprint.pformat(d2))

for key in d1:
    print(">>> ", key)
    print(d1[key])
    print(d2[key])
    print()
