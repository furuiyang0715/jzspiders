'''转移数据
sudo docker build -f Dockerfile -t registry.cn-shenzhen.aliyuncs.com/jzdev/jzdata/jzspi:v2 .

sudo docker push registry.cn-shenzhen.aliyuncs.com/jzdev/jzdata/jzspi:v2

sudo docker pull registry.cn-shenzhen.aliyuncs.com/jzdev/jzdata/jzspi:v2

# local
sudo docker run -itd --name trans_history registry.cn-shenzhen.aliyuncs.com/jzdev/jzdata/jzspi:v2 /bin/bash

# remote
sudo docker run -itd --name trans_history --env LOCAL=0 registry.cn-shenzhen.aliyuncs.com/jzdev/jzdata/jzspi:v2 /bin/bash

docker exec -it trans_history /bin/bash

'''


'''暂时未进行转移
CArticle

GovSpiders 

Taoguba




'''