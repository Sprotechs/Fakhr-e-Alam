from PyQt5 import QtCore, QtGui, QtWidgets
from addInvestor_ui import Ui_MainWindow
from db import Connect
from msgBox import box
class AddInvestorWindow(QtWidgets.QMainWindow, Ui_MainWindow):
	def __init__(self):
		QtWidgets.QMainWindow.__init__(self)
		Ui_MainWindow.__init__(self)
		self.setupUi(self)
		self.addBtn.clicked.connect(self.addInvestor)
	def addInvestor(self):
		name = self.nameInput.text().strip()
		contact = self.contactInput.text().strip()
		address = self.addressInput.text().strip()
		joinDate = self.joinDateInput.dateTime().toString('dd/MMMM/yyyy')
		if not name:
			box(2,"Name Required",f"Name must be entered","")
			return
		con = Connect()
		investors = [inv['name'] for inv in con.getInvestors() if inv]
		if name in investors:
			box(2,"Invalid Investor",f"Investor is Already Added","")
			return
		con.addInvestor({"name":name,"contact":contact,"address":address,"join_date":joinDate})
		box(0,"Added",f"Successfully Added Investor","")
		self.refresh()
	def display(self,button):
		self.refresh = button
		self.show()

import sys
if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	window = AddInvestorWindow()
	window.show()
	sys.exit(app.exec_())