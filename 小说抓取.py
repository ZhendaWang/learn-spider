# 爬虫步骤：
# 1. 主页中提取出详情页的url
# 2. 请求详情页url获取文本数据，存储到本地
# 3. 使用线程池加速爬取速度！

# 导入库
import requests
import parsel
import os
from multiprocessing.dummy import Pool


class JinyongSpider(object):

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
        }
        # 保存子页面的url
        self.titles = []
        self.chapter_links = []

        # 创建一个文件夹
        if not os.path.exists('../鹿鼎记'):
            os.mkdir('../鹿鼎记')


    def parse_home_page(self, url='http://jinyong.zuopinj.com/3/'):
        # 发起请求
        response = requests.get(url, headers=self.headers)
        # 修改编码
        response.encoding = response.apparent_encoding
        # 解析数据
        selector = parsel.Selector(response.text)
        # 获取数据
        title = selector.xpath('//div[@class="book_list"]/ul/li/a/@title').extract()
        chapter_link = selector.xpath('//div[@class="book_list"]/ul/li/a/@href').extract()

        # 追加数据
        self.titles.extend(title)
        self.chapter_links.extend(chapter_link)


    def parse_detail_page(self, zip_list):
        print(f'正在爬取{zip_list[0]}章节的小说！')

        # 发起请求
        response = requests.get(url=zip_list[1], headers=self.headers)
        # 修改编码
        response.encoding = response.apparent_encoding
        # 解析数据
        selector = parsel.Selector(response.text)
        # 获取数据
        noval_text = selector.xpath('//div[@id="htmlContent"]//text()').extract()
        noval_text = '\n'.join(noval_text)

        # 写出数据
        with open(f'../鹿鼎记/{zip_list[0]}.txt', 'w', encoding='utf-8') as fp:
            print(f'正在写入{zip_list[0]}章')
            fp.write(noval_text)
            fp.close()
            print('写入完毕，关闭文件！')


    def multiprocees_function(self):
        # 实例化线程，一个进程开启多个线程
        pool = Pool(10)
        zip_list = list(zip(self.titles, self.chapter_links))
        # map操作(将zip_list中的每一个列表元素map到get_video_data的函数中，parse_detail_page这个函数接收的是列表元素)
        pool.map(self.parse_detail_page, zip_list)
        # 关闭线程池
        pool.close()
        # 主线程等待子线程结束之后再结束
        pool.join()


if __name__ == '__main__':
    # 实例化对象
    jinyongspider = JinyongSpider()
    # 先获取子页面链接
    jinyongspider.parse_home_page(url='http://jinyong.zuopinj.com/3/')
    # 再通过线程池运行爬虫
    jinyongspider.multiprocees_function()
