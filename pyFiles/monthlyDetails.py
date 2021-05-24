from PyQt5 import QtCore, QtGui, QtWidgets
from monthlyDetails_ui import Ui_MainWindow
from db import Connect
#618
class MonthlyDetailsWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

    def insertRow(self,row):
        table = self.detailsTable
        rowPosition = table.rowCount()
        table.insertRow(rowPosition)
        table.setItem(rowPosition , 0, QtWidgets.QTableWidgetItem(row['month']))
        table.setItem(rowPosition , 1, QtWidgets.QTableWidgetItem(row['year']))
        table.setItem(rowPosition , 2, QtWidgets.QTableWidgetItem(str(round(float(row['paid'])))))
        table.setItem(rowPosition , 3, QtWidgets.QTableWidgetItem(str(round(float(row['cost'])))))
        table.setItem(rowPosition , 4, QtWidgets.QTableWidgetItem(str(round(float(row['profit'])))))
    
    def display(self,type='S',id_=None):
        self.con = Connect()
        d = {}
        if type =='S':
            data = self.con.getMonthlyDetails()
            moreData = self.con.getAllDetails()
            self.nameLabel.setText("Unknown")
            self.typeLabel.setText("Seller")
            self.setMaximumSize(618,613)
        if type =='I':
            data = self.con.getMonthlyDetails(investorId=id_)
            investor = self.con.getInvestors(id_)[0]
            moreData = self.con.getInvestorDetails(id_)
            self.nameLabel.setText(investor['name'])
            self.typeLabel.setText("Investor")
            self.setMaximumSize(618,613)

        if type =='B':
            data = self.con.getMonthlyDetails(buyerId=id_)
            buyer = self.con.getBuyers(id_)[0]
            moreData = self.con.getBuyerDetails(id_)
            self.nameLabel.setText(buyer['name'])
            self.typeLabel.setText("Buyer")


        self.remainLabel.setText(str(round(float(moreData['remaining_price']))))
        self.totalLabel.setText(str(round(float(moreData['total_paid']))))
        for row in data:
            key = row['month']+'/'+row['year']
            if d.get(key):
            	d[key]['cost'] += row['cost']
            	d[key]['profit'] += row['profit']
            	d[key]['paid'] += row['paid']
            else:
            	d[key] = {}
            	d[key]['cost'] = row['cost']
            	d[key]['profit'] = row['profit']
            	d[key]['paid'] = row['paid']
        for key,value in d.items():
            month,year = key.split('/')
            value['month'] = month
            value['year'] = year
            if type=="I":
                value['profit'] = value['profit']/2
            self.insertRow(value)
        if type == "B":
            data = self.con.getBuyers(id_)
            table = self.tableWidget
            for key,value in data[0].items():  
                if key in ['investor_id','raff']:
                    continue
                rowPosition = table.rowCount()
                table.insertRow(rowPosition)
                table.setItem(rowPosition , 0, QtWidgets.QTableWidgetItem(key))
                table.setItem(rowPosition , 1, QtWidgets.QTableWidgetItem(value))
        self.show()
