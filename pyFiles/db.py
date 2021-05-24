import sqlite3,os
class Connect:
	def connect(self):
		if not os.path.exists('kitab.db'):
			import createDb
		self.db = sqlite3.connect("kitab.db")
	def getBuyers(self,buyerId=None):
		self.connect()
		data = []
		if not buyerId:
			cursor = self.db.execute("SELECT * FROM buyers")
		else:
			cursor = self.db.execute("SELECT * FROM buyers WHERE id=?",(buyerId,))
		for row in cursor:
			cells = {key:str(value) for key,value in zip(["id","name","address","contact","description","monthly_qist","investor_id","cost_price","other","sale_price","share","remaining_price","net_profit","total_paid","raff","join_date"],row)}
			investor = self.getInvestors(cells['investor_id'])
			cells['investor_name'] =  investor[0]['name'] if investor else "Invalid Investor"
			data.append(cells) 
		self.db.close()
		return data
	def getInvestorDetails(self,investorId):
		self.connect()
		data = []
		for row in self.db.execute("SELECT sum(cost_price),sum(other_amount),sum(sale_price),sum(remaining_price),sum(total_paid) FROM buyers WHERE investor_id=?",(investorId,)):
			cells = {key:str(value) for key,value in zip(["cost_price","other","sale_price","remaining_price","total_paid"],row if row != (None,None,None,None,None) else [0.0,0.0,0.0,0.0,0.0])}
			data.append(cells) 
		self.db.close()
		return data[0]
	def getBuyerDetails(self,buyerId):
		self.connect()
		data = []
		for row in self.db.execute("SELECT cost_price,other_amount,sale_price,remaining_price,total_paid FROM buyers WHERE id=?",(buyerId,)):
			cells = {key:str(value) for key,value in zip(["cost_price","other","sale_price","remaining_price",'total_paid'],row if row != (None,None,None,None) else [0.0,0.0,0.0,0.0])}
			data.append(cells) 
		self.db.close()
		return data[0]
	def getBalance(self,investorId):
		self.connect()
		cursor = self.db.execute("SELECT sum(debit),sum(credit) from ledger where investor_id=?",(investorId,))
		debit,credit=cursor.fetchone()
		if not debit and not credit:
			return 0.0
		return (debit-credit)

	def getAllDetails(self):
		self.connect()
		data = []
		for row in self.db.execute("SELECT sum(cost_price),sum(other_amount),sum(sale_price),sum(remaining_price),sum(net_profit),sum(total_paid) FROM buyers"):
			cells = {key:str(value) for key,value in zip(["cost_price","other","sale_price","remaining_price","net_profit","total_paid"],row if row != (None,None,None,None,None,None) else [0.0,0.0,0.0,0.0,0.0,0.0])}
			balance = 0.0
			for investor in self.db.execute("SELECT id from investors"):
				balance+=self.getBalance(investor[0])
			cells['total_balance'] = balance
			data.append(cells) 

		self.db.close()
		return data[0]
	def getInvestors(self,id_=None):
		self.connect()
		rows = []
		if not id_:
			cursor = self.db.execute("SELECT * FROM investors")
		else:
			cursor = self.db.execute("SELECT * FROM investors WHERE ID = ?",(id_,))
		for row in cursor:
			row = {key:str(value) for key,value in zip(["id","name","address","contact","join_date"],row)}
			rows.append(row)
		self.db.close()
		return rows
	def addBuyer(self,data):
		self.connect()
		name = data['name']
		address = data['address']
		contact = data['contact']
		description = data['description']
		monthlyQist = data['monthly_qist']
		investorId = data['investor_id']
		otherAmount = data['other_amount']
		costPrice = data['cost_price']
		share = data['share']
		joinDate = data['join_date']
		netProfit = (share/100)*costPrice
		salePrice = costPrice+netProfit
		remainingPrice = salePrice
		totalPaid = 0.0
		raff = salePrice/netProfit
		self.db.execute("""INSERT INTO buyers(NAME,ADDRESS,CONTACT,DESCRIPTION,MONTHLY_QIST,INVESTOR_ID,COST_PRICE,OTHER_AMOUNT,SALE_PRICE,SHARE,REMAINING_PRICE,NET_PROFIT,TOTAL_PAID,RAFF_WORK,JOIN_DATE) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",(name,address,contact,description,monthlyQist,investorId,costPrice,otherAmount,salePrice,share,remainingPrice,netProfit,totalPaid,raff,joinDate))
		self.db.commit()
		buyerId = self.db.execute("""SELECT id from buyers ORDER BY id DESC LIMIT 1""").fetchone()[0]
		self.db.execute("""INSERT INTO ledger (buyer_id,investor_id,description,datentime,debit,credit) VALUES(?,?,?,?,?,?)""",(buyerId,investorId,description,joinDate,0.0,costPrice))
		self.db.commit()
		self.db.execute("""INSERT INTO ledger (buyer_id,investor_id,description,datentime,debit,credit) VALUES(?,?,?,?,?,?)""",(buyerId,investorId,'Other Amount',joinDate,otherAmount/2,0.0))
		self.db.commit()
		self.db.close()
	def execute(self,string,data = set()):
		self.connect()
		if data:
			rows = [row for row in self.db.execute(string,data)]
		else:
			rows = [row for row in self.db.execute(string)]
		try:
			self.db.commit()
		except:
			pass
		self.db.close()
		return rows
	def addMonthlyQist(self,data):
		self.connect()
		buyerId = data['buyer_id']
		investorId = data['investor_id']
		month = data['month']
		year = data['year']
		paid = data['paid']
		cost = data['cost']
		profit = data['profit']
		self.db.execute("""INSERT INTO monthly_details(buyer_id,investor_id,month,year,paid,cost,profit) VALUES (?,?,?,?,?,?,?)""",(buyerId,investorId,month,year,paid,cost,profit))
		self.db.commit()
		self.db.execute("""INSERT INTO ledger (buyer_id,investor_id,description,datentime,debit,credit) VALUES(?,?,?,?,?,?)""",(buyerId,investorId,"Qist Received","1/"+month+"/"+year,paid,0.0))
		self.db.commit()
		self.db.close()

	def getMonthlyDetails(self,buyerId=None,investorId=None):
		self.connect()
		rows = []
		if not buyerId and not investorId:
			cursor = self.db.execute("""SELECT month,year,paid,cost,profit FROM monthly_details""")
		elif not investorId:
			cursor = self.db.execute("""SELECT month,year,paid,cost,profit FROM monthly_details WHERE buyer_id=?""",(buyerId,))
		else:
			cursor = self.db.execute("""SELECT month,year,paid,cost,profit FROM monthly_details WHERE investor_id=?""",(investorId,))
		for row in cursor:
			if not row:
				continue
			cells = {key:value for key,value in zip(['month','year','paid','cost','profit'],row)}
			rows.append(cells)
		self.db.close()
		return rows

	def deleteBuyer(self,buyerId=None,investorId=None):
		self.connect()
		if investorId:
			self.db.execute("""DELETE FROM buyers WHERE investor_id=?""",(investorId,))
		else:
			self.db.execute("""DELETE FROM buyers WHERE id=?""",(buyerId,))
		self.db.commit()
		self.db.close()

	def deleteInvestor(self,investorId,buyerId=None):
		self.connect()
		self.db.execute("""DELETE FROM investors WHERE id=?""",(investorId,))
		self.db.commit()
		self.db.close()
	def deleteMonthlyDetails(self,buyerId):
		self.connect()
		self.db.execute("""DELETE FROM monthly_details WHERE buyer_id=?""",(buyerId,))
		self.db.commit()
		self.db.close()
	def addInvestor(self,data):
		self.connect()
		name = data['name']
		address = data['address']
		contact = data['contact']
		joinDate = data['join_date']
		self.db.execute("""INSERT INTO investors(NAME,ADDRESS,CONTACT,JOIN_DATE) VALUES (?,?,?,?)""",(name,address,contact,joinDate))
		self.db.commit()
		self.db.close()
	def getProfit(self,investorId):
		self.connect()
		cursor = self.db.execute("""SELECT sum(profit) FROM monthly_details WHERE investor_id=?""",(investorId,)).fetchone()[0]
		self.db.close()
		return cursor/2 if cursor else 0.0
	def getInvestment(self,investorId):
		self.connect()
		cursor = self.db.execute("""SELECT sum(amount) FROM investment WHERE investor_id=?""",(investorId,)).fetchone()[0]
		self.db.close()
		return cursor if cursor else 0.0

	def addInvestment(self,data):
		self.connect()
		investorId = data['investor_id']
		amount = data['amount']
		joinDate = data['join_date']
		self.db.execute("""INSERT INTO investment(investor_id,amount,join_date) VALUES (?,?,?)""",(investorId,amount,joinDate))
		self.db.commit()
		self.db.execute("""INSERT INTO ledger (buyer_id,investor_id,description,datentime,debit,credit) VALUES(?,?,?,?,?,?)""",(-1,investorId,"Investment Amount",joinDate,amount,0.0))
		self.db.commit()
		self.db.close()
	def payProfit(self,data):
		self.connect()
		investorId = data['investor_id']
		amount = data['amount']
		month = data['month']
		year = data['year']
		joinDate = data['datentime']

		self.db.execute("""INSERT INTO profit_paid (investor_id,datentime,amount,month,year) VALUES(?,?,?,?,?)""",(investorId,joinDate,amount,month,year))
		self.db.commit()
		self.db.execute("""INSERT INTO ledger (buyer_id,investor_id,description,datentime,debit,credit) VALUES(?,?,?,?,?,?)""",(-1,investorId,"Profit Amount Paid",joinDate,0.0,amount))
		self.db.commit()
		self.db.close()

# con = Connect()
# print(con.execute("SELECT * FROM profit_paid"))
