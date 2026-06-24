# dialog.py

"""Dialog-style application."""

import sys, subprocess, time, browser_cookie3, configparser
from login import initial_login
from urllib.parse import unquote
from PyQt6 import QtCore
from PyQt6.QtWidgets import (
	QApplication,
	QDialog,
	QDialogButtonBox,
	QFormLayout,
	QLineEdit,
	QVBoxLayout,
	QPushButton,
	QWidget,
	QLabel,
	QGridLayout,
)


match_id, selection_ids, amount, initial_odd, instances, bet_combo = sys.argv[1], sys.argv[2], float(sys.argv[3]), sys.argv[4], sys.argv[5], sys.argv[6]
print(bet_combo)

# Logic to add true/false based bet combination type
if bet_combo == 'live+live':
	bet_1_type = 'true'
	bet_2_type = 'true'
else:
	bet_1_type = 'true'
	bet_2_type = 'false'

config = configparser.ConfigParser()

# Config variables
config.read('settings.ini')

SESSION = config['USER_PROFILE']['session']
if SESSION == 'chrome':
	CHROME_PROFILE = config['BROWSER_SETTINGS']['chrome_profile']

	cookies = browser_cookie3.chrome(cookie_file=CHROME_PROFILE+'/Network/Cookies', domain_name='.betclic.fr')
	cookie_data = {}
	for c in cookies:
		c = str(c).split(' ')
		c = c[1].split('=')
		cookie_data[c[0]] = c[1]

	token_decoded = unquote(cookie_data["BC-TOKEN"])
	with open("file_com/latest_token.txt", "w") as f:
		f.write(token_decoded)

elif SESSION == 'manual':
	x_token = initial_login()
	with open("file_com/latest_token.txt", "w") as f:
		f.write(x_token)


for i in range(1, 9):
	with open(f"file_com/ready 808{i}.txt", "w") as f:
		f.write('Not Ready')

with open(f'file_com/latest_odd.txt', 'w') as f:
	f.write('0')

with open(f'file_com/latest_odd_2.txt', 'w') as f:
	f.write('0')

with open(f"file_com/release.txt", "w") as f:
	f.write('NULL')

with open(f"file_com/latest.txt", "w") as f:
	f.write('NULL')

with open(f'file_com/exit.txt', 'w') as q:
	q.write('false')

with open('file_com/results.txt', 'w') as q:
	q.write('None')

with open('file_com/initial_odd.txt', 'w') as b:
	b.write(initial_odd)

with open('file_com/special_reload.txt', 'w') as f:
	f.write('NULL')

with open(f'file_com/running_status.txt', 'w') as f:
	f.write('start')

with open(f'file_com/odd_status.txt', 'w') as f:
	f.write('NULL')

with open(f'file_com/odd_status_2.txt', 'w') as f:
	f.write('NULL')

if ',' in match_id:
	match_id_1 = match_id.split(',')[0]
	match_id_2 = match_id.split(',')[1]

	selection_ids_1 = selection_ids.split(',')[0]
	selection_ids_2 = selection_ids.split(',')[1]

	subprocess.Popen(['python.exe', "odd_updater.py", match_id_1, selection_ids_1, 'latest_odd.txt', bet_1_type, 'odd_status.txt'])
	subprocess.Popen(['python.exe', "odd_updater.py", match_id_2, selection_ids_2, 'latest_odd_2.txt', bet_2_type, 'odd_status_2.txt'])
else:
	subprocess.Popen(['python.exe', "odd_updater.py", match_id, selection_ids, 'latest_odd.txt', 'true', 'odd_status.txt'])

#subprocess.Popen(['python.exe', "token_updater.py"])

for i in range(1, int(instances)+1):
	with open(f"file_com/close_state 808{i}.txt", "w") as f:
		f.write("")

	with open(f'file_com/initial_amount 808{i}.txt', 'w') as f:
		if i != 1:
			amount += 0.20
		f.write(str(amount))
	with open(f"file_com/latest_amount 808{i}.txt", "w") as f:
		f.write(str(amount))
	time.sleep(4.5)
	if ',' in match_id:
		subprocess.Popen(['python.exe', "main_instance_combined.py", selection_ids, f"808{i}", str(i), bet_1_type, bet_2_type])
	else:
		subprocess.Popen(['python.exe', "main_instance.py", selection_ids, f"808{i}", str(i)])



