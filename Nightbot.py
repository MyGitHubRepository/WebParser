""" Project: Web/Html Scraper, Coder: Hakan Etik, Date:18.08.2016 """
from ConsoleMenuGenerator import *
from NightbotParser import *

#Global definitions
is_build_slave_list_generated = False
build_slave_list = []

def generateBuildSlaveList():
	global is_build_slave_list_generated
	global build_slave_list
	url = 'http://nightbot/buildslaves'
	
	if not is_build_slave_list_generated:
		nightbotParser = NightbotParser(url, False, "nightbotSlaves.txt")
		nightbotParser.initialise()
		build_slave_list = nightbotParser.getBuildSlaveList()
		is_build_slave_list_generated = True
	
	return build_slave_list

def generateBuildSlaveStateUrl(slave_name):
	url = 'http://nightbot/buildslaves/%s' % slave_name	
	return url	

def generateBuildUrl(slave_status_list):
	build_name = slave_status_list[0] #Builder name
	build_number = slave_status_list[1] #Build number
	build_no = build_number.replace("#", "")
	url = 'http://nightbot/builders/%s/builds/%s' % (build_name, build_no)

	return url
	
def generateBuildSlaveStatusList(slave_name):
	build_slave_status_list = []
	slave_url = generateBuildSlaveStateUrl(slave_name)
	dbg_output_file_name = "Nightbot-%s.txt" % slave_name
	nightbotParser = NightbotParser(slave_url, False, dbg_output_file_name)
	nightbotParser.initialise()
	build_slave_status_list = nightbotParser.getBuildSlaveStatusList()
	
	return build_slave_status_list	

def showBuildInformation(slave_status_list):
	build_url = generateBuildUrl(slave_status_list)
	
	dbg_output_file_name = "Nightbot-%s.txt" % slave_status_list[0] #Builder name
	nightbotParser = NightbotParser(build_url, False, dbg_output_file_name)
	nightbotParser.initialise()
	build_info_list = nightbotParser.getBuildInformation()

	#print build info dictionary
	for k, v in build_info_list.iteritems():
		print "   ",k ,v
	
def showBuildSlaves():
	the_list = generateBuildSlaveList()
	#Print out all build slave machines
	for build_slave in range(0, len(the_list)):
		print "Build Slave Name :", the_list[build_slave][0]

def showBuilders():
	the_list = generateBuildSlaveList()
	#Print out all build slave machines and builders
	for build_slave in range(0, len(the_list)):
		for builders in range(1, len(the_list[build_slave])):
			print "    Builders :", the_list[build_slave][builders]

def showBuildSlaveStatus(slave_name=None):
	is_slave_found = False
	
	if slave_name == None:
		the_list = generateBuildSlaveList()
		user_input = raw_input("enter build slave name>")
		slave_name = "%s" % user_input
		for build_slave in range(0, len(the_list)):
			#print "Build Slave Name-->", the_list[build_slave][0]
			if slave_name == the_list[build_slave][0]:
				is_slave_found = True
				break
	else:
		is_slave_found = True

	if is_slave_found:
		the_status_list = generateBuildSlaveStatusList(slave_name)
		#Print out all build slave machines and builders
		if len(the_status_list) > 0:
			for list_item in range(0, len(the_status_list)):
				print "Builder name:", the_status_list[list_item][0] #Builder name
				print "    Build number:", the_status_list[list_item][1] #Build number
				showBuildInformation(the_status_list[list_item])
		else:
			print "No current builds!!"
	else:
		raise ValueError('Build slave is not defined for nightbot!!')

def checkBuilderSlaveStatus():
	the_list = generateBuildSlaveList()
	user_input = raw_input("enter builder name>")
	builder_name = "%s" % user_input
	is_builder_found = False
	builder_slave_name = None
	for build_slave in range(0, len(the_list)):
		for builders in range(1, len(the_list[build_slave])):
			if builder_name == the_list[build_slave][builders]:
				is_builder_found = True
				builder_slave_name = the_list[build_slave][0]
				break

	if is_builder_found:
		print "Build Slave name: ", builder_slave_name
		showBuildSlaveStatus(builder_slave_name)
	else:
		raise ValueError('Builder slave is not found for nightbot!!')

		
def writeBuildSlavesToFile():
	name = raw_input("enter output file name>")
	file_name = "%s.txt" % name
	target = open(file_name, 'w')
	target.truncate()
	the_list = generateBuildSlaveList()
	for build_slave in range(0, len(the_list)):	
		target.write("%s\n" % the_list[build_slave][0])
	target.close()

def writeBuildersToFile():
	file_name = raw_input("enter output file name>")
	target = open('%s.txt' % file_name , 'w')
	target.truncate()
	the_list = generateBuildSlaveList()
	for build_slave in range(0, len(the_list)):
		for builders in range(1, len(the_list[build_slave])):
			target.write("%s\n" % the_list[build_slave][builders])
	target.close()

#Main
def main():
	main_menu = Menu("***Nightbot***")
	# automatically calls main.AddItem(item1)
	open = Item("Show build slaves", showBuildSlaves, main_menu)

	# automatically sets parent to main
	main_menu.add_item(Item("Show builders", showBuilders))
	main_menu.add_item(Item("Show build slave status", showBuildSlaveStatus))
	main_menu.add_item(Item("Check builder slave status", checkBuilderSlaveStatus))
	main_menu.add_item(Item("Write buildslaves to file", writeBuildSlavesToFile))
	main_menu.add_item(Item("Write builders to file", writeBuildersToFile))
	main_menu.add_item(Item("Exit", main_menu.terminate))

	main_menu.cls() # clear console before drawing

	while(True):
		try:
			main_menu.draw()
			n=input("choice>")
			main_menu.run(n-1)
		except Exception as e:
			print("Undefined option please select defined option")
			print e
			time.sleep(1) # delays for 1 seconds
			main_menu.cls()


if __name__=='__main__':
	main()