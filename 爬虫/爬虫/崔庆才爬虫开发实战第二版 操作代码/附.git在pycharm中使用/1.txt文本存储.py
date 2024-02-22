import requests
from  pyquery import PyQuery as pq
import re
urls=[]
for i in range(1,11):
    print(i)
    url=f'https://ssr1.scrape.center/page/{i}'
    urls.append(url)
print(urls)
# ‘w’ 以覆盖方法写入
file=open('movies.txt','w',encoding='utf-8')
# 遍历每一页的url 并请求
for url in urls:
    html = requests.get(url).text
    doc = pq(html)
    # 遍历每一页的.el-card电影html选项容器
    for item in doc('.el-card').items():
    #电影名称 (item为pyuery对象)
        name=item.find('a>h2').text()
        print(name)
        file.write(f'名称: {name}\n')
        # 分类
        categories=item.find('.categories button span')
        # print(categories)
        # print(categories.text())
        # print(type(categories.text()))#字符串型
        categories=categories.text()
        file.write(f'类型：{categories}\n')
        #上映时间
        publish_at_div=item.find('.info:contains(上映)')#div
                # 包含‘上映’的.info div内的文本
        publish_at_str=item.find('.info:contains(上映)').text()#'1993-07-26 上映'
        #匹配1993-07-26 上映中的 数字“1993-07-26”
        # publish_at_re_str=re.search('\d{4}-\d{2}-\d{2}',publish_at_str)
        # print(type(publish_at_re_str))#<class 're.Match'>对象
        # publish_at_re_str=re.search('(\d{4}-\d{2}-\d{2})',publish_at_str).group(1)
        # print(type(publish_at_re_str))#<class 'str'>字符串
        # 如果当前电影没有 发布日期则设置为 空，如果有则设置为以上的正则表达式
        # ★三元表达式解析： 如果div下的文本存在 且 在此文本内 可提取“1993-07-26”这样格式 的数字
        #★则下行代码： 左 接收 右边的赋值（“1993-07-26”格式），否则None赋值给左式
        publish_at_re_str = re.search('(\d{4}-\d{2}-\d{2})',publish_at_str).group(1)\
        if publish_at_str and re.search('\d{4}-\d{2}-\d{2}',publish_at_str) else None
        file.write(f'上映时间：{publish_at_re_str}\n')
        #评分
        score=item.find('p.score').text()#class='score'的p
        file.write(f'评分：{score}\n')
        file.write(f'{"="*50}\n')

    #  每轮for循环代表 一个el-card的div元素
    # 等待当前页面 电影全部写完（全部el-card的div元素写完） 保存
file.close()