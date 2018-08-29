# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams['font.sans-serif'] = ['SimHei']

   #data recorder in trade procedure
class TradeRecorder:
	D=250
	RF=0.03
	def __init__(self):
		self.times=[]                #时间序列
		self.orders=[]               #合约单
		self.asset=None
		self.prices=[]
		self.profits=[]              #日收益
		self.invests=[]              #日投入
		self.roreturns=[]            #日收益率
		self.totalReturns=[]         #累计收益
		self.totalRoreturns=[]       #累计收益率
		self.initmoney=0.0           #初始资金
		self.finalmoney=0.0          #最后资金
		self.tradeDays=0             #交易天数
		self.lots=0                  #合约数
		self.profitTime=0            #盈利个数
		self.lossTime=0              #亏损个数
		self.profitAsLoss=0.0        #盈亏比
		self.totalReturn=0.0         #总收益
		self.roreturn=0.0            #总收益率
		self.annualRoreturn=0.0      #年化总收益率
		self.avgDailyRoreturn=0.0    #平均日收益率
		self.dailyVolatility=0.0     #日波动率
		self.annualVolatility=0.0    #年化波动率
		self.sharpeRatio=0.0	     #夏普率
		self.maxDrawdown=0.0         #最大回撤率

	def setAsset(self, asset):
		self.asset=asset
		for info in asset.info: self.prices.append(info.closingPrice)

	def addPrice(self, price):
		self.prices.append(price)
	
	def addOrder(self, order):
		self.orders.append(order)

	def addProfit(self, time, profit, invest):
		self.times.append(time)
		self.profits.append(profit)
		self.invests.append(invest)
		rate=0.0
		if invest: rate=profit/invest
		self.roreturns.append(rate)
		if len(self.times)>1: self.totalRoreturns.append(rate+self.totalRoreturns[len(self.times)-2])
		else: self.totalRoreturns.append(rate)
		if len(self.times)>1: self.totalReturns.append(profit+self.totalReturns[len(self.times)-2])
		else: self.totalReturns.append(profit)

	def eval(self):
		if self.lossTime: self.profitAsLoss=self.profitTime/self.lossTime
		else: self.profitAsLoss=9999999
		self.totalReturn=self.finalmoney-self.initmoney
		self.roreturn=self.totalReturn/self.initmoney
		self.annualRoreturn=np.power((self.roreturn+1), TradeRecorder.D/self.tradeDays)-1
		self.avgDailyRoreturn=np.mean(self.roreturns)
		self.dailyVolatility=np.sqrt(np.var(self.roreturns))
		self.annualVolatility=np.sqrt(TradeRecorder.D)*self.dailyVolatility
		if self.annualVolatility: self.sharpeRatio=(self.annualRoreturn-TradeRecorder.RF)/self.annualVolatility
		if self.dailyVolatility: self.sharpeRatio=np.sqrt(TradeRecorder.D)*(self.avgDailyRoreturn-self.RF/self.D)/self.dailyVolatility
		   #max draw down
		maxdiff,x,y=0,0,0
		for i in range(len(self.totalReturns)-1):
			for j in range(i+1, len(self.totalReturns)):
				diff=self.totalReturns[i]-self.totalReturns[j]
				if diff>maxdiff:
					maxdiff=diff
					x, y = i, j
		if self.totalReturns[x]: self.maxDrawdown=(maxdiff)/(self.totalReturns[x]+self.initmoney)
		else: self.maxDrawdown=0.0
		
	def showStatistics(self):
		print('初始资金: %f\n' % self.initmoney + \
		'最后资金: %f\n' % self.finalmoney + \
		'交易天数: %d\n' % self.tradeDays + \
		'合约数: %d\n' % self.lots + \
		'盈利个数: %d\n' % self.profitTime + \
		'亏损个数: %d\n' % self.lossTime + \
		'盈亏比: %f\n' % self.profitAsLoss + \
		'总收益: %f\n' % self.totalReturn + \
		'总收益率: %f\n' % self.roreturn + \
		'年化总收益率: %f\n' % self.annualRoreturn + \
		'平均日收益率: %f\n' % self.avgDailyRoreturn + \
		'日波动率: %f\n' % self.dailyVolatility + \
		'年化波动率: %f\n' % self.annualVolatility + \
		'夏普率: %f\n' % self.sharpeRatio + \
		'最大回撤率: %f\n' % self.maxDrawdown + \
		'累计日收益率: %f\n' % self.totalRoreturns[len(self.times)-1])
		plt.figure()
		plt.plot(self.profits)
		# print(self.profits)
		plt.title('日收益')
		a,b=plt.subplots()
		b.plot(self.totalReturns, label='profit', color='b')
		b.legend(loc=2)
		if len(self.prices)>0:
			c=b.twinx()
			c.plot(self.prices, label='price', color='r')
			c.legend(loc=1)
		plt.title('累计收益')
		# plt.figure()
		# plt.plot(self.times, self.roreturns)
		# plt.title('日收益率')
		# plt.figure()
		# plt.plot(self.times, self.totalRoreturns)
		# plt.title('累计日收益率')
		plt.show()

	def showOrders(self):
		if not self.orders: return
		print(self.orders[0].str_title)
		for order in self.orders:
			print(order.toString())

	def showDailyProfits(self):
		s=0
		for i in range(len(self.times)):
			s+=self.profits[i]
			print(self.times[i], self.profits[i], self.invests[i], self.roreturns[i])
		print('total profit: %f\n' % s)
