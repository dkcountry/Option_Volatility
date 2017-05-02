import numpy as np 
import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import csv

'''open csv file with list of tickers'''
def getUniverse(csvfile):
	with open(csvfile,'rb') as f:
		reader = csv.reader(f)
		data = [x[0] for x in reader][1:]
	return data

'''Convert datetime type into string'''
def formatDate(date):
	return date.strftime('%Y%m%d')

'''Return panda series of tickers with earnings on input date in string format'''
def getNames(strDate):
	r = requests.get("https://biz.yahoo.com/research/earncal/" +strDate+".html")
	soup = BeautifulSoup(r.text, "html.parser")
	data = soup.find_all('td')
	data = [x.find_all('a',href = True) for x in data]
	if len(data) == 0:
		return pd.Series()
	data = [str(x[0]) for x in data if len(x) != 0]
	names = []
	for string in data:
		string = string[::-1]
		entry = ''
		i = 4
		if string[i] == '>':
			proceed = False
		else:
			proceed = True
		while(proceed):
			entry = entry + string[i]
			i = i + 1
			if string[i] == '>':
				proceed = False
			else:
				proceed = True
		if (len(entry) != 0) and (str.isupper(entry)):
			names.append(entry[::-1])
	return pd.Series(strDate,index = np.unique(names))

'''Returns panda df with earning dates for symbols given within datetime range'''
def getDates(universe,begin,end):
	if begin >= end:
		print "Error: starting date must be prior to end date"
		return pd.DataFrame()
	maxDates = 10
	columns = ['ern' + str(x) for x in range(1,maxDates+1)]
	ernData = pd.DataFrame(index = universe,columns = columns)
	date = end
	while(date != begin):
		data = getNames(formatDate(date))
		if data.empty is False:
			for sym in data.index:
				if sym in ernData.index:
					i = 0
					while(i < maxDates):
						if pd.isnull(ernData.loc[sym].iloc[i]):
							ernData.loc[sym].iloc[i] = data.loc[sym]
							i = maxDates
						else:
							i = i+1
			
		date = date - datetime.timedelta(days = 1)
	return ernData

if __name__ == "__main__":
	names = getUniverse('sp500.csv')
	end = datetime.date(2017,1,22)
	begin = datetime.date(2014,1,1)