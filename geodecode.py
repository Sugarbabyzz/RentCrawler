
import requests

def geocode(address):
    parameters = {'address': address, 'key': 'cb649a25c1f81c1451adbeca73623251'}
    base = 'http://restapi.amap.com/v3/geocode/geo'
    response = requests.get(base, parameters)
    answer = response.json()
    print('')
    print('正在解析 ' + address + ' 的经纬度...')
    print('获取解析结果如下：')
    print(answer['geocodes'])
    print('经纬度获取成功...')
    print(' ' + address + ' 的经纬度：[' + answer['geocodes'][0]['location'] + ']' )


if __name__ == '__main__':
    address = '北京科技大学'
    geocode(address)

