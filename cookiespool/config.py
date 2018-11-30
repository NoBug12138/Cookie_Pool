# Redis数据库地址
REDIS_HOST = '127.0.0.1'

# Redis端口
REDIS_PORT = 6379

# Redis密码，如无填None
REDIS_PASSWORD = None

# Redis DB
REDIS_DB = 1

# 产生器使用的浏览器
BROWSER_TYPE = 'Chrome'

# 产生器类，如扩展其他站点，请在此配置
GENERATOR_MAP = {
    'baixing': 'BaixingCookiesGenerator',
    'youxin': 'YouxinCookiesGenerator'
}

# 测试类，如扩展其他站点，请在此配置
TESTER_MAP = {
    'baixing': 'BaixingValidTester',
    'youxin': 'YouxinValidTester'
}

TEST_URL_MAP = {
    'baixing': 'http://shanghai.baixing.com/cheliang/?src=topbar'
}

# 产生器和验证器循环周期
CYCLE = 5

# API地址和端口
API_HOST = '0.0.0.0'
API_PORT = 5000

# 产生器开关，模拟登录添加Cookies
GENERATOR_PROCESS = True
# 验证器开关，循环检测数据库中Cookies是否可用，不可用删除
VALID_PROCESS = True
# API接口服务
API_PROCESS = True
