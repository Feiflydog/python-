import requests

"""
目标：爬取摄影吧源代码，5页内容
1.构造url，请求头
2.获取数据，保存至文件中

"""
class Sheying(object):
    def __init__(self, name, pn):
        # 保存传入的贴吧名称
        self.name = name
        # 构造url
        self.url = "http://tieba.baidu.com/f?kw=%E6%91%84%E5%BD%B1&ie=utf-8&pn=".format(name)
        # 构造请求头
        self.headers = {
            "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) "
                         "AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/50.0.2661.102 Safari/537.36"
        }
        # 构造url列表，用for循环遍历拼接页数
        self.url_list = [self.url + str(pn*50) for pn in range(pn) ]
        # print(self.url_list)

    # 获取数据
    def get_data(self, url):
        response = requests.get(url, headers=self.headers)
        return response.content

    # 保存数据
    def save_data(self, data, num):
        # 构造保存数据的文件名
        file_data = self.name + '_' + str(num) + '.html'
        with open(file_data, 'wb') as f:
            f.write(data)

    def run(self):
        for url in self.url_list:
            # 调用请求方法获取数据
            data = self.get_data(url)
            # 获取url_list列表的索引值
            num = self.url_list.index(url)
            # 保存数据
            self.save_data(data,num)


if __name__ == '__main__':
    sheying = Sheying("摄影吧", 5)
    sheying.run()
