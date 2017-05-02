import numpy as np 
import pandas as pd
import math
import matplotlib.pyplot as plt
import datetime
import quandl
import csv

'''retrieve daily adj. close data for a single name from quandl'''
def getData(sym):
	data = quandl.get("WIKI/" + sym)[['Adj. Close']][::-1][:1500]
	return data

'''daily percent return'''
def dailyReturn(data):
	rv = pd.Series(index = data.index)
	for i in range(len(data.index)-1):
		rv.iloc[i] = round((data.iloc[i]['Adj. Close'] - 
			data.iloc[i+1]['Adj. Close'])/data.iloc[i+1]['Adj. Close'] * 100,3)
	return rv.dropna()

'''Get 5,10,21 censored vol and 63, 126 day uncensored vol'''
def getRealizedVol(cenVol,uncenVol):
	rv = pd.DataFrame(index = cenVol.index,columns = [5,10,21,63,126])
	for i in range(len(cenVol.index) -126):
		rv.iloc[i][5] = np.sqrt(np.average(cenVol.iloc[i:i+5]**2))*16
		rv.iloc[i][10] = np.sqrt(np.average(cenVol.iloc[i:i+10]**2))*16
		rv.iloc[i][21] = np.sqrt(np.average(cenVol.iloc[i:i+21]**2))*16
		rv.iloc[i][63] = np.sqrt(np.average(uncenVol.iloc[i:i+63]**2))*16
		rv.iloc[i][126] = np.sqrt(np.average(uncenVol.iloc[i:i+126]**2))*16
	return rv

'''vol chart - use datetime dates as inputs'''
def plotVol(vol,begin,end):
	begin = pd.Timestamp(begin)
	end = pd.Timestamp(end)
	vol = vol[(vol.index <= end) & (vol.index >= begin)]
	plt.plot(vol[5])
	plt.plot(vol[10])
	plt.plot(vol[21])
	plt.plot(vol[63])
	plt.yticks(range(0,65,5))
	plt.ylim([0,60])
	plt.grid()
	plt.show()


def getERN(csvfile):
	data = pd.read_csv(csvfile,index_col = 0)
	return data

def getSymErnData(sym,erndata):
	if sym in erndata.index:
		print "Earnings data found"
		return erndata.loc[sym].dropna()
	else:
		print 'WARNING: No earnings data for ' + str(sym)
		return pd.Series()


def cenMoves_ernMoves(stockdata,sym_erndata):
	rv = pd.Series(index = stockdata.index)
	for i in range(len(data.index)-1):
		rv.iloc[i] = round((data.iloc[i]['Adj. Close'] - 
			data.iloc[i+1]['Adj. Close'])/data.iloc[i+1]['Adj. Close'] * 100,3)
	cv = rv.dropna()
	ernindex = []
	ernMove = []
	if sym_erndata.empty:
		print "WARNING: Returning uncensored data"
		return cv, pd.Series()
	for date in sym_erndata:
		date = datetime.datetime.strptime(str(int(date)),'%Y%m%d')
		d1 = pd.Timestamp(date - datetime.timedelta(days = 1))
		d2 = pd.Timestamp(date)
		d3 = pd.Timestamp(date + datetime.timedelta(days = 1))
		move = [0]
		for x in [d1,d2,d3]:
			if x in stockdata.index:
				move.append(stockdata[x])
				cv = cv.drop(x)
		ernindex.append(d2)
		p = pd.Series(np.absolute(move))
		p = p[p == max(p)].index[0]
		ernMove.append(move[p])
	ernMoves = pd.Series(ernMove,index = ernindex)
	return cv, ernMoves


if __name__ == "__main__":
	sym = 'PNRA'
	data = getData(sym)
	stockdata = dailyReturn(data)
	ern = getERN('updated_ernData.csv')
	symERN = getSymErnData(sym,ern)
	cenReturns, ernMoves = cenMoves_ernMoves(stockdata,symERN)
	vol = getRealizedVol(cenReturns,stockdata)
	end = datetime.date(2017,1,17)
	begin = datetime.date(2015,1,1)
	plotVol(vol,begin,end)