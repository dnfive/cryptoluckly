from settings import *

def main():
	LoadAllConfigs()
	if settings['is_ready'] == False:
		CreateDatabase()
		settings['is_ready'] = 'true'
		UpdateSettings(settings)
	# datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
	#blockinfo['title'] = "Test Block"
	#blockinfo['timestamp'] = str(datetime.datetime.now().strftime("%d-%m-%Y %H:%M"))
	#blockinfo['type'] = "transfer"
	#blockinfo['adr_from'] = "my_address"
	#blockinfo['adr_to'] = "my_address"
	#blockinfo['cost'] = 0.0
	#blockinfo['fee'] = 0.0
	#blockinfo['message'] = 'First block'
	#writeblock(blockinfo)
	#TestingBlockchain()


if __name__ == "__main__":
	main()