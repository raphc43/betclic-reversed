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

bet_name, amount = sys.argv[1], sys.argv[2]


for i in range(1, 5):
	with open(f"file_com/ready 808{i}.txt", "w") as f:
		f.write('Not Ready')
	subprocess.run(["start", "cmd", "/K", 'mitmproxy', f"-p 808{i}", "-s .\\proxy_script.py"], shell=True)

with open(f"file_com/release.txt", "w") as f:
	f.write('NULL')

with open(f"file_com/latest.txt", "w") as f:
	f.write('NULL')

with open(f"file_com/latest_amount.txt", "w") as f:
	f.write(amount)

#for i in range(1, int(instances)+1):
for i in range(1, 5):
	time.sleep(3)
	subprocess.Popen(['python.exe', "selenium_script.py", f"808{i}", bet_name])



counter = 0
ready = 'Not Ready'

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


	return ready_8081, ready_8082, ready_8083, ready_8084, ready_8085

def updateReady():
	ready_8081, ready_8082, ready_8083, ready_8084, ready_8085 = extractReady()

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
		if latest_port != 'NULL':
			with open(f"file_com/release.txt", "w") as q:
				q.write(latest_port)
	return

app = QApplication([]) # Creating app instance
window = QWidget()
window.setWindowTitle("Place Bet")

'''
while True:
	if counter > 3:
		ready = 'FALSE'
	else:
		ready = 'TRUE'
	counter+=1
'''
layout = QGridLayout()
'''layout.addWidget(QPushButton("Button (0, 0)"), 0, 0)
layout.addWidget(QPushButton("Button (0, 1)"), 0, 1)
layout.addWidget(QPushButton("Button (0, 2)"), 0, 2)
layout.addWidget(QPushButton("Button (1, 0)"), 1, 0)
layout.addWidget(QPushButton("Button (1, 1)"), 1, 1)
layout.addWidget(QPushButton("Button (1, 2)"), 1, 2)'''
placeBet = QPushButton("Place Bet")
placeBet.clicked.connect(release)
layout.addWidget(placeBet, 2, 1)

label_1 = QLabel(ready)
label_2 = QLabel(ready)
label_3 = QLabel(ready)
label_4 = QLabel(ready)
label_5 = QLabel(ready)


window.setLayout(layout)
timer = QtCore.QTimer()
timer.timeout.connect(updateReady)
timer.start(51)

window.show()
sys.exit(app.exec())