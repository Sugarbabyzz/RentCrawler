import pymysql
import time
import datetime

'''
    数据预处理
'''

db = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='rentdb')
cursor = db.cursor()
deleteCursor = db.cursor()

deletedImages = 0
deletedTime = 0
deletedPrice = 0

# 计算各小区平均价格
dict = {}
sql = 'SELECT location, AVG(price) FROM bj GROUP BY location'
try:
    cursor.execute(sql)
    row = cursor.fetchone()
    while row:
        dict[row[0]] = row[1]
        print(row)
        row = cursor.fetchone()
except:
    print('Error')

print(dict)

# 数据处理阶段
sql = 'SELECT * FROM bj'
try:
    cursor.execute(sql)
    print('Count:', cursor.rowcount)
    row = cursor.fetchone()
    while row:
        print('Row:', row)
        # 去除不提供图片的房源
        if '1efeae8459c48eeb3fef0bc54884fd1d' in row[7]:
            # imageDeleteSQL = 'DELETE FROM bj WHERE title = %s' % row[1]
            # deleteCursor.execute(imageDeleteSQL)
            # continue
            deletedImages = deletedImages + 1

        # 比较发布时间
        if not row[9].startswith('2019-06') and not row[9].startswith('2019-05') and not row[9].startswith('2019-04') \
            and not row[9].startswith('2019-03') and not row[9].startswith('2019-02') and not row[9].startswith('2019-01') \
            and not row[9].startswith('2018-12'):
            # imageDeleteSQL = 'DELETE FROM bj WHERE title = %s' % row[1]
            # deleteCursor.execute(imageDeleteSQL)
            # continue
            deletedTime = deletedTime + 1

        # 比较租金
        if row[6]:
            if (float(row[6]) * 1.5) < dict[row[2]]:
            #     imageDeleteSQL = 'DELETE FROM bj WHERE title = %s' % row[1]
            #     deleteCursor.execute(imageDeleteSQL)
            #     continue
                deletedPrice = deletedPrice + 1

        row = cursor.fetchone()

    print('')
    print('正在处理 北京 房源数据...')

    print('当前 北京 共有 %s 条房源数据' % cursor.rowcount)
    print('共有 %s 个小区' % len(dict))
    print('不提供图片的房源数量为 = ', deletedImages)
    print('发布时间过久的房源数量为 = ', deletedTime)
    print('租金过高于当前小区平均水平的房源数量为 =', deletedPrice)

    print('处理结束.')

except:
    print('Error')

