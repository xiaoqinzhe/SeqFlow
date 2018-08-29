# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from app.trading.visual_market import VMarket
from util import util
from datetime import datetime
from app.trading.trade_recorder import TradeRecorder

#asset order
class AssetOrder:
	uid=0
	str_title='id order_time asset_code optype price amount service_charge pay'
	def __init__(self, orderTime, assetCode, optype, curPrice, amount, cost, serviceCharge=0):
		self.id=AssetOrder.uid
		AssetOrder.uid+=1
		self.orderTime=orderTime       #order time
		self.assetCode=assetCode      #which asset
		self.optype=optype             #operation type: 0 for buy, 1 for sell, 2 for pingcang
		self.curPrice=curPrice         #current asset price
		self.amount=amount             #number of shou asset
		self.serviceCharge=serviceCharge  #fu wu fei
		self.totalCost=cost+serviceCharge    #total cost
		self.remainMoney=0.0
		self.curEarning=0.0       #cur earning if sell

	def toString(self):
		return '%d %d %s %d %f %d %f %f' % (self.id, self.orderTime, self.assetCode, \
			self.optype, self.curPrice, self.amount, self.serviceCharge, -self.totalCost)

sim_st=20170126
sim_et=20180126

#asset trade
class Trader:
	def __init__(self, decision, st=sim_st, et=sim_et, codes=None):
		self.assets=[]                     #asset
		self.curtime=st                    #current time		
		self.market = VMarket(st=st, et=et, codes=codes)      #trade market
		if self.curtime is None:
			self.curtime = self.market.curtime
		self.codes=self.market.codes
		self.orders=[]                     #asset orders
		self.oldorders=[]
		self.decision=decision             #making decision
		self.serviceChargeRate=0.001
		self.initmoney=10000.0                 #init investment money
		self.curmoney=self.initmoney                  #current remain money		
		self.profit=0.0                    #profit
		self.roreturn=0.0                  #rate of return
		self.alrProfit=0.0                 #已经得到的利润
		self.inmoneyp=0.0                  #investment money in a period
		self.outmoneyp=0.0                 #return money in a period
		self.sharpeRatio=0.0
		self.recorder=TradeRecorder()      #recoder
		self.recorder.initmoney=self.initmoney
		self.isCharged=True

	def run(self):
		while(True):
			#update current time
			#day=self.curtime.day
			self.curtime=self.market.curtime
			#if not market.judgeTradeDay(curtime): continue
			#update asset and etf info from market (prices...)
			self.market.nextState()
			if self.market.endFlag: break
			#calculate period return
			# if self.curtime.day!=day: self.periodProfit()
			self.periodProfit()
			#make decision and handle
			closeOrders, decOrders=self.decision.decide(self)
			# return format of decide(): [id1, id2, ...], [[code, optype, amount]]
			self.handleTrade(closeOrders, decOrders)
			self.recorder.addPrice(self.getLastPrice(self.codes[0]))
		self.closeAllOrders()
		self.recorder.finalmoney=self.curmoney
		print(self.curtime, self.profit, self.curmoney)
		self.recorder.showOrders()
		self.recorder.showDailyProfits()
		self.recorder.eval()
		self.recorder.showStatistics()

	def periodProfit(self):
		self.recorder.tradeDays+=1
		p=self.calculateTotalProfit()
		self.outmoneyp=p-self.profit
		self.profit=p
		for order in self.orders:
			if order.optype==0: self.inmoneyp+=order.totalCost
			else: self.inmoneyp-=order.totalCost
		#date=datetime()
		self.recorder.addProfit(self.curtime, self.outmoneyp, self.inmoneyp)
		self.inmoneyp=0.0
		self.roreturn=self.profit/self.initmoney

	def closeAllOrders(self):
		i=0
		while i<len(self.orders):
			self.closeOrder(self.orders[i])

	def closeAssetOrders(self, asset):
		i=0
		while i<len(self.orders):
			order=self.orders[i]
			if order.assetCode==asset.code: 
				self.closeOrder(order)
			else: i+=1

	def handleTrade(self, closeOrders, decOrders):
		for oid in closeOrders:
			order=self.getOrderFId(oid)
			if order: self.closeOrder(order)
		for do in decOrders:
			self.openOrder(do[0], do[1], do[2])
	
	#add order buy
	def openOrder(self, code, optype, amount):
		price=self.getLastPrice(code)
		oo=AssetOrder(self.curtime, code, optype, price, amount, price*amount, self.calServiceCharge(price*amount, self.serviceChargeRate))
		if optype==0 and self.curmoney<oo.totalCost: return False
		self.curmoney-=oo.totalCost
		self.orders.append(oo)
		self.recorder.addOrder(oo)
		oo.remainMoney=self.curmoney
		self.recorder.lots+=1
		return True

	# ping cang order
	def closeOrder(self, corder):
		if corder.optype==0: optype=1
		else: optype=0
		price=self.getLastPrice(corder.assetCode)
		oo=AssetOrder(self.curtime, corder.assetCode, optype, price, \
			corder.amount, -price*corder.amount, self.calServiceCharge(price*corder.amount, self.serviceChargeRate))
		if optype==0 and self.curmoney<oo.totalCost: return False
		self.alrProfit+=(-corder.totalCost-oo.totalCost)
		self.curmoney-=oo.totalCost
		self.orders.remove(corder)
		self.oldorders.append(corder)
		self.oldorders.append(oo)
		self.recorder.addOrder(oo)
		oo.remainMoney=self.curmoney
		if (-corder.totalCost-oo.totalCost)>0: self.recorder.profitTime+=1
		else: self.recorder.lossTime+=1
		return True

	def getOrderFId(self, oid):
		for o in self.orders:
			if o.id==oid:
				return o
		return None

	def getAssetFCode(self, code):
		for op in self.assets:
			if op.code==code:
				return op
		return None
	
	def calculateTotalProfit(self):
		profits=0
		for order in self.orders:
			cost, _=self.orderProfit(order)
			profits+=cost
		profits=profits+self.curmoney-self.initmoney
		return profits

	def orderProfit(self, order):
		if order.optype==0: optype=1
		else: optype=0
		p = self.getLastPrice(order.assetCode)*order.amount
		if optype==0: 
			cost=p+self.calServiceCharge(p, self.serviceChargeRate)
		else: cost=-p+self.calServiceCharge(p, self.serviceChargeRate)
		#print('**', order.assetCode, order.totalCost, cost, '**')
		order.earning=order.totalCost+cost

		return -cost, order.earning

	def getLastPrice(self, assetCode):
		return self.market.getLastPrice(assetCode)

	def calTradingCost(self, price, amount, op):
		if op==0:
			return price*amount
		else: 
			return -price*amount

	def calServiceCharge(self, fee, rate=0.001):
		if not self.isCharged:
			return 0
		return fee*rate