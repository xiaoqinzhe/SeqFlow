# -*- coding: utf-8 -*-
from __future__ import unicode_literals
class BasicDecision:
	def __init__(self):
		self.lossThreshold=500

	def decide(self, trader):
		return None, None

	def controlLoss(self, trader, order):
		price = trader.getLastPrice(order.assetCode)
		if (order.curPrice-price)*order.amount>=self.lossThreshold: return True
		return False

class SimpleDecision(BasicDecision):
	def __init__(self, code):
		super(SimpleDecision, self).__init__()
		self.assetCode=code
		self.buyThreshold=0.01
		self.lossThreshold=600

	def decide(self, trader):
		closeOrder, openOrders=[], []
		for order in trader.orders:
			if(self.controlLoss(trader, order)): closeOrder.append(order.id)
		actualmoney=trader.curmoney+0
		price=trader.getLastPrice(self.assetCode)
		if self.judgeBuy(trader, self.assetCode):
			n=actualmoney//(price)
			if n: openOrders.append([self.assetCode, 0, n/2])
		return closeOrder, openOrders

	def judgeBuy(self, trader, code):
		prices=trader.market.getNPrices(code, 2)
		if len(prices)<2: return False
		if (prices[1]-prices[0])>self.buyThreshold: return True
		return False

class RnnDecision(BasicDecision):
	def __init__(self):
		super(RnnDecision, self).__init__()
		self.optionCode=code
		self.buyThreshold=0.005
		self.sellThreshold=0.01
		self.lossThreshold=600
		self.oldres=None
		self.model=RnnModel()

	def decide(self, optionTrade):
		super(RnnDecision, self).decide(optionTrade)
		closeOrder, openOrders=[], []
		judres=self.judge(self.trade.etf)

		for order in self.trade.orders:
			if(judres<0 or self.controlLoss(order)): closeOrder.append(order.id)
				
		if judres > 0:
			actualmoney=self.trade.curmoney+0
			option=self.trade.getOptionFCode(self.optionCode)
			n=actualmoney//(option.getLastPrice()*OptionOrder.hand2gu)
			if n: openOrders.append([self.optionCode, 0, n/2])

		return closeOrder, openOrders

	def judge(self, etf):
		if len(etf.info)<self.model.n_seq: return 0
		seq=[[]]
		for i in range(len(etf.info)-self.model.n_seq, len(etf.info)): 
			seq[0].append([etf.info[i].closingPrice, etf.info[i].topPrice, etf.info[i].bottomPrice, etf.info[i].turnover, etf.info[i].volumn])
		res = self.model.predictV(seq)
		if self.oldres==None: self.oldres=etf.getLastPrice()
		#print(res[0][0], self.oldres)
		old=etf.getLastPrice()
		#old=self.oldres
		print(old, res[0][0])
		self.oldres=res[0][0]
		if res[0][0]-old>self.buyThreshold: return 1
		elif old-res[0][0]>self.sellThreshold: return -1

		# if len(option.info)<2: return False
		# now=low=len(option.info)-1
		# while(low>0 and option.info[low].closingPrice>option.info[low-1].closingPrice):
		# 	low-=1
		# if low==0: return False
		# if (option.info[now].closingPrice-option.info[low].closingPrice)>=self.buyThreshold: return True
		return 0