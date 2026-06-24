import sys, time, json, configparser
from token_updater import getLatestToken, getLatestTokenBrowser
from random import choice
from curl_cffi import requests
from login import initial_login

def proxy_formatter(proxy):
	proxy = proxy.split(':')
	proxy = f"{proxy[2]}:{proxy[3]}@{proxy[0]}:{proxy[1]}"
	return proxy

bet_id = sys.argv[1]

bet_id_1 = int(bet_id.split(',')[0])
bet_id_2 = int(bet_id.split(',')[1])

port_arg = sys.argv[2]
proxy_number = sys.argv[3]

bet_1_type = sys.argv[4]
bet_2_type = sys.argv[5]
amount_counter = 0

if 'true' in bet_1_type:
    bet_1_type = True
else:
    bet_1_type = False

if 'true' in bet_2_type:
    bet_2_type = True
else:
    bet_2_type = False


config = configparser.ConfigParser()
config.read('settings.ini')
proxy_option = config['PROXY OPTION']['proxy']
SESSION = config['USER_PROFILE']['session']

if proxy_option == 'true':
	proxy_duration = int(config['PROXY OPTION']['duration'])
	with open(f'proxies/proxy_{proxy_number}.txt', 'r') as f:
		temp_proxies_list = f.readlines()

	proxies_list = []
	# Formatting proxies
	for proxy in temp_proxies_list:
		if len(proxy) > 4:
			proxies_list.append(proxy_formatter(proxy.strip()))

	proxies = {
		"http": f"http://{proxies_list[0]}",
		"https": f"http://{proxies_list[0]}",
	}
else:
	proxies = {}


with open('file_com/initial_odd.txt', 'r') as b:
	initial_odd = float(b.readline())
released = False

