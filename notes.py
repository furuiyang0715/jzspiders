'''转移数据
sudo docker build -f Dockerfile -t registry.cn-shenzhen.aliyuncs.com/jzdev/jzdata/jzspi:v2 .

sudo docker run -itd --name trans_history registry.cn-shenzhen.aliyuncs.com/jzdev/jzdata/jzspi:v2 /bin/bash

docker exec -it trans_history /bin/bash

'''