import requests
from lxml import etree
import os
"""
目标：
1.构造url和请求头
2.获取源码
3.解析数据
4.保存数据

"""


class Sheying(object):
    def __init__(self, name):
        self.url = "http://tieba.baidu.com/f?ie=utf-8&kw={}".format(name)
        self.headers = {
            "User-Agent":"Mozilla/4.0 (compatible; MSIE 5.01; Windows NT 5.0)"

        }

    # 获取数据
    def get_data(self, url):
        response = requests.get(url, headers=self.headers)
        return response.content

    # 解析列表页数据，获取列表页面标题和链接
    def parse_list_data(self, data):
        # 写入文件
        with open("sheying.html", "wb") as f:
            f.write(data)
        # 实例化etree对象
        html = etree.HTML(data)
        # 使用xpath语法提取数据
        node_list = html.xpath('//*[@id="thread_list"]/li/div/div[2]/div[1]/div[1]/a')
        data_list = []
        # 循环遍历node_list
        for node in node_list:
            garage = {}
            garage['url'] = 'http://tieba.baidu.com' + node.xpath('./@href')[0]
            garage['title'] = node.xpath('./text()')[0]
            data_list.append(garage)

        # 提取下一页的节点
        next_page = html.xpath('//*[@id="frs_list_pager"]/a[last()-1]/@href')[0]
        # 拼接url
        next_url = 'http:' + next_page
        return data_list, next_url

    # 分析图片链接
    def parse_detail(self, data_list):
        html = etree.HTML(data_list)
        # 提取页面图片链接
        images_list = html.xpath("//cc/div[contains(@class,'d_post')]/img[@class='BDE_Image']/@src")
        # 返回图片节点列表
        print(images_list)
        return images_list

    # 下载图片，保存图片文件
    def download(self, image_list):
        if not os.path.exists('images'):
            os.makedirs('images')

        for image in image_list:
            file_name = 'images' + os.sep + image.split('/')[-1]
            image_data = self.get_data(image)
            # 写入文件
            with open(file_name, 'wb') as f:
                f.write(image_data)

    def run(self):
        next_url = self.url
        while next_url:
            # 获取数据
            data = self.get_data(self.url)
            # 解析列表页数据，返回列表数据和下一页数据
            # next_url和data_list顺序反了
            # next_url, data_list = self.parse_list_data(data)
            data_list, next_url = self.parse_list_data(data)
            # 利用for循环解析详情页数据，获取图片链接
            for data in data_list:
                url = data['url']
                get_list = self.get_data(url)
                images_list = self.parse_detail(get_list)
                # 保存数据
                self.download(images_list)


if __name__ == '__main__':
    sheying = Sheying('摄影吧')
    sheying.run()