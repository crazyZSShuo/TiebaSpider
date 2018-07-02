import requests
# from scrapy import Selector
from lxml import etree
import time
headers = {
	'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36',
	'Referer':'http://tieba.baidu.com'
}
url = 'http://tieba.baidu.com/f?kw=%E7%94%9F%E6%B4%BB%E5%A4%A7%E7%88%86%E7%82%B8&ie=utf-8&pn=0'
res = requests.get(url,headers = headers)
time.sleep(1)
res.encoding = 'utf-8'
resp = etree.HTML(res.text)
titles = resp.xpath('//div[@class = "threadlist_title pull_left j_th_tit "]/a/text()')
links =  resp.xpath('//div[@class = "threadlist_title pull_left j_th_tit "]/a/@href')
names = resp.xpath('//span[@class = "tb_icon_author_rely j_replyer"]/a/text()')
times = resp.xpath('//span[@class = "threadlist_reply_date pull_right j_reply_data"]/text()')
Nums = resp.xpath('//span[@class = "threadlist_rep_num center_text"]/text()')
		# print(titles)
		# print(title,link,name,time,Num)
for title,link,name,time,Num in zip(titles,links,names,times,Nums):
	data = {
	'标题':title,
	'链接':'https"//tieba.baidu.com'+link,
	'发帖人':name,
	'发表时间':time.strip(),
	'回帖数量':Num
	}
	print(data)
		# 	data_list.append(data)
		# return data_list
# def write_to_file(data_list):
# 	with open('./tieba.txt','a+') as f :
# 		for data in data_list:
# 			f.write(data)
# 		f.close()
# 		print('写入完成！')


def main(deep):
	url_list = []
	# 构造翻页
	host_url = 'http://tieba.baidu.com/f?kw=%E7%94%9F%E6%B4%BB%E5%A4%A7%E7%88%86%E7%82%B8&ie=utf-8&pn='
	for i in range(0,deep+1):
		url_list.append(host_url+str(i*50))
	for page_link in url_list:
		get_content(page_link)
		# write_to_file(dic)

if __name__ == '__main__':
	print('欢迎来到贴吧！！')
	deeps = input('请输入你要爬取的页码：')
	print('好的，我已经接受你的页码，页码为：{}'.format(deeps))
	print('开始爬取中，请稍后。。。。。')
	num = int(deeps)
	main(num)

