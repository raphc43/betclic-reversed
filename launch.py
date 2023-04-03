# dialog.py

"""Dialog-style application."""

import sys, subprocess

from PyQt6.QtWidgets import (
	QApplication,
	QDialog,
	QDialogButtonBox,
	QFormLayout,
	QLineEdit,
	QVBoxLayout,
	QPushButton,
	QWidget
)

def startBet():
	if "https://www." not in link.text():
		new_link = f"https://www.{link.text()}"
	else:
		new_link = link.text()

	subprocess.Popen(['python.exe', "new_window.py", bet_xpath.text(), amount.text(), new_link])

app = QApplication([]) # App instance

window = QWidget()
window.setWindowTitle("QDialog")
dialogLayout = QVBoxLayout()

bet_xpath = QLineEdit()
amount = QLineEdit()
link = QLineEdit()

formLayout = QFormLayout()
formLayout.addRow("Bet Xpath:", bet_xpath)
formLayout.addRow("Amount:", amount)
formLayout.addRow("Link:", link)
#formLayout.addRow("Instances:", instances)
dialogLayout.addLayout(formLayout)
'''buttons = QDialogButtonBox()
buttons.setStandardButtons(
    QDialogButtonBox.StandardButton.Cancel
    | QDialogButtonBox.StandardButton.Ok
)'''
button = QPushButton("Start")
button.clicked.connect(startBet)
dialogLayout.addWidget(button)
window.setLayout(dialogLayout)


window.show()
sys.exit(app.exec())