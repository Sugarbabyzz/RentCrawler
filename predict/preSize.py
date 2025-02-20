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

# 西城 152.24 -1025.94
# 东城 130.90 471.94
# 丰台 78.41 481.42
# 房山 45.56 213.20
# 昌平 59.71 516.64
# 朝阳 128.54 -779.85
# 海淀 112.52 431.72
# 石景山 79.13 558.67
# 通州 58.96 -41.02
sql = 'SELECT * FROM bj WHERE area = "通州" and size < 400'
try:
    cursor.execute(sql)
    print('Count:', cursor.rowcount)
    row = cursor.fetchone()
    while row:
        print('Row:', row)

        x.append(int(row[3]))
        y.append(int(row[6]))
        # y.append(int(row[6])/int(row[3]))

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


