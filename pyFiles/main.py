import sys
from db import Connect
from PyQt5 import QtCore, QtGui, QtWidgets
from main_ui import Ui_MainWindow
from listBuyers import ListBuyersWindow
from listInvestors import ListInvestorsWindow
from monthlyDetails import MonthlyDetailsWindow
from qistEntry import QistWindow
from export import ExportWindow
from payProft import PayProftWindow

class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.refresh()

        self.buyersBtn.clicked.connect(self.displayBuyerList)
        self.investorsBtn.clicked.connect(self.displayInvestorList)
        self.detailsBtn.clicked.connect(self.displayDetails)
        self.addQistBtn.clicked.connect(self.displayQist)
        self.exportBtn.clicked.connect(self.displayExport)
        self.payBtn.clicked.connect(self.displayProfit)
    def displayBuyerList(self):
    	self.buyerWindow = ListBuyersWindow()
    	self.buyerWindow.display(self.refresh)
    def displayInvestorList(self):
    	self.investorWindow = ListInvestorsWindow()
    	self.investorWindow.display(self.refresh)
    def displayDetails(self):
    	self.detailsWindow = MonthlyDetailsWindow()
    	self.detailsWindow.display()
    def displayQist(self):
    	self.qistWindow = QistWindow()
    	self.qistWindow.display(self.refresh)

    def displayExport(self):
        self.exportWindow = ExportWindow()
        self.exportWindow.display()

    def displayProfit(self):
        self.payProftWindow = PayProftWindow()
        self.payProftWindow.display(self.refresh)

    def refresh(self):
        self.con = Connect()
        details = self.con.getAllDetails()
        self.totalCostLabel.setText(str(round(float(details['cost_price']))))
        self.totaOtherLabel.setText(str(round(float(details['other']))))
        self.remainLabel.setText(str(round(float(details['remaining_price']))))
        self.profitLabel.setText(str(round(float(details['net_profit']))))
        self.totalSaleLabel.setText(str(round(float(details['sale_price']))))
        self.totalPaidLabel.setText(str(round(float(details['total_paid']))))
        self.balanceLabel.setText(str(round(float(details['total_balance']))))
        


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())