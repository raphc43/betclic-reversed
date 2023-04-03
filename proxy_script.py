import re, json, os, sys, time

port_arg = sys.argv[2] # represents port entered

first_request_completed = False
ready = False
released = False
print(first_request_completed)
from mitmproxy import ctx
view = ctx.master.addons.get("view")
def request(flow):
	global first_request_completed, ready
	if "https://betting.begmedia.com/api/v5/bets" in flow.request.url and 'selectionIdentifier' in flow.request.content.decode('utf-8'):
		if first_request_completed == True and flow.request.method == "POST":
			start = time.time() # Countdown to end WHILE LOOP
			with open(f'file_com/latest.txt', 'w') as f:
				f.write(port_arg)
			try:
				while True:
					if ready == False:
						with open(f'file_com/ready {port_arg}.txt', 'w') as f:
							f.write('Ready')
							ready = True

					if ready == True:
						with open('file_com/release.txt', 'r') as f:
							released_port = f.readline()
							with open('file_com/initial_odd.txt', 'r') as b:
								initial_odd = float(b.readline())
								request_data = json.loads(flow.request.content.decode("utf-8"))
								current_odd = float(request_data['bets'][0]["betSelections"][0]["odds"])
								if port_arg in released_port and current_odd >= initial_odd:
									first_request_completed = False
									ready = False
									released = True
									with open('file_com/release.txt', 'w') as q:
										q.write('NULL')
									with open('file_com/latest.txt', 'w') as q:
										q.write('NULL')
									with open(f'file_com/ready {port_arg}.txt', 'w') as q:
										q.write('Not Ready')
									return flow
								if port_arg in released_port and current_odd < initial_odd:
									first_request_completed = False
									ready = False
									with open('file_com/release.txt', 'w') as q:
										q.write('NULL')
									with open('file_com/latest.txt', 'w') as q:
										q.write('NULL')
									with open(f'file_com/ready {port_arg}.txt', 'w') as q:
										q.write('Not Ready')
									with open('file_com/results.txt', 'w') as q:
										q.write('Odd was lower! Try again')
									flow.kill() # Killing request
									return flow

					end = time.time()

					# discarding request and breaking loop if timeout
					if (int(end - start)) >= 9: 
						with open('file_com/release.txt', 'w') as q:
							q.write('NULL')
						with open('file_com/latest.txt', 'w') as q:
							q.write('NULL')
						with open(f'file_com/ready {port_arg}.txt', 'w') as q:
							q.write('Not Ready')
						flow.kill() # Killing request
						first_request_completed = False
						ready = False

						return 
			except:
				pass

	if "https://betting.begmedia.com/api/v5/bets" in flow.request.url and 'selectionIdentifier' in flow.request.content.decode('utf-8'):
		if first_request_completed == False and flow.request.method == "POST":
			first_request_completed = True
			return

def response(flow):
	try:
		if released == True and 'placement' in flow.response.text:
			released = False
			response_data = json.loads(flow.response.content.decode("utf-8"))
			f.write()
			try:
				error1 = response_data[0]["betError"]["technicalMessage"]
			except:
				error1 = "NULL"
			error2 = response_data[0]["betError"]["userMessage"]
			if "Encrypted delay token obsolete, generating a new one" in error1:
				with open('file_com/special_reload.txt', 'w') as q:
					q.write(port_arg)
				with open('file_com/results.txt', 'w') as q:
					q.write('Token was expired! Try again')
				flow.kill()
			elif "La cote a changé. Vérifie la avant de valider de nouveau ton pari." in error2:
				with open('file_com/special_reload.txt', 'w') as q:
					q.write(port_arg)
				with open('file_com/results.txt', 'w') as q:
					q.write('Odd was lower! Try again')
				flow.kill()
	except:
		pass

	if view.store_count() >= 40:
		view.clear()