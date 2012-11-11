import urllib2,re,threading
from Queue import Queue
from bs4 import BeautifulSoup
from urlparse import urlparse
from sets import Set

log=open("cr.log",'w')
seen=Set()
data=open("data",'a')



class Crawler(threading.Thread): 
	def __init__(self, queue,id):
		threading.Thread.__init__(self)
		self.queue,self.id = queue,id
	def run(self):
		while True:
			url = self.queue.get().lower()
			try:
				print self.id,":",self.queue.qsize(),
				child=extractlinks(url)
				seen.add(url)
				for c in child: 
					if c not in seen: self.queue.put(c)
			except Exception, e:
				print e
				seen.add(url)
			self.queue.task_done()


def extractlinks(url):
	if url.lower() in seen or not valid(url.lower()): return []
	print url
	html=urllib2.urlopen(url).read()
	soup = BeautifulSoup(html)
	anchors = soup.findAll('a')
	links = []
	for a in anchors:
		if not valid(a.get('href')): continue
		url2=str(a.get('href')).lower()
		if url2[-1]=='/': url2=url2[:-1]
		if url2[-3:]==':80': url2=url2[:-3]
		links.append(url2)
		data.write(url2 +'\t'+str(url)+'\n')
		log.write(str(a.get('href')))
		log.write('\n')
	return links
def valid(url):
	if url==None or urlparse(url)==None  or urlparse(url)[1]=='':return False
	if url[:9]=='javascript': return False
	if urlparse(url)[1].find("nju.edu.cn")<0:return False
	if urlparse(url)[1] in ["go.nju.edu.cn","hwxy.nju.edu.cn","jcxy.nju.edu.cn","geoinformatics.nju.edu.cn","csbbs.nju.edu.cn"]:return False
	if url[-4:] in ['.doc','.avi','.xls','.pdf','.jpg','.gif','.flv','.rar','.zip']:return False
	if url.find("portal.nju.edu.cn/portal/media-type/html/group/xxgk/page/default.psml/js_pane")>=0:return False
	if url.find("chin.nju.edu.cn/smf")>=0:return False
	if url.find("nubs.nju.edu.cn/faculty.php/d")>=0:return False
	if url.find("law.nju.edu.cn/comment.asp")>=0:return False
	if url.find("moon.nju.edu.cn/courses/calendar")>=0:return False
	if url.find("nubs.nju.edu.cn/faculty.php/c")>=0:return False
	if url.find("nubs.nju.edu.cn/faculty.php/e")>=0:return False
	return True

def bfs(start):
	q=Queue()
	for s in start: q.put(s)
	while(not q.empty()):
		url=q.get().lower()
		try:
			child=extractlinks(url)#fetch(url)
			seen.add(url)
			for c in child: 
				if c not in seen: q.put(c)
		except Exception, e:
			print e
			seen.add(url)

	

def multithread(start):
	q=Queue()
	for s in start: q.put(s)
	for i in range(15):
		t = Crawler(q,i)
		#t.setDaemon(True)
		t.start()
	q.join()
def main():
	##bfs(["http://www.nju.edu.cn","http://cs.nju.edu.cn"])
	multithread(["http://www.nju.edu.cn","http://cs.nju.edu.cn"])




main()

