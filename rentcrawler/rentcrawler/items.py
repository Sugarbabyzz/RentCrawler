from scrapy import Field, Item


class HouseItem(Item):

    house_city = Field()            # 所属城市
    house_title = Field()           # 房源信息标题
    house_location = Field()        # 城市城区
    house_lnglat = Field()          # 经纬度
    house_size = Field()            # 面积
    house_orient = Field()          # 朝向
    house_type = Field()            # 户型
    house_time = Field()            # 发布时间
    house_price = Field()           # 价钱
    house_image = Field()           # 照片
    house_url = Field()             # 链接
    house_refer = Field()           # 来源
    house_area = Field()            # 城区





