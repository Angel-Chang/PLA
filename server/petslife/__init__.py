import pymysql
pymysql.install_as_MySQLdb()

import logging

# 基礎設定
logging.basicConfig(level=logging.WARNING,
                    format='[%(levelname)-8s] %(asctime)s | %(name)s:%(lineno)d | %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    handlers = [logging.FileHandler('server.log', 'a', 'utf-8'),])
 
# 定義 handler 輸出 sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
# 設定輸出格式
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
# handler 設定輸出格式
console.setFormatter(formatter)
# 加入 hander 到 root logger
logging.getLogger('').addHandler(console)