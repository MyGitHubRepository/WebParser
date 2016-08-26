""" Project: Web/Html Scraper, Coder: Hakan Etik, Date:15.08.2016 """

from bs4 import BeautifulSoup
import urllib2

class WebParser:
	def __init__(self, url, debug_mode, output_file_name):
		self.webPageHandle = 0
		self.soup = 0
		self.url = url
		self.debugMode = debug_mode
		self.outputFileName = output_file_name

	def urlOpen(self):
		self.webPageHandle = urllib2.urlopen(self.url)
		#self.dumpWebPageToConsole(self.webPageHandle)

	def initialiseSoup(self):
		htmlPage = self.webPageHandle.read()
		self.soup = BeautifulSoup(htmlPage,'html.parser')
		self.dumpWebPageToFile(self.outputFileName)

	def initialise(self):
		self.urlOpen()
		self.initialiseSoup()

	def getDebugMode(self):
		return self.debugMode
		
	def parseWebPageHead(self):
		return self.soup.find_all('head')
	
	def parseWebPageBody(self):
		return self.soup.find_all('body')

	def findTag(self, tag):
		return self.soup.find_all(tag)

	def findTagWithAttrs(self, tag, attrs={}):
		return self.soup.find_all(tag, attrs)

	def findTagWithAttrsAndLimit(self, tag, limit_number, attrs={}):
		return self.soup.find_all(tag, attrs, limit=limit_number)	
		
	def dumpWebPageToFile(self, file_name):
		if self.debugMode:
			html = self.soup.prettify("utf-8")
			target = open(file_name, 'w')
			target.truncate()
			target.write(html)
			target.close()		

	def dumpWebPageToConsole(self, web_page_handle):
		if self.debugMode:
			print 'RESPONSE:', web_page_handle
			print 'URL     :', web_page_handle.geturl()

			headers = web_page_handle.info()
			print 'DATE    :', headers['date']
			print 'HEADERS :'
			print '---------'
			print headers

			html = web_page_handle.read()
			print 'LENGTH  :', len(html)
			print 'DATA    :'
			print '---------'
			print html
	
def main():
	url = 'http://nightbot/buildslaves'
	parser = WebParser(url, False, "nightbot.txt")
	parser.initialise()
	if parser.getDebugMode:
		print "HEAD:"
		print parser.parseWebPageHead()
		print "-----------"
		print "BODY:"
		print parser.parseWebPageBody()
		
if __name__=='__main__':
	main()
