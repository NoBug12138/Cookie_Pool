from cookiespool.scheduler import Scheduler, RedisClient


def main():
    conn_baixing = RedisClient('accounts', 'baixing')
    conn_youxin = RedisClient('accounts', 'youxin')
    conn_baixing.set('18721918121', '1234567')
    conn_youxin.set('youxin001', '1234567')
    s = Scheduler()
    s.run()


if __name__ == '__main__':
    main()