ready = 'Not Ready'
status = 'Running'


def updateOddsDisplay():
	with open("file_com/latest_odd.txt", "r") as f:
		odd_1 = f.readline()
	with open("file_com/odd_status.txt", "r") as f:
		odd_status_1 = f.readline()
		if "1" in odd_status_1:
			odd_status_1 = 'active'
		elif "2" in odd_status_1:
			odd_status_1 = 'suspended'
		elif "3" in odd_status_1:
			odd_status_1 = 'unavailable'
		else:
			odd_status_1 = 'unknown'

	with open("file_com/latest_odd_2.txt", "r") as f:
		odd_2 = f.readline()
	with open("file_com/odd_status_2.txt", "r") as f:
		odd_status_2 = f.readline()
		if "1" in odd_status_2:
			odd_status_2 = 'active'
		elif "2" in odd_status_2:
			odd_status_2 = 'suspended'
		elif "3" in odd_status_2:
			odd_status_2 = 'unavailable'
		else:
			odd_status_2 = 'unknown'

	text = f"{odd_1} - {odd_status_1}"
	bet_1_odd_label.setText(text)

	text = f"{odd_2} - {odd_status_2}"
	bet_2_odd_label.setText(text)

	if ',' in match_id:
		try:
			odd_1 = float(odd_1.strip().replace(',', '.'))
			odd_2 = float(odd_2.strip().replace(',', '.'))
			my_float = odd_1 * odd_2
			formatted_float = "{:.2f}".format(my_float)
			text = f"Combined odd: {formatted_float}"
		except:
			text = f"Combined odd: NULL"
		combined_odd_display.setText(text)
		layout.addWidget(combined_odd_display, 9, 0)

	layout.addWidget(bet_1_odd_label, 7, 0)
	layout.addWidget(bet_2_odd_label, 8, 0)

def extractReady():
	with open("file_com/ready 8081.txt", "r") as f:
		ready_8081 = f.readline()
	with open("file_com/ready 8082.txt", "r") as f:
		ready_8082 = f.readline()
	with open("file_com/ready 8083.txt", "r") as f:
		ready_8083 = f.readline()
	with open("file_com/ready 8084.txt", "r") as f:
		ready_8084 = f.readline()
	with open("file_com/ready 8085.txt", "r") as f:
		ready_8085 = f.readline()
	with open("file_com/ready 8086.txt", "r") as f:
		ready_8086 = f.readline()
	with open("file_com/ready 8087.txt", "r") as f:
		ready_8087 = f.readline()
	with open("file_com/ready 8088.txt", "r") as f:
		ready_8088 = f.readline()


	return ready_8081, ready_8082, ready_8083, ready_8084, ready_8085, ready_8086, ready_8087, ready_8088

def updateReady():
	ready_8081, ready_8082, ready_8083, ready_8084, ready_8085, ready_8086, ready_8087, ready_8088 = extractReady()

	label_1.setText(ready_8081)
	layout.addWidget(label_1, 0, 0)

	label_2.setText(ready_8082)
	layout.addWidget(label_2, 0, 1)

	label_3.setText(ready_8083)
	layout.addWidget(label_3, 0, 2)

	label_4.setText(ready_8084)
	layout.addWidget(label_4, 1, 0)

	label_5.setText(ready_8085)
	layout.addWidget(label_5, 1, 1)

	label_6.setText(ready_8086)
	layout.addWidget(label_6, 1, 2)

	label_7.setText(ready_8087)
	layout.addWidget(label_7, 2, 0)

	label_8.setText(ready_8088)
	layout.addWidget(label_8, 2, 1)

def release():
	for i in range(1, int(instances)+1):
		with open(f"file_com/ready 808{i}.txt", "r") as f:
			ready = f.readline()
			if ready != "Not Ready":
				with open("file_com/release.txt", "w") as q:
					q.write(f"808{i}")
				return
	with open("file_com/results.txt", "w") as q:
		q.write("You pressed at the wrong time!")
	return