headers = {
    'Host': 'betting.begmedia.com',
    # 'Content-Length': '275',
    #'Sec-Ch-Ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
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

json_data = {
    'bets': [
        {
            'amount': 0.1,
            'comboSelections': [],
            'betSelections': [
                {
                    'odds': 1.09,
                    'selectionIdentifier': {
                        'id': bet_id_1,
                        'isLive': bet_1_type,
                    },
                },
                {
                    'odds': 1.75,
                    'selectionIdentifier': {
                        'id': bet_id_2,
                        'isLive': bet_2_type,
                    },
                },
            ],
            'isFreebet': False,
        },
    ],
    'requestedAdditionalInformation': {
        'isBetInformationRequested': False,
        'isSelectionInformationRequested': False,
        'isTicketInformationRequested': False,
    },
}


def getCurrentOdd():
	# Getting current odd
	with open(f'file_com/latest_odd.txt', 'r') as f:
		with open(f'file_com/latest_odd_2.txt', 'r') as q:
			return f.readline(), q.readline()

def getAmount():
	# Gets updated amount
	# logic to increment/reset amount
	global amount_counter
	if amount_counter < 10:
		with open(f'file_com/latest_amount {port_arg}.txt', 'r') as f:
			ready = float(f.readline()) + 0.01
			ready = round(ready, 2)
			amount = str(ready)
		with open(f'file_com/latest_amount {port_arg}.txt', 'w') as f:
			f.write(amount)
		amount_counter += 1
	else:
		with open(f'file_com/initial_amount {port_arg}.txt', 'r') as f:
			initial_amount = f.readline()
		amount = initial_amount
		with open(f'file_com/latest_amount {port_arg}.txt', 'w') as f:
			f.write(amount)
		amount_counter = 0
	return amount


if SESSION == 'chrome':
	with open("file_com/latest_token.txt", "r") as f:
		headers["X-Client"] = f.readline()

elif SESSION == 'manual':
	# Getting x-client header or in other words logging in
	headers["X-Client"] = initial_login()

external_wait = False

while True:
	# MAIN LOOP
	if external_wait:
		if '8081' in port_arg:
			time.sleep(3.8)
		elif '8082' in port_arg:
			time.sleep(6.8)
		elif '8083' in port_arg:
			time.sleep(9.8)
		elif '8084' in port_arg:
			time.sleep(12.8)
		elif '8085' in port_arg:
			time.sleep(15.8)
		elif '8086' in port_arg:
			time.sleep(18.8)
		elif '8087' in port_arg:
			time.sleep(21.8)
		elif '8088' in port_arg:
			time.sleep(24.8)

		external_wait = False
	external_wait = True

	with open(f'file_com/running_status.txt', 'r') as f:
		status = f.readline()

	start_p = time.time() # Countdown to change proxies
	proxy_counter = 1
	if 'start' in status:
		if proxy_option == 'true' and len(proxies_list) > 1:
			end_p = time.time()

			# segment to check whether switch proxy or not
			if (int(end_p - start_p)) >= proxy_duration: 
				proxies = {
					"http": f"http://{proxies_list[proxy_counter]}",
					"https": f"http://{proxies_list[proxy_counter]}",
				}
				if proxy_counter == len(proxies_list):
					proxy_counter = 0
				else:
					proxy_counter += 1
				start_p = time.time()

		time.sleep(choice([1, 1.5, 1.7, 2, 2.2, 2.5]))
		amount = float(getAmount())
		amount = round(amount, 2)

		try:
			current_odd_1, current_odd_2 = getCurrentOdd()
			current_odd_1 = float(current_odd_1)
			current_odd_2 = float(current_odd_2)
		except:
			pass
		else:
			try:
				if SESSION == 'manual':
					headers["X-Client"] = getLatestToken(headers["X-Client"], proxies)
				elif SESSION == 'chrome':
					headers["X-Client"] = getLatestTokenBrowser('', proxies)
			except:
				headers["X-Client"] = "NULL/EMPTY"

			# Checking whether to exit or not
			with open(f'file_com/exit.txt', 'r') as f:
				if 'true' in f.readline():
					with open(f'file_com/close_state {port_arg}.txt', 'w') as q:
						q.write(port_arg)
					print("[+] Quiting Instance")
					exit() # Exiting program

			if current_odd_1 != 0.0 and current_odd_2 != 0.0 and "NULL/EMPTY" not in headers["X-Client"]:
				json_data['bets'][0]['amount'] = amount
				json_data['bets'][0]['betSelections'][0]['odds'] = current_odd_1
				json_data['bets'][0]['betSelections'][1]['odds'] = current_odd_2
				current_odd_combined = current_odd_1 * current_odd_2

				# first request
				try:
					response = requests.post('https://betting.begmedia.com/api/v5/bets', headers=headers, json=json_data, impersonate='chrome101', proxies=proxies)
					response = json.loads(response.text)
					time.sleep(int(response[0]['placementDelay'])) # Delay
					with open("first_logs.txt", "a") as f:
						f.write(str((response[0]['placementDelay'])))
				except:
					#time.sleep(3.3)
					pass
				else:
					try:
						# Taking odd from the first response and updating json_data for the second one
						#current_odd = float(response[0]['betSelections'][0]['odds'])
						#json_data['bets'][0]['betSelections'][0]['odds'] = current_odd
					 	# second request
						with open(f"file_com/ready {port_arg}.txt", "w") as f:
							f.write(f"Ready({amount})")

						start = time.time() # Countdown to end the following WHILE LOOP
						while True:
							with open('file_com/release.txt', 'r') as f:
								released_port = f.readline()
								if port_arg in released_port and current_odd_combined >= initial_odd:
									released = True
									with open('file_com/release.txt', 'w') as q:
										q.write('NULL')
									with open(f'file_com/ready {port_arg}.txt', 'w') as q:
										q.write('Not Ready')

		
									try:
										response = requests.post('https://betting.begmedia.com/api/v5/bets', headers=headers, json=json_data, impersonate='chrome101', proxies=proxies)
									except:
										pass
							
									'''with open("second_logs.txt", "a") as f:
										f.write(str(response.text))'''
									break

								if port_arg in released_port and current_odd_combined < initial_odd:
									released = True
									with open('file_com/release.txt', 'w') as q:
										q.write('NULL')
									with open(f'file_com/ready {port_arg}.txt', 'w') as q:
										q.write('Not Ready')
									with open('file_com/results.txt', 'w') as q:
										q.write('Odd was lower! Try again')
									break

							end = time.time()
							# discarding request and breaking loop if timeout
							if (int(end - start)) >= 3.3: 
								external_wait = False
								released = False
								with open('file_com/release.txt', 'w') as q:
									q.write('NULL')
								with open(f'file_com/ready {port_arg}.txt', 'w') as q:
									q.write('Not Ready')
								break

						if released == True:
							released = False
							# parsing response and displaying message
							if str(json.loads(response.text)[0]['betPlacedCount']) == "1":
								with open('file_com/results.txt', 'w') as q:
									q.write('Bet successful!')

							elif "Encrypted delay token obsolete, generating a new one" in response.text:
								with open('file_com/results.txt', 'w') as q:
									q.write('Token was expired! Try again')

							elif "La cote a changé. Vérifie la avant de valider de nouveau ton pari." in response.text or "La cote a changÃ©. VÃ©rifie la avant de valider de nouveau ton pari." in response.text:
								with open('file_com/results.txt', 'w') as q:
									q.write('Odd change popup occured! Try again')

							elif "suspendue" in response.text:
								with open('file_com/results.txt', 'w') as q:
									q.write('Bet was either suspended or terminated!')
									
							elif "Le solde de ton compte est insuffisant. Tu peux effectuer un dépôt" in response.text:
								with open('file_com/results.txt', 'w') as q:
									q.write('Low deposit!')
					except:
						pass