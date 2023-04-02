import re, json, os, sys, time

port_arg = sys.argv[2] # represents port entered

first_request_completed = False
ready = False
print(first_request_completed)
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
						with open(f'file_com/release.txt', 'r') as f:
							if f.readline() == port_arg:
								first_request_completed = False
								ready = False
								with open(f'file_com/release.txt', 'w') as f:
									f.write('NULL')
								with open(f'file_com/latest.txt', 'w') as f:
									f.write('NULL')
								return

					end = time.time()

					# discarding request and breaking loop if timeout
					if (int(end - start)) >= 7: 
						flow.kill()#flow.request.reply(KILL) # Killing request
						first_request_completed = False
						ready = False
						with open(f'file_com/ready {port_arg}.txt', 'w') as f:
							f.write('Not Ready')
						return 
			except:
				raise

	if "https://betting.begmedia.com/api/v5/bets" in flow.request.url and 'selectionIdentifier' in flow.request.content.decode('utf-8'):
		if flow.request.method == "POST":
			first_request_completed = True
			return

def response(flow):
	pass