def updateResult():
	counter = 0
	if "Wait" in results.text():
		for i in range(1, int(instances)+1):
			with open(f"file_com/close_state 808{i}.txt", "r") as q:
				if "808" in q.readline():
					counter += 1
		if counter == int(instances):
			results.setText("Successfully Closed!")
			layout.addWidget(results, 3, 1)
	elif "Successfully Closed!" not in results.text():
		with open(f"file_com/results.txt", "r") as f:
			results.setText(f.readline())
			layout.addWidget(results, 3, 1)


def resetResult():
	with open(f"file_com/results.txt", "w") as f:
		f.write("None")

def closeInstances():
	with open(f"file_com/exit.txt", "w") as f:
		f.write("true")
	time.sleep(1)
	with open(f"file_com/results.txt", "w") as f:
		f.write("Wait - Closing...")

def changeAmount():
	float_amount = float(change_amount.text())
	for i in range(1, int(instances)+1):
		with open(f'file_com/initial_amount 808{i}.txt', 'w') as f:
			if i != 1:
				float_amount += 0.20
			f.write(str(float_amount))

		with open(f"file_com/latest_amount 808{i}.txt", "w") as f:
			f.write(str(float_amount))
		
def startButton():
	with open(f'file_com/running_status.txt', 'w') as f:
		f.write('start')

def stopButton():
	with open(f'file_com/running_status.txt', 'w') as f:
		f.write('stop')

def updateStatus():
	with open(f'file_com/running_status.txt', 'r') as f:
		if 'start' in f.readline():
			running_status.setText("Running!")
			layout.addWidget(running_status, 6, 1)
		else:
			running_status.setText("Stopped!")
			layout.addWidget(running_status, 6, 1)

app = QApplication([]) # Creating app instance
window = QWidget()
window.setWindowTitle("Place Bet")


layout = QGridLayout()
layout.addWidget(QLabel("Message:"), 3, 0)
results = QLabel("None")
layout.addWidget(results, 3, 1)
'''layout.addWidget(QPushButton("Button (0, 0)"), 0, 0)
layout.addWidget(QPushButton("Button (0, 1)"), 0, 1)
layout.addWidget(QPushButton("Button (0, 2)"), 0, 2)
layout.addWidget(QPushButton("Button (1, 0)"), 1, 0)
layout.addWidget(QPushButton("Button (1, 1)"), 1, 1)
layout.addWidget(QPushButton("Button (1, 2)"), 1, 2)'''

timer = QtCore.QTimer()
timer.timeout.connect(updateReady)
timer.timeout.connect(updateResult)
timer.timeout.connect(updateStatus)
timer.timeout.connect(updateOddsDisplay)
timer.start(5)

placeBet = QPushButton("Place Bet")
placeBet.clicked.connect(release)
layout.addWidget(placeBet, 4, 1)

reset_result = QPushButton("Clear Message")
reset_result.clicked.connect(resetResult)
layout.addWidget(reset_result, 4, 0)

close_instances = QPushButton("Close Instances")
close_instances.clicked.connect(closeInstances)
layout.addWidget(close_instances, 4, 2)

label_1 = QLabel(ready)
label_2 = QLabel(ready)
label_3 = QLabel(ready)
label_4 = QLabel(ready)
label_5 = QLabel(ready)
label_6 = QLabel(ready)
label_7 = QLabel(ready)
label_8 = QLabel(ready)

# Change amount
change_amount = QLineEdit()
change_amount_button = QPushButton("Change amount")
layout.addWidget(change_amount, 5, 1)
layout.addWidget(change_amount_button, 5, 0)
change_amount_button.clicked.connect(changeAmount)

# Start/Stop
running_status = QLabel(status)
start_button = QPushButton("Start")
stop_button = QPushButton("Stop")
layout.addWidget(start_button, 6, 2)
layout.addWidget(stop_button, 6, 0)
start_button.clicked.connect(startButton)
stop_button.clicked.connect(stopButton)

bet_1_odd = '0.0'
bet_1_odd_label = QLabel(bet_1_odd)
bet_2_odd = '0.0'
bet_2_odd_label = QLabel(bet_2_odd)
combined_odd = 'Combined odd - 0.0'
combined_odd_display = QLabel(combined_odd)



window.setLayout(layout)
window.show()
sys.exit(app.exec())