#### 安装
```
pip3 install -r requirements.txt
```
#### 进程开关
在config.py修改
```
# 产生器开关，模拟登录添加Cookies
GENERATOR_PROCESS = True
# 验证器开关，循环检测数据库中Cookies是否可用，不可用删除
VALID_PROCESS = True
# API接口服务
API_PROCESS = True
```
#### 访问URL
```
0.0.0.0:5000/baixing/random
```
#### redis存储字段
```
"cookies:baixing"  # cookie存储，格式set
"accounts:baixing"  # 账号密码存储，格式hash
```
#### 启动
1. 方式一
```
python3 run.py
```
2. 方式二
```
sh start.sh
```
