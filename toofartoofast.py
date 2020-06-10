import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
import yfinance as yfin
import time

spy = yfin.Ticker("SPY")

#stock info 
#print(spy.info)
#stock info for ytd 

time.sleep(5)

ytd = spy.history(start="2019-01-01")
ytd = ytd[["Close", "Volume"]]
# print(ytd)

#stock info for 2006-2009
#Great Recession = gr
gr = spy.history(start="2007-01-01",end="2012-01-01")
gr = gr[["Close", "Volume"]]

ytd["SMA50"] = ytd['Close'].rolling(window=50).mean()
ytd["SMA200"] = ytd['Close'].rolling(window=200).mean()

gr["SMA50"] = gr['Close'].rolling(window=50).mean()
gr["SMA200"] = gr['Close'].rolling(window=200).mean()

'''
#plotting ytd recovery timeline
ytd["Close"].plot(figsize=(16,9))

plt.xlabel("date")
plt.ylabel("price (dollars)")
plt.title("SPY patterns from 2019 to present")

plt.plot(ytd['SMA50'], 'g--', label="SMA50")
plt.plot(ytd['SMA200'], 'r--', label="SMA200")
plt.plot(ytd['Close'], label="Close")
plt.legend()
plt.show()
'''

'''
#plotting great recession recovery timeline
gr["Close"].plot(figsize=(16,9))

plt.xlabel("date")
plt.ylabel("price (dollars)")
plt.title("SPY patterns from 2007 to 2012")

plt.plot(gr['SMA50'], 'g--', label="SMA50")
plt.plot(gr['SMA200'], 'r--', label="SMA200")
plt.plot(gr['Close'], label="Close")
plt.legend()
plt.show()
'''

# finding the largest pre-recession values for 2008 and 2020
gr_high = gr["Close"].max()
ytd_high = ytd["Close"].max()

#finding their corresponding dates
ytd_high_date = ytd["Close"].idxmax()
ytd_current_date = ytd["Close"].tail(1).idxmin()

#calculating how much the SPY has fallen (percentage-wise)
#from pre-recession highs 
ytd_percentlost = ytd_high - ytd["Close"].tail(1)

#calculating the 2020 recovery time (# of days since highest value)
recoverytime = ytd_high_date - ytd_current_date

#using recovery time to create new dataframe plotting great recession recovery
#timeline against 2020 recovery timeline
gr_high_date = gr["Close"].idxmax()
gr_current_date = gr_high_date - recoverytime

gr_recovery = gr[gr_high_date:gr_current_date]
ytd_recovery = ytd[ytd_high_date:ytd_current_date]

#creating new dataframe that overlays both results
overlay = pd.DataFrame(columns=["2008", "2020"])

overlay["2020"] = ytd_recovery["Close"].reset_index(drop=True) 
overlay["2008"] = gr_recovery.reset_index(drop=True)

#dividing both columns by their respective highs to create percentage graph
overlay["2020"] = overlay["2020"] / ytd_high
overlay["2008"] = overlay["2008"] / gr_high

#plotting overlay recession recovery timeline
overlay.plot(figsize=(16,9))

plt.xlabel("days from pre-recession high")
plt.ylabel("percentage fallen (percentage=1 represents highest value)")
plt.title("SPY recovery in 2008 and 2020 overlayed")

#plt.plot(gr['SMA50'], 'g--', label="SMA50")
#plt.plot(gr['SMA200'], 'r--', label="SMA200")
plt.plot(overlay['2008'], label="2008 recovery")
plt.plot(overlay['2020'], label="2020 recovery")
plt.legend()
plt.show()


