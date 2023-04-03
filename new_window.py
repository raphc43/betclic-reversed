# dialog.py

"""Dialog-style application."""

import sys, subprocess, time

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
from PyQt6 import QtCore

bet_name, amount, link = sys.argv[1], sys.argv[2], sys.argv[3]


for i in range(1, 5):
	with open(f"file_com/ready 808{i}.txt", "w") as f:
		f.write('Not Ready')
	#subprocess.run(["start", "cmd", "/K", 'mitmproxy', f"-p 808{i}", "-s .\\proxy_script.py"], shell=True)

with open(f"file_com/release.txt", "w") as f:
	f.write('NULL')

with open(f"file_com/latest.txt", "w") as f:
	f.write('NULL')

with open(f"file_com/latest_amount.txt", "w") as f:
	f.write(amount)

with open(f'file_com/amount_counter.txt', 'w') as f:
	f.write('0')

with open(f'file_com/initial_amount.txt', 'w') as f:
	f.write(amount)

with open(f'file_com/exit.txt', 'w') as q:
	q.write('false')

with open('file_com/results.txt', 'w') as q:
	q.write('None')

with open('file_com/initial_odd.txt', 'w') as b:
	b.write('0')

with open('file_com/special_reload.txt', 'w') as f:
	f.write('NULL')

with open(f'file_com/running_status.txt', 'w') as f:
	f.write('start')

#for i in range(1, int(instances)+1):
if "betclic.fr/live" not in link:
	for i in range(1, 5):
		time.sleep(3)
		subprocess.Popen(['python.exe', "selenium_script2.py", f"808{i}", bet_name, amount, link])
else:
	for i in range(1, 5):
		time.sleep(3)
		subprocess.Popen(['python.exe', "selenium_script.py", f"808{i}", bet_name, amount, link])



ready = 'Not Ready'
status = 'Running'

def extractReady():
	with open("file_com/ready 8081.txt", "r") as f:
		ready_8081 = f.readline()
	with open("file_com/ready 8082.txt", "r") as f:
		ready_8082 = f.readline()
	with open("file_com/ready 8083.txt", "r") as f:
		ready_8083 = f.readline()
	with open("file_com/ready 8084.txt", "r") as f:
		ready_8084 = f.readline()


	return ready_8081, ready_8082, ready_8083, ready_8084

def updateReady():
	ready_8081, ready_8082, ready_8083, ready_8084 = extractReady()

	label_1.setText(ready_8081)
	layout.addWidget(label_1, 0, 0)

	label_2.setText(ready_8082)
	layout.addWidget(label_2, 0, 1)

	label_3.setText(ready_8083)
	layout.addWidget(label_3, 0, 2)

	label_4.setText(ready_8084)
	layout.addWidget(label_4, 1, 1)

	#label_5.setText(ready_8085)
	#layout.addWidget(label_5, 1, 1)

def release():
	with open(f"file_com/latest.txt", "r") as f:
		latest_port = f.readline()

	with open(f"file_com/ready {latest_port}.txt", "r") as f:
		ready_state = f.readline()

	if latest_port != 'NULL' and ready_state == "Ready":
		with open(f"file_com/release.txt", "w") as q:
			q.write(latest_port)
	else:
		with open(f"file_com/results.txt", "w") as f:
			f.write("You pressed at the wrong time!")
	return

def updateResult():
	with open(f"file_com/results.txt", "r") as f:
		results.setText(f.readline())
		layout.addWidget(results, 2, 1)

def resetResult():
	with open(f"file_com/results.txt", "w") as f:
		f.write("None")

def closeInstances():
	with open(f"file_com/exit.txt", "w") as f:
		f.write("true")
	time.sleep(1)
	with open(f"file_com/results.txt", "w") as f:
		f.write("Successfully closed")

def changeAmount():
	with open(f"file_com/latest_amount.txt", "w") as f:
		f.write(change_amount.text())
	with open(f'file_com/amount_counter.txt', 'w') as f:
		f.write('0')
	with open(f'file_com/initial_amount.txt', 'w') as f:
		f.write(change_amount.text())
		
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
			layout.addWidget(running_status, 5, 1)
		else:
			running_status.setText("Stopped!")
			layout.addWidget(running_status, 5, 1)

app = QApplication([]) # Creating app instance
window = QWidget()
window.setWindowTitle("Place Bet")


layout = QGridLayout()
layout.addWidget(QLabel("Message:"), 2, 0)
results = QLabel("None")
layout.addWidget(results, 2, 1)
'''layout.addWidget(QPushButton("Button (0, 0)"), 0, 0)
layout.addWidget(QPushButton("Button (0, 1)"), 0, 1)
layout.addWidget(QPushButton("Button (0, 2)"), 0, 2)
layout.addWidget(QPushButton("Button (1, 0)"), 1, 0)
layout.addWidget(QPushButton("Button (1, 1)"), 1, 1)
layout.addWidget(QPushButton("Button (1, 2)"), 1, 2)'''
placeBet = QPushButton("Place Bet")
placeBet.clicked.connect(release)
layout.addWidget(placeBet, 3, 1)

reset_result = QPushButton("Clear Message")
reset_result.clicked.connect(resetResult)
layout.addWidget(reset_result, 3, 0)

close_instances = QPushButton("Close Instances")
close_instances.clicked.connect(closeInstances)
layout.addWidget(close_instances, 3, 2)


label_1 = QLabel(ready)
label_2 = QLabel(ready)
label_3 = QLabel(ready)
label_4 = QLabel(ready)
label_5 = QLabel(ready)

# Change amount
change_amount = QLineEdit()
change_amount_button = QPushButton("Change amount")
layout.addWidget(change_amount, 4, 1)
layout.addWidget(change_amount_button, 4, 0)
change_amount_button.clicked.connect(changeAmount)

# Start/Stop
running_status = QLabel(status)
start_button = QPushButton("Start")
stop_button = QPushButton("Stop")
layout.addWidget(start_button, 5, 2)
layout.addWidget(stop_button, 5, 0)
start_button.clicked.connect(startButton)
stop_button.clicked.connect(stopButton)


window.setLayout(layout)

timer = QtCore.QTimer()
timer.timeout.connect(updateReady)
timer.timeout.connect(updateResult)
timer.timeout.connect(updateStatus)
timer.start(51)

window.show()
sys.exit(app.exec())