from PyQt5 import QtCore, QtGui, QtWidgets
from payProft_ui import Ui_MainWindow
from db import Connect
from datetime import datetime
from msgBox import box
class PayProftWindow(QtWidgets.QMainWindow, Ui_MainWindow):
	def __init__(self):
		QtWidgets.QMainWindow.__init__(self)
		Ui_MainWindow.__init__(self)
		self.setupUi(self)
		self.con = Connect()
		for investor in self.con.getInvestors():
			self.investorBox.addItem(investor['name'],investor['id'])
		self.payBtn.clicked.connect(self.addQist)
		self.monthBox.currentIndexChanged.connect(self.changeProfitValue)
		self.yearBox.currentIndexChanged.connect(self.changeMonthBox)
		self.investorBox.currentIndexChanged.connect(self.changeYearBox)
	def changeMonthBox(self):
		self.monthBox.clear()
		data = self.con.execute("SELECT month,year FROM monthly_details where investor_id=? AND year=?",(self.investorBox.itemData(self.investorBox.currentIndex()),self.yearBox.currentText()))
		months = list(set([d[0] for d in data if d[1]]))
		months.sort()
		for month in ["Select Month"]+months:
			self.monthBox.addItem(month)
	def changeYearBox(self):
		self.yearBox.clear()
		investor = self.investorBox.itemData(self.investorBox.currentIndex())
		data = self.con.execute("SELECT year FROM monthly_details where investor_id=?",(investor))
		years = list(set([d[0] for d in data]))
		years.sort()
		for year in ["Select Year"]+years:
			self.yearBox.addItem(year)
	def changeProfitValue(self):
		if self.yearBox.currentIndex()<1 or self.monthBox.currentIndex()<1 or self.investorBox.currentIndex() == 0:
			self.profitInput.setValue(0)
			return
		investor = self.investorBox.itemData(self.investorBox.currentIndex())
		data = self.con.execute("SELECT profit/2 FROM monthly_details WHERE investor_id=? and month=? and year=?",(investor,self.monthBox.currentText(),self.yearBox.currentText()))
		self.profitInput.setValue(round(data[0][0]))
		isPaid = self.con.execute("SELECT amount,datentime FROM profit_paid WHERE year=? and month=?",(self.yearBox.currentText(),self.monthBox.currentText()))
		if isPaid:
			box(2,"Already Paid",f"For the following month and year, {isPaid[0][0]} was already paid on {isPaid[0][1]}","")
			self.payBtn.setEnabled(False)
			return
		self.payBtn.setEnabled(True)
		


	def display(self,button):
		self.mainRefresh=button
		self.show()
	def addQist(self):
		investorId = self.investorBox.itemData(self.investorBox.currentIndex())
		year = self.yearBox.currentText()
		month = self.monthBox.currentText()
		if investorId==0:
			box(2,"Select Investor",f"Select Investor First","")
			return 
		if self.monthBox.currentIndex()<1:
			box(2,"Select Month",f"Please Select Month","")
			return 
		if self.yearBox.currentIndex()<1:
			box(2,"Select Year",f"Please Select Year","")
			return 
		self.con.connect()
		investor = self.investorBox.itemData(self.investorBox.currentIndex())
		amount = self.amountInput.value()
		datentime = self.joinDateInput.dateTime().toString('dd/MMMM/yyyy')
		data = {"investor_id":investor,"amount":amount,"month":self.monthBox.currentText(),
				"year":self.yearBox.currentText(),'datentime':datentime}
		self.con.payProfit(data)
		box(1,"Paid",f"For the following month and year, {amount} paid on {datentime}","")
		try:
			self.mainRefresh()
		except:
			pass

import sys
if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	window = PayProftWindow()
	window.show()
	sys.exit(app.exec_())