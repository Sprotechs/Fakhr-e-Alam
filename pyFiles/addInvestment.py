from PyQt5 import QtCore, QtGui, QtWidgets
from addInvestment_ui import Ui_MainWindow
from db import Connect
from msgBox import box
class AddInvestmentWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.con = Connect()
        investors = self.con.getInvestors()
        for inv in [{"id":0,"name":"Select Investor"}]+investors:
            self.nameBox.addItem(inv['name'],inv['id'])
        self.addBtn.clicked.connect(self.addBuyer)

    def addBuyer(self):
        investor = self.nameBox.currentIndex()
        if investor==0:
            box(2,"Investor Required","Please Select Investor","")
            return 
        investor = self.nameBox.itemData(self.nameBox.currentIndex())
        amount = self.amountInput.value()
        if not amount:
            box(2,"Amount Required","Please Enter Price","")
            return
        joinDate = self.joinDateInput.dateTime().toString('dd/MMMM/yyyy')
        data = {'investor_id':investor,'amount':amount,'join_date':joinDate}
        self.con.addInvestment(data)
        box(1,"Added","Investment Added","")
        self.refresh()
    def display(self,button):
        self.refresh = button
        self.show()


        
import sys
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = AddInvestmentWindow()
    window.show()
    sys.exit(app.exec_())