from bs4 import BeautifulSoup
import requests
import time
headers = {
	'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36',
	'Referer':'http://tieba.baidu.com'
}

# 抓取网页的方法
def get_html(url):
	try:
		res = requests.get(url,headers = headers,timeout = 30)
		res.raise_for_status()
		res.encoding = 'utf-8'
		return res.text

	except Exception as e:
		return 'Error!'

def get_content(url):
	# 初始化一个列表来保存所有的帖子信息
	comments = [] 
	html = get_html(url)
	soup = BeautifulSoup(html,'lxml')
	# 找到所有li标签class属性，返回一个列表
	liTags = soup.find_all('li',attrs = {'class':'j_thread_list clearfix'})

	# 通过循环 找到每个帖子里我们需要的信息
	for li in liTags:
		# 初始化一个字典来存储文章信息
		comment = {}
		try:
			# 筛选信息 保存到字典中
			comment['title'] = li.find('a',attrs = {'class':'j_th_tit'}).text.strip()
			comment['link']  = 'http://tieba.baidu.com/'+li.find('a',attrs = {'class':'j_th_tit'})['href']
			comment['name']  = li.find('span',attrs = {'class':'tb_icon_author'}).text.strip()
			comment['time']  = li.find('span',attrs = {'class':'threadlist_reply_date pull_right j_reply_data'}).text.strip()
			comment['replyNum'] = li.find('span',attrs = {'class','threadlist_rep_num center_text'}).text.strip()
			comments.append(comment) # 把字典结构保存到列表中 并返回
		except:
			print('This is Error！')
	# 返回保存字典信息的列表
	return comments

# 把信息保存到本地的方法
def write_to_file(dict):
	with open('./tieba.txt','a+') as f:
		for comment in dict:
			f.write('标题：{} \t 链接：{} \t 发帖人：{} \t 发帖时间：{} \t 回复数量：{} \n'.format(comment['title'],comment['link'],comment['name'],comment['time'],comment['replyNum']))
		print('当前页面爬取完成')

def main(start_url,deep):
	url_list = []
	# 将所有需要爬取的url存入列表
	for i in range(0,deep):
		url_list.append(start_url+str(50*i))
	print('所有网页已经下载本地，开始筛选信息。。。')

	# 循环写入数据
	for url in url_list:
		content = get_content(url)
		write_to_file(content)
	print('保存完毕！！')

start_url = 'http://tieba.baidu.com/f?kw=%E7%94%9F%E6%B4%BB%E5%A4%A7%E7%88%86%E7%82%B8&ie=utf-8&pn='
deep = 3

if __name__ == '__main__':
	main(start_url,deep)

