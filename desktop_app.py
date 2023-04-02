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
	subprocess.Popen(['python.exe', "new_window.py", bet_name.text(), amount.text()])

app = QApplication([]) # App instance

window = QWidget()
window.setWindowTitle("QDialog")
dialogLayout = QVBoxLayout()

bet_name = QLineEdit()
amount = QLineEdit()
instances = QLineEdit()

formLayout = QFormLayout()
formLayout.addRow("Bet name:", bet_name)
formLayout.addRow("Amount:", amount)
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