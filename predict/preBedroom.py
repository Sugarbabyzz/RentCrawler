import pymysql
from sklearn.linear_model import LinearRegression
from matplotlib import pyplot as plt
from matplotlib import font_manager
import numpy as np
import re

#设置字体，让图形支持中文
myfont = font_manager.FontProperties(fname='/Users/sugar/Documents/GitHub/RentCrawler/predict/simsun.ttc')

#下面是爬虫代码

db = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='rentdb')
cursor = db.cursor()

x = [] #存放所有的x，就是房屋面积
y = [] #存放所有的y，就是租房价格



# 西城 4786.52 1227.04
# 东城 4862.12 2297.26
# 丰台 2933.32 902.41
# 房山 1221.07 1088.26
# 昌平 2539.52 513.83
# 朝阳 5423.17 781.52
# 海淀 4565.65 830.95
# 石景山 2499.64 1447.86
# 通州 2074.59 639.69

# 卧室数量
sql = 'SELECT * FROM bj WHERE area = "通州" and size < 400'
try:
    cursor.execute(sql)
    print('Count:', cursor.rowcount)
    row = cursor.fetchone()
    while row:
        print('Row:', row)

        if '室' in row[5]:
            m = re.match('(.*)室', row[5])
        elif '房间' in row[5]:
            m = re.match('(.*)房间', row[5])

        x.append(int(m.group(1)))
        y.append(int(row[6]))   # 租金
        row = cursor.fetchone()
except:
    print('Error')


#下面是训练代码
linearReg = LinearRegression()
X = np.array([x])
y = np.array([y])
X = X[y <= 50000] #只考虑租房价格100000元以内的房子
y = y[y <= 50000] #只考虑租房价格100000元以内的房子
X = X.reshape(-1,1) #转成二维数组，固定1列（一个特征），行为自动
plt.scatter(X,y,color="b")  #根据矩阵X和向量y，把训练及的点画在图形上
linearReg.fit(X,y)  #根据矩阵X和向量y，进行训练
k = linearReg.coef_[0]  #系数
b = linearReg.intercept_ #截距
plt.plot(X,k * X + b,color="r")  # 根据训练所得的系数k和截距b，画出所得模型，其实就是直线方程 y = kX + b
plt.xlabel("发布月份 / 月",fontproperties = myfont, fontsize=15)
# plt.xlabel("月份 / 月",fontproperties = myfont, fontsize=25)
plt.ylabel("租金 / 元",fontproperties = myfont, fontsize=15)
plt.title("北京-西城",fontproperties = myfont, fontsize=25)

#下面是预测代码
predict_x = [[2],[4]] #分别预测面积未50和120的租房价格
predict_y = linearReg.predict(predict_x)
print(predict_y)
plt.scatter(predict_x,predict_y,color="g") #预测的两个点画到图形上
print('k=', k, ',b=', b)

plt.legend()
# plt.savefig('./发布时间/时间.jpg')
plt.show() #显示图形


