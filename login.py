import requests
#from curl_cffi import requests
from bs4 import BeautifulSoup
import json, uuid, time, configparser


def initial_login():

	# Config variables
	config = configparser.ConfigParser()
	config.read('settings.ini')

	username = config['USER_PROFILE']['username']
	password = config['USER_PROFILE']['password']
	birthdate = config['USER_PROFILE']['birthdate']

	headers = {
	    'Host': 'www.betclic.fr',
	    'Cache-Control': 'max-age=0',
	    'Sec-Ch-Ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
	    'Sec-Ch-Ua-Mobile': '?0',
	    'Sec-Ch-Ua-Platform': '"Windows"',
	    'Upgrade-Insecure-Requests': '1',
	    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
	    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
	    'Sec-Fetch-Site': 'same-origin',
	    'Sec-Fetch-Mode': 'navigate',
	    'Sec-Fetch-User': '?1',
	    'Sec-Fetch-Dest': 'document',
	    # 'Accept-Encoding': 'gzip, deflate',
	    'Accept-Language': 'en-US,en;q=0.9',
	    'If-None-Match': 'W/"97f3f-5nVhAy5s9nUfv5+LK3XTNuSCH+E"',
	}


	headers_for_login = {
	    'Host': 'apif.begmedia.com',
	    # 'Content-Length': '182',
	    'Sec-Ch-Ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
	    'Accept': 'application/json, text/plain, */*',
	    'Content-Type': 'application/json',
	    'X-Client': '',
	    'Sec-Ch-Ua-Mobile': '?0',
	    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
	    'Sec-Ch-Ua-Platform': '"Windows"',
	    'Origin': 'https://www.betclic.fr',
	    'Sec-Fetch-Site': 'cross-site',
	    'Sec-Fetch-Mode': 'cors',
	    'Sec-Fetch-Dest': 'empty',
	    'Referer': 'https://www.betclic.fr/',
	    # 'Accept-Encoding': 'gzip, deflate',
	    'Accept-Language': 'en-US,en;q=0.9',
	}

	# sending requests
	while True:
		try:
			response = requests.get('https://www.betclic.fr/', headers=headers)
		except:
			pass 
		else:
			break

	page = BeautifulSoup(response.text, 'lxml')
	page = page.find('script', {'id':'ng-state'}).text
	page_dict = json.loads(page)

	context = page_dict['app-context']['xClient']['Context']
	auth = page_dict['app-context']['xClient']['Auth']
	headers_for_login['X-Client'] = '{"auth":"'+auth+'","context":"'+context+'"}'

	random_uuid = str(uuid.uuid4())


	# SECOND REQUEST
	json_data = {
	    'login': username,
	    'password': password,
	    'fingerprint': random_uuid,
	    'client_info': {
	        'application': 'BETCLIC.FR',
	        'universe': 'sport',
	        'channel': 'WEB_BETCLIC.FR',
	    },
	}

	while True:
		try:
			response = requests.post('https://apif.begmedia.com/api/v1/account/auth/logins', headers=headers_for_login, json=json_data)		
			with open('session_id.txt', 'w') as f:
				f.write(json.loads(response.text)['id'])
		except:
			pass 
		else:
			break


	json_data = [
	    {
	        'digestId': json.loads(response.text)['digests'][0]['id'],
	        'parameters': {
	            'birthdate': birthdate,
	        },
	    },
	]


	time.sleep(1)
	while True:
		try:
			response = requests.post(
				"https://apif.begmedia.com/api/v1/account/auth/logins/"+json.loads(response.text)['id']+"/digests",
				#"https://apif.begmedia.com/api/v1/account/auth/logins/f885859b-010b-46d5-889b-bee582250620/digests",
				headers=headers_for_login,
				json=json_data,
			)	
		except:
			pass 
		else:
			break


	auth = json.loads(response.text)['token']['auth']
	context = json.loads(response.text)['token']['context']
	x_client = '{"auth":"'+auth+'","context":"'+context+'"}'
	return x_client

