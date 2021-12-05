import sqlite3
import os
import hashlib
import datetime
try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser  # ver. < 3.0

config = ConfigParser()

name_base = "block.db"
conn = sqlite3.connect(name_base, check_same_thread = False) # Подключение к БД
cursor = conn.cursor()

settings = {
	'is_ready': False
}

blockinfo = {
	'title': 'Empty',
	'timestamp': '04.12.2021 00:00',
	'type': 'Empty',
	'adr_from': 'Empty',
	'adr_to': 'Empty',
	'cost': 0.0,
	'fee': 0.0,
	'message': 'Empty',
	'prev_hash': 'Empty'
}

def CreateDatabase():
	# Создание таблицы
	try:
		cursor.execute("""
				CREATE TABLE blockchain
				(nblock INTEGER PRIMARY KEY AUTOINCREMENT, title text, timestamp text, type text, 
				adr_from text, adr_to text, cost real, fee real, message text, prev_hash text)
			""") 
	except sqlite3.DatabaseError as err:
				print('Error: ', err)
	# Генезис блок
	try:
		 cursor.execute("""
				INSERT INTO blockchain
				VALUES (null, 'Genesis', '04.12.2021 00:00', 'genesis', '0', '0', 0.0, 0.0, 'Genesis block', 'genesis')
			""")
	except sqlite3.DatabaseError as err:
				print('Error: ', err)
	conn.commit()
	return print("Database created successfully!")

def UpdateSettings(sInfo):
	config.set('settings', 'is_ready', sInfo['is_ready'])
	# save to a file
	with open('settings.ini', 'w') as configfile:
	    config.write(configfile)

def LoadAllConfigs():
	config.read('settings.ini')
	settings['is_ready'] = config.getboolean('settings', 'is_ready')

def get_hash(bInfo):
	f = open('block.txt', 'w')
	f.write('title : ' + str(bInfo['title']) + '\n')
	f.write('timestamp : ' + str(bInfo['timestamp']) + '\n')
	f.write('type : ' + str(bInfo['type']) + '\n')
	f.write('adr_from : ' + str(bInfo['adr_from']) + '\n')
	f.write('adr_to : ' + str(bInfo['adr_to']) + '\n')
	f.write('cost : ' + str(bInfo['cost']) + '\n')
	f.write('fee : ' + str(bInfo['fee']) + '\n')
	f.write('message : ' + str(bInfo['message']) + '\n')
	f.write('prev_hash :' + str(bInfo['prev_hash']) + '\n')
	f.close()
	file = open('block.txt', 'rb').read()
	h = hashlib.md5(file).hexdigest()
	path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'block.txt')
	os.remove(path)
	return h

def writeblock(bInfo):
	try:
		cursor.execute("""
	 			SELECT MAX(nblock) FROM blockchain
	 		""")
		nblock = cursor.fetchone()[0]
	except sqlite3.DatabaseError as err:
		print('Error: ', err)

	try:
		cursor.execute("""
				SELECT * FROM blockchain WHERE nblock = ?
			""", [nblock])
		prev_b = cursor.fetchone()
	except sqlite3.DatabaseError as err:
		print('Error: ', err)
	prev_binfo = TransformToDict(prev_b)
	bInfo['prev_hash'] = get_hash(prev_binfo)
	cursor.execute("""
		INSERT INTO blockchain
		VALUES (null, ?, ?, ?, ?, ?, ?, ?, ?, ?)
	""", (bInfo['title'], 
		bInfo['timestamp'], 
		bInfo['type'],
		bInfo['adr_from'],
		bInfo['adr_to'], 
		bInfo['cost'], 
		bInfo['fee'], 
		bInfo['message'],
		bInfo['prev_hash']))
	conn.commit()
	prev_block = int(prev_binfo['nblock'])+1
	return print("Block " , str(prev_block) , "successfully created!")

def TestingBlockchain():
	try:
		cursor.execute("""
		 		SELECT MAX(nblock) FROM blockchain
		 	""")
		nblock = cursor.fetchone()[0]
	except sqlite3.DatabaseError as err:
		print('Error: ', err)
	for i in range(1, nblock):
		try:
			cursor.execute("""
				SELECT * FROM blockchain WHERE nblock = ?
			""", [i])
			prev_b = cursor.fetchone()
		except sqlite3.DatabaseError as err:
			print('Error: ', err)

		prev_binfo = TransformToDict(prev_b)
		try:
			cursor.execute("""
				SELECT * FROM blockchain WHERE nblock = ?
			""", [i+1])
			b = cursor.fetchone()
		except sqlite3.DatabaseError as err:
			print('Error: ', err)
		if b[9] == get_hash(prev_binfo):
			print('Block ', str( b[0]-1 ) , " is good")
		else:
			print('Block ', str( b[0]-1 ) , " is bad")


# TODO написать функцию для преобразования ответа базы в словарь для облегчения
def TransformToDict(block):
	prevblock = {'nblock': block[0],
				  'title': block[1],
				  'timestamp': block[2],
				  'type': block[3],
				  'adr_from': block[4],
				  'adr_to': block[5],
				  'cost': block[6],
				  'fee': block[7],
				  'message': block[8],
				  'prev_hash': block[9]}
	return prevblock 

def IsAccountCreated(login, password):
	try:
		account = cursor.execute("""
			SELECT * FROM accounts WHERE login = ?
			""", (str(login),)).fetchone()
	except sqlite3.DatabaseError as err:
		print('Error: ', err)
	else:			
		if account is None:
			return 0
		else:
			if str(account[2]) != str(password):
				return 1
			else:
				return 2