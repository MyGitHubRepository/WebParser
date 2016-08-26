""" Project: Web/Html Scraper, Coder: Hakan Etik, Date:17.08.2016 """

from WebParser import *
import re

class NightbotParser:
	def __init__(self, url, debug_mode, output_file_name):
		self.url = url
		self.debugMode = debug_mode
		self.outputFileName = output_file_name
		self. webParser = None
		
	def initialise(self):
		#initialise WebParser class
		self. webParser = WebParser(self.url, self.debugMode, self.outputFileName)
		self. webParser.initialise()

	def with_builders(self, href):
		return href and re.compile("builders").search(href)

	def with_builds(self, href):
		return href and re.compile("builds").search(href)

	def without_builds(self, href):
		return href and not re.compile("builds").search(href)
		
	def createBuildSlaveListItem(self, tag):
	  multi_dim_list = []

	  #Create list as Build slave name and Build slave builders
	  multi_dim_list.append(tag.b.a.string) #append build slave name
	  #print "tag a name : ", build_slave_tag.b.a.string
	  
	  tags_a = tag.find_all(href=self.with_builders)
	  for tag_a in tags_a:
		#print "tag a name-> : ", tag_a.string
		multi_dim_list.append(tag_a.string)#append build builder name

	  return multi_dim_list
	
	def getBuildSlaveList(self):
		tag = 'tr'
		attrs= {'class': ['alt', '']}
		build_slave_tags = self.webParser.findTagWithAttrs(tag, attrs)
		
		build_slave_list = []
		for build_slave_tag in build_slave_tags:
			build_slave_list.append(self.createBuildSlaveListItem(build_slave_tag))
		
		return build_slave_list

	def createBuildSlaveStatusListItem(self, tag):
		multi_dim_list = []
		#Create list as Builder name and Build number
		tags_a_builder_name = tag.find_all(href=self.without_builds)
		tags_a_build_number = tag.find_all(href=self.with_builds)
		
		for builder_name, build_number in zip(tags_a_builder_name, tags_a_build_number):
			multi_dim_list.append(builder_name.string) #append builder name
			multi_dim_list.append(build_number.string)#append build number
			#print "Builder name : ", builder_name.string
			#print "Build number : ", build_number.string
	
		return multi_dim_list

	def getBuildSlaveStatusList(self):
		tag = 'li'
		build_slave_status_tags = self.webParser.findTag(tag)		
		
		build_slave_status_list = []
		for build_slave_status_tag in build_slave_status_tags:
			build_slave_status_list.append(self.createBuildSlaveStatusListItem(build_slave_status_tag))
		
		return build_slave_status_list
	
	def getBuildInformation(self):
		build_info_list = {'Build In progress:' : 'Completed',
							'Result:' : 'Not completed',
							'Revision:' : 'Not idendified',
							'Reason:' : 'Not determined'}
		tag = 'div'
		attrs= {'class': 'column'}
		build_info_result = self.webParser.findTagWithAttrsAndLimit(tag, 1, attrs)

		#Get build in progress info
		string_to_search = "Build In Progress:"
		build_tag = build_info_result[0].find_all('h2', string=string_to_search)
		if len(build_tag[0].next_sibling.string.strip()) is not 0:
			build_info_list['Build In progress:'] = build_tag[0].next_sibling.string.strip()
		else:
			build_info_list['Build In progress:'] = build_tag[0].next_sibling.next_sibling.string.strip()

		#Get build result
		string_to_search = "Results"
		build_tag = build_info_result[0].find_all('h2', string=string_to_search)
		if len(build_tag) is not 0:
			build_info_list['Result:'] = build_tag[0].next_sibling.string

		#Get build svn revision 
		string_to_search = "Got Revision"
		build_tag = build_info_result[0].find_all('td', string=string_to_search)
		if len(build_tag) is not 0:
			build_info_list['Revision:'] = build_tag[0].next_sibling.string

		#Get build reason 
		build_tag = build_info_result[0].find_all('p', text=re.compile("'"))
		build_reason_string = build_tag[0].string.strip()
		build_reason_string = build_reason_string[:build_reason_string.rfind("'")]
		build_reason_string = build_reason_string[build_reason_string.rfind("'"):]
		build_info_list['Reason:'] = build_reason_string

		return build_info_list
		
def main():
	url = 'http://nightbot/buildslaves'
	nightbotParser = NightbotParser(url, False, "nightbotSlaves.txt")
	nightbotParser.initialise()
	build_slave_list = nightbotParser.getBuildSlaveList()
	
	#Print out all build slave machines and builders
	for build_slave in range(0, len(build_slave_list)):
		print "Build Slave Name-->", build_slave_list[build_slave][0]
		for builders in range(0, len(build_slave_list[build_slave])):
			print "    Builders-->", build_slave_list[build_slave][builders]
			
if __name__=='__main__':
	main()