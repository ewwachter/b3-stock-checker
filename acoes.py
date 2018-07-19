#!/usr/bin/env python

import matplotlib.pyplot as plt
import matplotlib.dates as dates
import matplotlib.cbook as cbook
import numpy as np
import time
import sys
import requests

#################################################
####fill this part with your API and tickers#####
#################################################
API_KEY = ""

fiis=[
	# "xpml11.sa",
	# "cbop11.sa",
	"hglg11.sa",
	"hfof11.sa",
	"rbbv11.sa",
	"jsre11.sa",
	# "htmx11.sa",
	# "visc11.sa",
	# "knri11.sa",
	# "ggrc11.sa",
	# "brcr11.sa",
	# "hgre11.sa",
	# "mall11.sa",
	]
#################################################
#################################################
URL_API="https://www.alphavantage.co/query?" + "apikey="+API_KEY

function=["TIME_SERIES_DAILY",
	"TIME_SERIES_WEEKLY",
	"TIME_SERIES_INTRADAY&interval=1min",
	"",
	"",]


opens = "1. open"
high = "2. high"
low = "3. low"
close = "4. close"
vol = "5. volume"

def get_json(addr):
	while True:
		#get url
		r = requests.get(addr)

		#get response in json format
		try:
			data = r.json()
		except ValueError:
			print ("Decoding JSON has failed")
			print(r.text)
			time.sleep(10)
		else:
			return data

		time.sleep(30)


def get_series(ticker,period,response_str):
	addr = URL_API + "&function=" + period
	addr = addr + "&symbol=" + ticker
	print ("addr:", addr)

	data = get_json(addr)
	# print (data)

	try:
		time_series = data[response_str]
	except KeyError:
		# except KeyError as error:
		print ("problem with this ticker")
		print (data)
		return 0

	# return data
	return time_series
	# i=0
	# for time in time_series:
	# 	# lala = time["4. close"]
	# 	# print (str(i) + ":: "+ str(lala))
	# 	print (str(i) + ":: "+ str(time))
	# 	i+=1

if len(sys.argv) <= 1:
	print ("usage: ", sys.argv[0], " ncols")
	exit()

ncols = sys.argv[1]
print ("ncols:", ncols)

# months = dates.MonthLocator()   # every month
# days = dates.DayLocator()  # every day
monthsFmt = dates.DateFormatter('%d/%m')

# fig, ax = plt.subplots(nrows=len(fiis), ncols=1)
fig, ax = plt.subplots(nrows=int((len(fiis))/2)+1, ncols=int(ncols))

print("leng fiis:"+str(len(fiis)))
print("nrows:"+str(int((len(fiis))/2)+1)+" ncols:"+str(ncols))

line=0
col=0
for i in fiis:
	ax[line][col].set_title(i)

	if(line>=int(len(fiis)/2)):
		col+=1
		line=0
	else:
		line+=1

plt.show(block=False)

while(1):
	line=0
	col=0
	for i in fiis:
		print(i)
		dict_time_series = get_series(i,function[0],"Time Series (Daily)")

		high_list = list();
		date_list_format = list();
		if(dict_time_series != 0):
			#get list of dates
			date_list = dict_time_series.keys()
			# print(date_list)
			# print ("=================================")

			#sort response by date
			date_list = sorted(date_list)
			# print(date_list)
			# print ("=================================")

			#creates list with the high values on the same order as sorted date_list
			# i=0
			for x in date_list:
				# print (str(i) + ":: "+ str(x))
				# print (dict_time_series[x][high])
				high_list.append(float(dict_time_series[x][high]))
				date_list_format.append(np.datetime64(x))
				# i+=1

			# for i in range(len(date_list)-30,len(date_list)):
			# 	print(date_list[i] + ": " + str(high_list[i]))

			####################################################
			#display graph
			####################################################

			ax[line][col].plot(date_list_format[70:100], high_list[70:100])
			# ax[line][col].plot(date_list_format[93:100], high_list[93:100])

			# format the ticks
			# ax[line][col].xaxis.set_major_locator(months)
			ax[line][col].xaxis.set_major_formatter(monthsFmt)
			# ax[line][col].xaxis.set_minor_locator(days)

			#enable grid
			ax[line][col].grid(True)

			# format the ticks
			# ax[line][col].xaxis.set_major_formatter(dates.DateFormatter('%d.%m.%Y'))

			# rotates and right aligns the x labels, and moves the bottom of the
			# axes up to make room for them
			# fig = plt.figure()
			# fig.autofmt_xdate()
			# plt.xticks(rotation=45)
		
		ax[line][col].set_title(i)
		
		print("line:"+str(line)+" col:"+str(col))

		if(line>=int(len(fiis)/2)):
			col+=1
			line=0
		else:
			line+=1

		time.sleep(30)

	# fig.tight_layout()
	plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)

	#display the figure
	fig.canvas.draw()
	fig.canvas.flush_events()
