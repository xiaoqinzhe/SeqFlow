# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from dataproc.seq import seqdb

class VMarket:
	def __init__(self, st=None, et=None, codes=None):
		self.curtime=st
		self.endtime=et
		self.codes=codes
		self.assets={}
		self.endFlag=False
		self.initData()

	def initData(self):
		if self.codes is None:
			self.codes = seqdb.get_all_stock_codes()
		self.curIndexes = {}
		l=0
		for i, code in enumerate(self.codes):
			self.assets[code] = seqdb.get_stock(code+".csv", start_time=self.curtime, end_time=self.endtime)
			self.curIndexes[code] = 0
			if i:
				print(l, len(self.assets[code]))
				for i in range(len(self.assets[self.codes[0]])): 
					print(self.assets[self.codes[0]][i,0], self.assets[code][i,0])
				assert l==len(self.assets[code]), "stocks length is not equal!"
			l=len(self.assets[code])
			print(l)
		print(len(self.codes))
		if self.curtime is None: 
			self.curtime = self.assets[self.codes[0]][0][0]
		self.curi=0

	def updateIndex(self):
		pass

	def getNPrices(self, code, n):
		s = self.curi-n+1
		if self.curi-n+1 < 0:
			s = 0
		return self.assets[code][s:self.curi+1,4]

	def nextState(self):
		self.curi+=1
		if self.curi==len(self.assets[self.codes[0]]): 
			self.endFlag=True
			self.curi-=1

	def getLastPrice(self, code):
		return self.assets[code][self.curi, 4]