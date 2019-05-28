from sklearn.linear_model import LinearRegression
from matplotlib import pyplot as plt
from matplotlib import font_manager
import numpy as np
import requests
import re
from lxml import etree
import time


#下面是爬虫代码
page = 1
x = [] #存放所有的x，就是房屋面积
y = [] #存放所有的y，就是租房价格
base_url = "https://su.lianjia.com"
while page < 2: #这里设置获取多少页房产信息
    time.sleep(1) #休眠1秒
    #每一页的url地址，page参数是页码
    request_url = base_url + "/zufang/gongyeyuan/pg" + str(page) + "/#contentList"
    print(request_url)
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"
    }
    respnose = requests.get(request_url,headers=headers) #发请求加入User-Agent头信息，不然链家会拒绝请求
    html = respnose.content.decode("utf-8") #获取html网页字节内容并转换为字符串
    selector = etree.HTML(html)
    list = selector.xpath('//div[@class="content__list--item"]')
    for item in list:
        title = item.xpath("./div/p[1]/a/text()")[0].strip() #通过xpath获取标题
        price = item.xpath("./div/span/em/text()")[0].strip() #通过xpath获取价格，价格y值
        price = price.split("-")[0]
        # 通过xpath获取价格，房屋面积作为样本特征x
        area = item.xpath("./div/p[2]/text()")
        area = "".join(area).replace("\n","")
        m = re.match(r'.* (\d{1,4})㎡', area) #通过正则匹配价格
        if m != None:
            x.append(int(m.group(1))) #获取面积
            y.append(int(price)) #获取价格
    page = page + 1

#下面是训练代码
linearReg = LinearRegression()
X = np.array([x])
y = np.array([y])
X = X[y <= 10000] #只考虑租房价格10000元以内的房子
y = y[y <= 10000] #只考虑租房价格10000元以内的房子
X = X.reshape(-1,1) #转成二维数组，固定1列（一个特征），行为自动
plt.scatter(X,y,color="b")  #根据矩阵X和向量y，把训练及的点画在图形上
linearReg.fit(X,y)  #根据矩阵X和向量y，进行训练
k = linearReg.coef_[0]  #系数
b = linearReg.intercept_ #截距
plt.plot(X,k * X + b,color="r")  # 根据训练所得的系数k和截距b，画出所得模型，其实就是直线方程 y = kX + b
plt.xlabel("House Size")
plt.ylabel("Price")

#下面是预测代码
predict_x = [[50],[120]] #分别预测面积未50和120的租房价格
predict_y = linearReg.predict(predict_x)
print(predict_y)
plt.scatter(predict_x,predict_y,color="g") #预测的两个点画到图形上

plt.legend()
plt.show() #显示图形