def login():
	with open('session_id.txt', 'r') as f:
		session_id = f.read()
	# Config variables
	config = configparser.ConfigParser()
	config.read('settings.ini')

	username = config['USER_PROFILE']['username']
	password = config['USER_PROFILE']['password']
	birthdate = config['USER_PROFILE']['birthdate']

	headers = {
	    'Host': 'www.betclic.fr',
	    'Cache-Control': 'max-age=0',
	    'Sec-Ch-Ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
	    'Sec-Ch-Ua-Mobile': '?0',
	    'Sec-Ch-Ua-Platform': '"Windows"',
	    'Upgrade-Insecure-Requests': '1',
	    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
	    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
	    'Sec-Fetch-Site': 'same-origin',
	    'Sec-Fetch-Mode': 'navigate',
	    'Sec-Fetch-User': '?1',
	    'Sec-Fetch-Dest': 'document',
	    # 'Accept-Encoding': 'gzip, deflate',
	    'Accept-Language': 'en-US,en;q=0.9',
	    'If-None-Match': 'W/"97f3f-5nVhAy5s9nUfv5+LK3XTNuSCH+E"',
	}


	headers_for_login = {
	    'Host': 'apif.begmedia.com',
	    # 'Content-Length': '182',
	    'Sec-Ch-Ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
	    'Accept': 'application/json, text/plain, */*',
	    'Content-Type': 'application/json',
	    'X-Client': '',
	    'Sec-Ch-Ua-Mobile': '?0',
	    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
	    'Sec-Ch-Ua-Platform': '"Windows"',
	    'Origin': 'https://www.betclic.fr',
	    'Sec-Fetch-Site': 'cross-site',
	    'Sec-Fetch-Mode': 'cors',
	    'Sec-Fetch-Dest': 'empty',
	    'Referer': 'https://www.betclic.fr/',
	    # 'Accept-Encoding': 'gzip, deflate',
	    'Accept-Language': 'en-US,en;q=0.9',
	}

	# sending requests
	while True:
		try:
			response = requests.get('https://www.betclic.fr/', headers=headers)
		except:
			pass 
		else:
			break

	page = BeautifulSoup(response.text, 'lxml')
	page = page.find('script', {'id':'ng-state'}).text
	page_dict = json.loads(page)

	context = page_dict['app-context']['xClient']['Context']
	auth = page_dict['app-context']['xClient']['Auth']
	headers_for_login['X-Client'] = '{"auth":"'+auth+'","context":"'+context+'"}'

	random_uuid = str(uuid.uuid4())


	# SECOND REQUEST
	json_data = {
	    'login': username,
	    'password': password,
	    'fingerprint': random_uuid,
	    'client_info': {
	        'application': 'BETCLIC.FR',
	        'universe': 'sport',
	        'channel': 'WEB_BETCLIC.FR',
	    },
	}

	while True:
		try:
			response = requests.post('https://apif.begmedia.com/api/v1/account/auth/logins', headers=headers_for_login, json=json_data)		
		except:
			pass 
		else:
			break


	json_data = [
	    {
	        'digestId': json.loads(response.text)['digests'][0]['id'],
	        'parameters': {
	            'birthdate': birthdate,
	        },
	    },
	]


	time.sleep(1)
	while True:
		try:
			response = requests.post(
				"https://apif.begmedia.com/api/v1/account/auth/logins/"+session_id+"/digests",
				#"https://apif.begmedia.com/api/v1/account/auth/logins/f885859b-010b-46d5-889b-bee582250620/digests",
				headers=headers_for_login,
				json=json_data,
			)	
		except:
			pass 
		else:
			break


	auth = json.loads(response.text)['token']['auth']
	context = json.loads(response.text)['token']['context']
	x_client = '{"auth":"'+auth+'","context":"'+context+'"}'
	return x_client