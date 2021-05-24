from PyQt5 import QtCore, QtGui, QtWidgets
from qistEntry_ui import Ui_MainWindow
from db import Connect
from datetime import datetime
from msgBox import box
class QistWindow(QtWidgets.QMainWindow, Ui_MainWindow):
	def __init__(self):
		QtWidgets.QMainWindow.__init__(self)
		Ui_MainWindow.__init__(self)
		self.setupUi(self)
		self.con = Connect()
		for buyer in [{'id':0,'name':'Select Buyer'}]+self.con.getBuyers():
			self.nameBox.addItem(buyer['name'],buyer['id'])
		for month in ['Select Month']+[datetime.strptime(f"2019-{m}-15",'%Y-%m-%d').strftime('%B') for m in range(1,13)]:
			self.monthBox.addItem(month)
		date = int(datetime.now().strftime('%Y'))
		for year in ['Select Year']+[str(y) for y in range(date-5,date+6)]:
			self.yearBox.addItem(year)
		self.addBtn.clicked.connect(self.addQist)
	def display(self,button):
		self.mainRefresh=button
		self.show()
	def addQist(self):
		buyerId = self.nameBox.itemData(self.nameBox.currentIndex())
		year = self.yearBox.currentText()
		month = self.monthBox.currentText()
		if buyerId==0:
			box(2,"Select Buyer",f"Select Buyer First","")
			return 
		if self.monthBox.currentIndex()<1:
			box(2,"Select Month",f"Please Select Month","")
			return 
		if self.yearBox.currentIndex()<1:
			box(2,"Select Year",f"Please Select Year","")
			return 
		self.con.connect()
		investor = [row for row in self.con.db.execute('SELECT investor_id,raff_work,remaining_price,total_paid FROM buyers WHERE id=?',(buyerId,))]
		self.con.db.close()
		amount = self.amountInput.value()
		try:
			profit = amount / (investor[0][1] if investor else 0.0)
		except:
			profit = 0.0
		cost = amount - profit
		self.con.execute('UPDATE buyers SET remaining_price=?,total_paid=? where id=?',(investor[0][2]-amount,investor[0][3]+amount,buyerId))
		self.con.addMonthlyQist({'buyer_id':buyerId,'investor_id':investor[0][0] if investor else -1,'month':month,'month_index':self.monthBox.currentIndex(),'year':year,'paid':amount,'cost':cost,'profit':profit})
		box(1,"Added",f"Qist Entry successfully completed","")
		self.mainRefresh()

import sys
if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	window = QistWindow()
	window.show()
	sys.exit(app.exec_())