import matplotlib.pyplot as plt
from matplotlib import font_manager

#设置字体，让图形支持中文
myfont = font_manager.FontProperties(fname='/Users/sugar/Documents/GitHub/RentCrawler/predict/simsun.ttc')

input_valuse = ["东城", "西城", "朝阳", "海淀", "石景山", "丰台", "昌平", "通州", "房山"]
# squares = [143.7, 140.1, 122.1, 121.8, 88.1, 87.4, 67.9, 60.2, 51.6]
squares = [12417, 11032, 13438, 11888, 6642, 7294, 6884, 5312, 3858 ]
plt.plot(input_valuse, squares, linewidth=5)

plt.title("北京", fontsize=25, fontproperties = myfont)
plt.xlabel("城区", fontsize=15, fontproperties = myfont)
plt.ylabel("平均租金", fontsize=15, fontproperties = myfont)
plt.xticks(fontproperties = myfont)
plt.tick_params(axis='both', labelsize=14)

for a, b in zip(input_valuse, squares):
    plt.text(a, b, b, ha='center', va='bottom', fontsize=10)

plt.savefig('./位置/位置图.jpg')
plt.show()
