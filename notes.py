'''转移数据
sudo docker build -f Dockerfile -t registry.cn-shenzhen.aliyuncs.com/jzdev/jzdata/jzspi:v2 .

sudo docker push registry.cn-shenzhen.aliyuncs.com/jzdev/jzdata/jzspi:v2

sudo docker pull registry.cn-shenzhen.aliyuncs.com/jzdev/jzdata/jzspi:v2

# local
sudo docker run -itd --name trans_history registry.cn-shenzhen.aliyuncs.com/jzdev/jzdata/jzspi:v2 /bin/bash

# remote
sudo docker run -itd --name trans_history --env LOCAL=0 registry.cn-shenzhen.aliyuncs.com/jzdev/jzdata/jzspi:v2 /bin/bash
# 对于数据量比较大的东财以及淘股吧
sudo docker run -itd --name dc --env LOCAL=0 registry.cn-shenzhen.aliyuncs.com/jzdev/jzdata/jzspi:v2 python CArticle/ca_main.py
sudo docker run -itd --name tgb --env LOCAL=0 registry.cn-shenzhen.aliyuncs.com/jzdev/jzdata/jzspi:v2 python Taoguba/tgb_main.py


docker exec -it trans_history /bin/bash

'''


'''暂时未进行转移
CArticle

GovSpiders 

Taoguba




'''