# -*- coding: utf-8 -*-
from __future__ import unicode_literals
'''
seqdb is used to get sequence dataset
'''

import numpy as np
import pandas as pd
import datetime
import matplotlib.pyplot as plt
from config.config import configs
from dataproc.common import time_filter
import os

seqpath = configs['data_path'] + "seq/"
# stock data info
stock_column_names = ["date", "opening", "high", "low", "closing", "volume", "turnover"]

def get_seq(filename, column_indexes = None, start_time=None, end_time=None):
	"""
	get sequence data from csv format file filename (path)
	:param filename:
	:param column_indexes:
	:param start_time:
	:param end_time:
	:return:
	"""
	path = seqpath + filename
	df = pd.read_csv(path)
	# df["date"]=pd.to_datetime(df['date'])
	df=df.values
	if start_time: df = time_filter(df, start_time, end_time)
	if column_indexes is None: column_indexes = [0]
	df = df[:, column_indexes]
	return df
# get stock data
# name : ["date", "opening", "high", "low", "closing", "volume", "turnover"]
def get_stock(filename, column_names=stock_column_names, start_time=None, end_time=None):
	indexes = [stock_column_names.index(name) for name in column_names]
	return get_seq("stocks/" + filename, indexes, start_time, end_time)

def get_all_stock_codes():
	files = []
	path = seqpath+"stocks/"
	for file in os.listdir(path):
		if os.path.isfile(path+file):
			files.append(file.split('.')[0])
	return files

def get_sunspot(start_time=None, end_time=None):
	return get_seq('sunspot/monthly-sunspot-number-zurich-17.csv', [1], start_time, end_time)

def get_temperature():
	return get_seq('temperature/daily-minimum-temperatures-in-me.csv', [0])

def get_house_power_consumption(params=None):
	path = '../data/house_consumption/household_power_consumption.txt'
	df = pd.read_csv(path, delimiter=';', na_values='?')
	datasize=16000
	print(df.columns)
	print(df.dtypes)
	# print(df.head())
	# print(df.describe())
	plt.plot(df.loc[:datasize,'Global_active_power']*1000/60 - df.loc[:datasize,'Sub_metering_1'] - df.loc[:datasize,'Sub_metering_2'] - df.loc[:datasize,'Sub_metering_3'])
	plt.show()
	df=df.values
	return df
