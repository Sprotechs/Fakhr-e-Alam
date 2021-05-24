from PyQt5 import QtCore, QtGui, QtWidgets
from addBuyer_ui import Ui_MainWindow
from db import Connect
from msgBox import box
class AddBuyerWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.con = Connect()
        investors = self.con.getInvestors()
        for inv in [{"id":0,"name":"Select Investor"}]+investors:
            self.investorBox.addItem(inv['name'],inv['id'])
        self.addBtn.clicked.connect(self.addBuyer)

    def addBuyer(self):
        name = self.nameInput.text().strip()
        if not name.strip():
            box(2,"Name Required","Please Enter Buyer Name","")
            return 
        contact = self.contactInput.text().strip()
        address = self.addressInput.text().strip()
        description = self.descriptionInput.text().strip()
        investor = self.investorBox.currentIndex()
        if investor==0:
            box(2,"Investor Required","Please Select Investor","")
            return 
        investor = self.investorBox.itemData(self.investorBox.currentIndex())
        monthlyQist = self.qistInput.value()
        costPrice = self.costInput.value()
        if not costPrice:
            box(2,"Cost Price Required","Please Enter Cost Price","")
            return
        other = self.otherInput.value()
        share = self.shareInput.value()
        joinDate = self.joinDateInput.dateTime().toString('dd/MMMM/yyyy')
        data = {'name':name,'address':address,'contact':contact,'description':description,'monthly_qist':monthlyQist,
        'investor_id':investor,'other_amount':other,'cost_price':costPrice,'share':share,'join_date':joinDate}
        self.con.addBuyer(data)
        box(1,"Buyer Added","Buyer Added to the Database","")
        self.refresh()
    def display(self,button):
        self.refresh = button
        self.show()


        
import sys
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = AddBuyerWindow()
    window.show()
    sys.exit(app.exec_())