from PyQt5.QtWidgets import QMessageBox
def box(icon,title,text,detail,buttons=False,cmd=None):
	msg = QMessageBox()
	msg.setIcon(icon)
	msg.setText(text)
	msg.setWindowTitle(title)
	msg.setDetailedText(detail)
	if buttons:
		msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
		msg.buttonClicked.connect(cmd)
	msg.exec_()