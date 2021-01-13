# 导入所需库
import requests

class Jdcomment_spider(object):

    # 请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'
    }

    def __init__(self, file_name='jd_commet'):
        # 实例化类的时候运行初始化函数
        # 打开文件
        self.fp = open(f'./{file_name}.txt', 'w', encoding='utf-8')

        print(f'正在打开文件{file_name}.txt文件!')


    def parse_one_page(self, url):
        # 指定url
        # url = 'https://club.jd.com/comment/productPageComments.action?productId=10023108638660&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&rid=0&fold=1'
        # print(url)

        # 发起请求
        response = requests.get(url, headers=self.headers)
        # 获取响应
        js_data = response.json()

        # 提取评论列表
        comments_list = js_data['comments']

        for comment in comments_list:
            # 商品id
            goods_id = comment.get('id')
            # 用户昵称
            nickname = comment.get('nickname')
            # 评分
            score = comment.get('score')
            # 商品尺寸
            productSize = comment.get('productSize')
            # 商品颜色
            productColor = comment.get('productColor')
            # 评论时间
            creationTime = comment.get('creationTime')
            # 评论内容
            content = comment.get('content')
            content = ' '.join(content.split('\n'))  # 处理换行符

            print(content)

            # 循环写出数据
            self.fp.write(f'{goods_id}\t{nickname}\t{score}\t{productSize}\t{productColor}\t{creationTime}\t{content}\n')


    def parse_max_page(self):
        for page_num in range(49):  # 抓包获得最大页数
            # 指定通用的url模板
            new_url = f'https://club.jd.com/comment/productPageComments.action?productId=10023108638660&score=0&sortType=5&page={page_num}&pageSize=10&isShadowSku=0&rid=0&fold=1'

            print(f'正在获取第{page_num}页')

            # 调用函数
            self.parse_one_page(url=new_url)


    def close_files(self):
        self.fp.close()
        print('爬虫结束，关闭文件！')


if __name__ == '__main__':
    # 实例对象
    jd_spider = Jdcomment_spider()
    # 开始爬虫
    jd_spider.parse_max_page()
    # 关闭文件
    jd_spider.close_files()