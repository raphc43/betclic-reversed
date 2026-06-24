import requests, json, time, configparser

config = configparser.ConfigParser()
config.read('settings.ini')
SESSION = config['USER_PROFILE']['session']

headers = {
	'authority': 'globalapi.begmedia.com',
	'accept': 'application/json, text/plain, */*',
	'accept-language': 'en-US,en;q=0.9',
	'origin': 'https://www.betclic.fr',
	'referer': 'https://www.betclic.fr/',
	'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
	'sec-ch-ua-mobile': '?0',
	'sec-ch-ua-platform': '"Windows"',
	'sec-fetch-dest': 'empty',
	'sec-fetch-mode': 'cors',
	'sec-fetch-site': 'cross-site',
	'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
	'x-client': '',
}

def getLatestToken(current_token='', proxies={}):			
	if SESSION == 'manual':
		headers['x-client'] = current_token
		while True:
			try:
				response = requests.get('https://globalapi.begmedia.com/api/Messages/CountNew', headers=headers, proxies=proxies)
			except:
				pass
			else:
				break
		token = json.loads(response.headers["x-client"])
		token = '{'+f'"auth":"{token["Auth"]}","context":"{token["Context"]}"'+'}'
		with open("file_com/latest_token.txt", "w") as f:
			f.write(token)
		return token
def getLatestTokenBrowser(current_token='', proxies={}):			
	if SESSION == 'chrome':
		with open("file_com/latest_token.txt", "r") as f:
			latest_token = f.readline()
		headers['x-client'] = latest_token
		while True:
			try:
				response = requests.get('https://globalapi.begmedia.com/api/Messages/CountNew', headers=headers, proxies=proxies)
			except:
				pass
			else:
				break
		token = json.loads(response.headers["x-client"])
		token = '{'+f'"auth":"{token["Auth"]}","context":"{token["Context"]}"'+'}'
		with open("file_com/latest_token.txt", "w") as f:
			f.write(token)
		return token
getLatestTokenBrowser()