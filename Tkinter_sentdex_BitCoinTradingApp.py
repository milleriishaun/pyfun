# Intermediate sendex Tkinter tutorial series 29 vids(~10mins each)
# Going through this to learn proper class/function management
# also using matplotlib
# create a Tkinter BitCoin tracker

# So far, this program is a live tkinter app, with multiple pages, and live graph

# FOUNDATION FOR THE APP BELOW
import tkinter as tk
# like css for tkinter
from tkinter import ttk

# get matplotlib for our graphs
import matplotlib
# this is the backend of matplotlib... important so everything works
matplotlib.use("TkAgg")
# get canvas for graph to sit on and navbar for forward/back/zoom
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# make sure to draw figures
# from matplotlib.figure import Figure

# import the animation from matplotlib
import matplotlib.animation as animation
from matplotlib import style
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
from matplotlib.finance import candlestick_ohlc

# now we have to use these modules to manage the datasets/limiting data
# tikc data has all the buys and sells,
# want to have open high/open low candlesticks to make sense
# we want to be able to modify the data... so impor these modules
import urllib
import json

# data manipulation
import pandas as pd
# number crunching
import numpy as np

darkColor = '#183A54'
lightColor = '#00A3E0'

SMALL_FONT = ("Verdana", 8)
NORM_FONT = ("Verdana", 10)
LARGE_FONT = ("Verdana", 12)

# add a style for the graph
style.use("ggplot")

# display of the graph is hard to configure
f = plt.figure()
# add a subplot to this figure
# a = f.add_subplot(111)
# add the plot point data (x[], y[])
# a.plot([1,2,3,4,5,6,7,8], [5,6,1,3,8,9,3,5]) # not using this again
# we want to clear the data, so it isn't just adding graphs up and taking RAM



exchange = "Bitfinex"
# we need to add an indicator counter, indicator updates the part even while
# the graph only loads every 10 seconds
# force an update
datCounter = 9000
programName = "bitfinex"

# default graph data/candles
reSampleSize = "15Min"
dataPace = "tick"
candleWidth = 0.008

# indicator defaults
topIndicator = "none"
middleIndicator = "none"
bottomIndicator = "none"
# allow user to get an infinite amount of SMA/EMA
SMAs = []
EMAs = []

# use the constant for the chart Load, default is True
chartLoad = True

# this is so that the data can include different panes, for late adjustments
paneCount = 1

def tutorial():
    # def leavemini(what):
        # what.destroy()
    
    def page2():
        tut.destroy()
        tut2 = tk.Tk()

        def page3():
            tut2.destroy()
            tut3 = tk.Tk()

            tut3.wm_title("Part 3!")

            label = ttk.Label(tut3, text="Part 3", font=NORM_FONT)
            label.pack(side="top", fill="x", pady=10)
            B1 = ttk.Button(tut3, text="Done!", command=tut3.destroy)
            B1.pack()
            tut3.mainloop()

        tut2.wm_title("Part 2!")

        label = ttk.Label(tut2, text="Part 2", font=NORM_FONT)
        label.pack(side="top", fill="x", pady=10)
        B1 = ttk.Button(tut2, text="Next", command=page3)
        B1.pack()
        tut2.mainloop()

    tut = tk.Tk()
    tut.wm_title("Tutorial")
    label = ttk.Label(tut, text="What do you need help with?", font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)

    B1 = ttk.Button(tut, text = "Overview of the application", command=page2)
    B1.pack()

    B2 = ttk.Button(tut, text = "How do I trade with this client?", command=lambda: popupmsg("Not yet completed"))
    B2.pack()

    # How do indicators work
    # How do I trade with that API
    # questions like how do I connect to that API on that Exchange
    B3 = ttk.Button(tut, text = "Indicator Questions/Help", command=lambda: popupmsg("Not yet complete"))
    B3.pack()

    tut.mainloop()

# note that chartLoad is animation... and algorithmic trading
# and eventually we will have to create a headless version, which doesn't have a GUI
# The reason is to not have to update graph every time for automated trading
# run on a cloud server like digital ocean, can't have a GUI
def loadChart(run):
    global chartLoad
    if run == "start":
        charLoad = True



# MIDDLE INDICATOR
def addMiddleIndicator(what):
    # this is so that there is no 30 sec waiting time til update
    # we need it to update immediately
    global middleIndicator
    global datCounter
    
    # if watching tick data, don't need to watch RSI, etc... so popup
    if dataPace == "tick":
        popupmsg("Indicators in Tick Data not available. Choose 1 minute tf if you want short term.")

    # this is for the sma
    if what != "none":
        # is the indicator currently none?
        if middleIndicator == "none":
            # if user wants to do a simple moving avg
            if what == "sma":
                midIQ = tk.Tk()
                midIQ.wm_title("Periods?")
                label = ttk.Label(midIQ, text="Choose how many periods you want your SMA to be.")
                label.pack(side="top", fill="x", pady=10)
                e = ttk.Entry(midIQ)
                e.insert(0, 10)
                e.pack()
                e.focus_set()

                def callback():
                    global middleIndicator
                    global datCounter

                    # this says any interval is good
                    middleIndicator = []
                    periods = (e.get())
                    group = []
                    group.append("sma")
                    group.append(int(periods))
                    middleIndicator.append(group)
                    datCounter = 9000
                    print("middle indicator set to: ", middleIndicator)
                    midIQ.destroy()

                b = ttk.Button(midIQ, text="Submit", width=10, command=callback)
                b.pack()
                tk.mainloop()

            # if user wants to do a simple moving avg
            if what == "ema":
                midIQ = tk.Tk()
                midIQ.wm_title("Periods?")
                label = ttk.Label(midIQ, text="Choose how many periods you want your EMA to be.")
                label.pack(side="top", fill="x", pady=10)
                e = ttk.Entry(midIQ)
                e.pack()
                e.focus_set()

                def callback():
                    global middleIndicator
                    global datCounter

                    middleIndicator = []
                    periods = (e.get())
                    group = []
                    group.append("ema")
                    group.append(int(periods))
                    middleIndicator.append(group)
                    datCounter = 9000
                    print("middle indicator set to: ", middleIndicator)
                    midIQ.destroy()

                b = ttk.Button(midIQ, text="Submit", width=10, command=callback)
                b.pack()
                tk.mainloop()  


        else:
            if what == "sma":
                midIQ = tk.Tk()
                midIQ.wm_title("Periods?")
                label = ttk.Label(midIQ, text="Choose how many periods you want your SMA to consider.")
                label.pack(side="top", fill="x", pady=10)
                e = ttk.Entry(midIQ)
                e.insert(0, 10)
                e.pack()
                e.focus_set()

                def callback():
                    global middleIndicator
                    global datCounter

                    # this says not any interval is good
                    # middleIndicator = []
                    periods = (e.get())
                    group = []
                    group.append("sma")
                    group.append(int(periods))
                    middleIndicator.append(group)
                    datCounter = 9000
                    print("middle indicator set to: ", middleIndicator)
                    midIQ.destroy()

                b = ttk.Button(midIQ, text="Submit", width=10, command=callback)
                b.pack()
                tk.mainloop()

            # if user wants to do a simple moving avg
            if what == "ema":
                midIQ = tk.Tk()
                midIQ.wm_title("Periods?")
                label = ttk.Label(midIQ, text="Choose how many periods you want your EMA to be.")
                label.pack(side="top", fill="x", pady=10)
                e = ttk.Entry(midIQ)
                e.pack()
                e.focus_set()

                def callback():
                    global middleIndicator
                    global datCounter

                    # middleIndicator = []
                    periods = (e.get())
                    group = []
                    group.append("ema")
                    group.append(int(periods))
                    middleIndicator.append(group)
                    datCounter = 9000
                    print("middle indicator set to: ", middleIndicator)
                    midIQ.destroy()

                b = ttk.Button(midIQ, text="Submit", width=10, command=callback)
                b.pack()
                tk.mainloop() 

    else:
        middleIndicator = "none"

# TOP INDICATOR
def addTopIndicator(what):
    # this is so that there is no 30 sec waiting time til update
    # we need it to update immediately
    global topIndicator
    global datCounter
    
    # if watching tick data, don't need to watch RSI, etc... so popup
    if dataPace == "tick":
        popupmsg("Indicators in Tick Data not available.")
    
    # force the update to remove the indicator from the graph
    elif what == "none":
        topIndicator = what
        datCounter = 9000

    elif what == "rsi":
        # ask the user a period of time first before get RSI applied
        # (generally 14 day interval when applied, but we want to allow user to choose interval)
        rsiQ = tk.Tk()
        rsiQ.wm_title("Periods?")
        label = ttk.Label(rsiQ, text="Choose how many periods you want each RSI calculation to consider.")
        label.pack(side="top", fill="x", pady=10)

        e = ttk.Entry(rsiQ)
        # just put in a default if someone doesn't know
        e.insert(0, 14)
        e.pack()
        e.focus_set()

        def callback():
            global topIndicator
            global datCounter

            periods = (e.get())
            group = []
            group.append("rsi")
            group.append(periods)

            topIndicator = group
            datCounter = 9000
            # print to the console
            print("Set top indicator to ", group)
            # close the window once entered+callback
            rsiQ.destroy()

        # button configging
        b = ttk.Button(rsiQ, text="Submit", width=10, command=callback)
        b.pack()
        tk.mainloop()

    # there's 3 main values for macd that people use, but he forgets
    elif what == "macd":
        # global topIndicator
        # global datCounter
        topIndicator = "macd"
        datCounter = 9000



# add the BOTTOM INDICATOR
def addBottomIndicator(what):
    # this is so that there is no 30 sec waiting time til update
    # we need it to update immediately
    global bottomIndicator
    global datCounter
    
    # if watching tick data, don't need to watch RSI, etc... so popup
    if dataPace == "tick":
        popupmsg("Indicators in Tick Data not available.")
    
    # force the update to remove the indicator from the graph
    elif what == "none":
        bottomIndicator = what
        datCounter = 9000

    elif what == "rsi":
        # ask the user a period of time first before get RSI applied
        # (generally 14 day interval when applied, but we want to allow user to choose interval)
        rsiQ = tk.Tk()
        rsiQ.wm_title("Periods?")
        label = ttk.Label(rsiQ, text="Choose how many periods you want each RSI calculation to consider.")
        label.pack(side="top", fill="x", pady=10)

        e = ttk.Entry(rsiQ)
        # just put in a default if someone doesn't know
        e.insert(0, 14)
        e.pack()
        e.focus_set()

        def callback():
            global bottomIndicator
            global datCounter

            periods = (e.get())
            group = []
            group.append("rsi")
            group.append(periods)

            bottomIndicator = group
            datCounter = 9000
            # print to the console
            print("Set bottom indicator to ", group)
            # close the window once entered+callback
            rsiQ.destroy()

        # button configging
        b = ttk.Button(rsiQ, text="Submit", width=10, command=callback)
        b.pack()
        tk.mainloop()

    # there's 3 main values for macd that people use, but he forgets
    elif what == "macd":
        # global bottomIndicator
        # global datCounter
        bottomIndicator = "macd"
        datCounter = 9000







def changeTimeFrame(tf):
    global dataPace
    global datCounter
    if tf == "7d" and reSampleSize == "1Min":
        popupmsg("Too much data chosen, choose a smaller time frame or higher OHLC Interval")
    else:
        dataPace = tf
        datCounter = 9000

# size of the bar, and width of the candle
def changeSampleSize(size, width):
    global reSampleSize
    global datCounter
    global candleWidth
    if dataPace == "7d" and reSampleSize == "1Min":
        popupmsg("Too much data chosen, choose a smaller time frame or higher OHLC Interval")
    elif dataPace == "tick":
        popupmsg("You're currently viewing tick data, not OHLC.")
    else:
        reSampleSize = size
        datCounter = 9000
        candleWidth = width


def changeExchange(toWhat, pn):
    global exchange
    global datCounter
    global programName

    exchange = toWhat
    programName = pn
    datCounter = 9000


# popupmsg
def popupmsg(msg):
    # mini tkinter instance... notice mainloop
    popup = tk.Tk()
    popup.wm_title("!")
    label = ttk.Label(popup, text=msg, font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Okay", command=popup.destroy)
    B1.pack()
    popup.mainloop()


# need an animation function using matplotlib
# this is our main animation function
# but the animation can update other things too,
# animate function works with matplotlib, but animate can also
# update the tkinter code... even though tkinter has its own update function
# The core of the updates are going to happen in this animation
def animate(i):
    # need a data link
    # use the BTC API... er the BITFINEX API
    # we'll get the last trades(gives us historical data)...
    # (as opposed to ticks which gives us info but not population of a graph right away) 
    # for last trades... can do up to 2000 of the last ones
    # with the info, check which are bids and which are asks
    # This is a generated data set, and the last info was a UNIX timestamp

    # All the below makes the program go too slow and is not live
    # even without this slow code, it is still slow to resize window
    # r = requests.get('https://api.coindesk.com/v1/bpi/historical/close.json?start=2016-03-19&end=2018-03-19', verify=False)
    # real data from few years
    # get the BitCoin Price Index
    # for k, v in r.json()['bpi'].items():
    #     print(k, v)
    # a.clear()
    # a.plot(r.json()['bpi'].keys(), r.json()['bpi'].values())
    
    # refresh rate, and counter
    global refreshRate
    global datCounter


    # just have defaults... slow/fast are the periods... slow reacting and fast reacting
    def computeMACD(x, slow=26, fast=12, location="bottom"):
        values = {"key":1, "prices":x}

        url = "http://seaofbtc.com/api/indicator/macd" # get API
        data = urllib.parse.urlencode(values) # encode the values
        data = data.encode("utf-8")
        req = urllib.request.Request(url, data) # request the url with the data
        resp = urllib.request.urlopen(req) # open the request
        respData = resp.read() # read the data

        newData = str(respData).replace("b", "").replace("[", "").replace("]", "").replace("'", "")

        # far from industry standard here
        split = newData.split("::")

        macd = split[0]
        ema9 = split[1]
        hist = split[2]
        
        # convert this into a list
        macd = macd.split(", ")
        ema9 = ema9.split(", ")
        hist = hist.split(", ")


        # convert from string into a n integer
        macd = [float(i) for i in macd]
        ema9 = [float(i) for i in ema9]
        hist = [float(i) for i in hist]

        # now we want to plot the data
        # it looks cooler to have a filled in histogram
        # use the dates to plot
        if location == "top":
            try:
                a0.plot(OHLC["MPLDates"][fast:], macd[fast:], color = darkColor, lw=2)
                a0.plot(OHLC["MPLDates"][fast:], ema9[fast:], color = lightColor, lw=1)
                a0.fill_between(OHLC["MPLDates"][fast:], hist[fast:], 0, alpha=0.5, facecolor=darkColor, edgecolor=darkColor)
                label = "MACD"
                a0.set_ylabel(label)
            except Exception as e:
                print("Error in computeMACD: ", str(e))
                topIndicator = "none"

        if location == "bottom":
            try:
                a3.plot(OHLC["MPLDates"][fast:], macd[fast:], color = darkColor, lw=2)
                a3.plot(OHLC["MPLDates"][fast:], ema9[fast:], color = lightColor, lw=1)
                a3.fill_between(OHLC["MPLDates"][fast:], hist[fast:], 0, alpha=0.5, facecolor=darkColor, edgecolor=darkColor)
                label = "MACD"
                a3.set_ylabel(label)
            except Exception as e:
                print("Error in computeMACD: ", str(e))
                bottomIndicator = "none"





    #CMBTC API for RSI indicator
    def rsiIndicator(priceData, location="top"):
        if location == "top":
            # dictionary of values
            values = {"key":1, "prices":priceData, "periods":topIndicator[1]}
        if location == "bottom":
            # dictionary of values
            values = {"key":1, "prices":priceData, "periods":bottomIndicator[1]}

        url = "http://seaofbtc.com/api/indicator/rsi"

        data = urllib.parse.urlencode(values)
        data = data.encode("utf-8")

        req = urllib.request.Request(url, data)
        resp = urllib.request.urlopen(req)

        respData = resp.read()

        # newData = respData.decode() # this wasn't working(ideally would use the JSON module...)
        # problem was that it was not a true JSON format... regarding the API itself
        # bad change below because messy, coverts from bytecode to a python list
        newData = str(respData).replace("b", "").replace("[", "").replace("]", "").replace("'", "")
        priceList = newData.split(', ')
        rsiData = [float(i) for i in priceList]

        # nwo actually put the RSI info up
        if location == "top":
            a0.plot_date(OHLC['MPLDates'], rsiData, lightColor, label="RSI")
            datLabel = "RSI("+str(topIndicator[1])+")"
            a0.set_ylabel(datLabel)

        if location == "bottom":
            a3.plot_date(OHLC['MPLDates'], rsiData, lightColor, label="RSI")
            datLabel = "RSI("+str(bottomIndicator[1])+")"
            a3.set_ylabel(datLabel)






    # we need this data to animate tick data only when it is user's choice
    # so only do it when data time frames are included
    if chartLoad:
        if paneCount == 1:
            if dataPace == "tick":
                try:
                    if exchange == "Bitfinex":

                        # full grid size, then starting point of plot, then spans, only 1 row remaining
                        # we can later say it's a 12x4... later we can customize
                        a = plt.subplot2grid((6,4), (0,0), rowspan=5, colspan=4)
                        # sharex means that the zoom will affect with the exact degree
                        # always be aligned with first chart, even when moved around
                        a2 = plt.subplot2grid((6,4), (5,0), rowspan=1, colspan=4, sharex = a)
                        dataLink = "https://api.bitfinex.com/v1/trades/BTCUSD?limit_trades=2000"
                        data = urllib.request.urlopen(dataLink)
                        data = data.read().decode("utf-8")
                        data = json.loads(data)
                        # data = data["btc_usd"] is useless for us

                        data = pd.DataFrame(data)

                        # numpy array converted to numpy's date time format
                        data["datestamp"] = np.array(data["timestamp"]).astype("datetime64[s]")
                        # because we can't pass a numpy array in, we use this tolist
                        allDates = data["datestamp"].tolist()

                        # Buys  
                        buys = data[(data["type"]=="buy")]# changed to match the api response bid is now buy
                        # datestamp
                        # buys["datestamp"]= np.array(buys["timestamp"]).astype("datetime64[s]")
                        # throw it at matplotlib
                        buyDates = (buys["datestamp"]).tolist()

                        sells = data[(data["type"]=="sell")] # changed to match the api response ask is now sell
                        # sells["datestamp"]= np.array(sells["timestamp"]).astype("datetime64[s]")
                        sellDates = (sells["datestamp"]).tolist()

                        # calculate the volume... which is from the JSON
                        volume = data["amount"].apply(float).tolist()

                        # update the graph
                        a.clear()
                        a.plot_date(buyDates, buys["price"], lightColor, label="buys")
                        a.plot_date(sellDates,sells["price"], darkColor, label="sells")

                        # for volume data, specify minimum point, the dat(volume), and the color
                        a2.fill_between(allDates, 0, volume, facecolor = darkColor)

                        # sets the maximum amount of marks... so if a lot of marks, don't let it run over itself
                        a.xaxis.set_major_locator(mticker.MaxNLocator(5))
                        # format how the date actually looks
                        a.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M:%S"))

                        # fix the axes labels
                        plt.setp(a.get_xticklabels(), visible=False)

                        # fix the legend to not cover the data
                        a.legend(bbox_to_anchor=(0, 1.02, 1, 1.02), loc=3,
                                ncol=2, borderaxespad=0)

                        title = "Bitfinex BTC/USD Prices\nLast Price: " + str(data["price"][0])
                        a.set_title(title)
                        priceData = data['price'].apply(float).tolist()


                    if exchange == "Bitstamp":
                        
                        # full grid size, then starting point of plot, then spans, only 1 row remaining
                        # we can later say it's a 12x4... later we can customize
                        a = plt.subplot2grid((6,4), (0,0), rowspan=5, colspan=4)
                        # sharex means that the zoom will affect with the exact degree
                        # always be aligned with first chart, even when moved around
                        a2 = plt.subplot2grid((6,4), (5,0), rowspan=1, colspan=4, sharex = a)
                        dataLink = "https://www.bitstamp.net/api/transactions/"
                        data = urllib.request.urlopen(dataLink)
                        data = data.read().decode("utf-8")
                        data = json.loads(data)
                        # data = data["btc_usd"] is useless for us

                        data = pd.DataFrame(data)

                        # numpy array converted to numpy's date time format
                        # they use date rather than timestamp
                        data["datestamp"] = np.array(data["date"].apply(int)).astype("datetime64[s]")

                        # have to add datestamps, rather than allDates
                        datastamps = data["datestamp"].tolist()

                        # because we can't pass a numpy array in, we use this tolist
                        # allDates = data["datestamp"].tolist()
                        '''
                        # Buys  
                        buys = data[(data["type"]=="buy")]# changed to match the api response bid is now buy
                        # datestamp
                        # buys["datestamp"]= np.array(buys["timestamp"]).astype("datetime64[s]")
                        # throw it at matplotlib
                        buyDates = (buys["datestamp"]).tolist()

                        sells = data[(data["type"]=="sell")] # changed to match the api response ask is now sell
                        # sells["datestamp"]= np.array(sells["timestamp"]).astype("datetime64[s]")
                        sellDates = (sells["datestamp"]).tolist()
                        '''
                        # calculate the volume... which is from the JSON
                        # bitstamp doesn't differentiate the buys versus the sells
                        # change this to get the dat in the list format, because
                        # the data from Bitstamp has different formatting
                        volume = data["amount"].apply(float).tolist()

                        # update the graph
                        a.clear()
                        a.plot_date(datastamps, data["price"], lightColor)
                        # a.plot_date(sellDates,sells["price"], darkColor, label="sells")

                        # for volume data, specify minimum point, the dat(volume), and the color
                        a2.fill_between(datastamps, 0, volume, facecolor = darkColor)

                        # sets the maximum amount of marks... so if a lot of marks, don't let it run over itself
                        a.xaxis.set_major_locator(mticker.MaxNLocator(5))
                        # format how the date actually looks
                        a.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M:%S"))

                        plt.setp(a.get_xticklabels(), visible = False)

                        # use 0 for most recent pricedelivered
                        title = "Bitstamp BTC/USD Prices\nLast Price: " + str(data["price"][0])
                        a.set_title(title)
                        priceData = data['price'].apply(float).tolist()
                        

                    if exchange == "Huobi":
                        try:
                            # full grid size, then starting point of plot, then spans, only 1 row remaining
                            # we can later say it's a 12x4... later we can customize
                            a = plt.subplot2grid((6,4), (0,0), rowspan=6, colspan=4)
                            # sharex means that the zoom will affect with the exact degree
                            # always be aligned with first chart, even when moved around
                            #
                            # took this out because it didn't work
                            # dataLink = ('http://seaofbtc.com/api/basic/price?key=1&tf=1d&exchange='+programName)
                            data = urllib.request.urlopen('http://seaofbtc.com/api/basic/price?key=1&tf=1d&exchange='+programName).read()
                            # data = data.decode() # this decoding is also unnecssary for Huobi
                            # but we do need o search and replace
                            data = data.decode()
                            data = json.loads(data)
                            # data = data["btc_usd"] is useless for us
                            #dont' need pandas to interpret this graphs since 1 axis
                            # data = pd.DataFrame(data)

                            # have to add datestamps, rather than allDates
                            # datastamps = data["datestamp"].tolist()
                            # numpy array converted to numpy's date time format
                            dateStamp = np.array(data[0]).astype("datetime64[s]")
                            # because we can't pass a numpy array in, we use this tolist
                            dateStamp = dateStamp.tolist()

                            # call on pandas for the dataframe
                            df = pd.DataFrame({'Datetime':dateStamp})

                            # assign the price/vol/symbol column
                            df['Price'] = data[1]
                            df['Volume'] = data[2]
                            df['Symbol'] = "BTC/USD"

                            # plot these dates by conversion to MPL
                            df['MPLDate'] = df['Datetime'] #.apply(lambda date: mdates.date2num(date.to_pydatetime()))

                            # Setting the index makes it easier to work in pandas
                            df = df.set_index("Datetime")

                            lastPrice = df["Price"][-1]

                            # This is our x and y
                            a.plot_date(df['MPLDate'][-4500:], df['Price'][-4500:], lightColor, label="price")

                            # sets the maximum amount of marks... so if a lot of marks, don't let it run over itself
                            a.xaxis.set_major_locator(mticker.MaxNLocator(5))
                            # format how the date actually looks
                            a.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M:%S"))

                            title = "Huobi Tick Data\nLast Price: " + str(lastPrice)
                            a.set_title(title)
                            priceData = df['Price'].apply(float).tolist()

                        except Exception as e:
                            print("Failed because of: ", e)
                
                except:
                    datCounter = 9000
                
# this is now NON-tick Graphing
            else:
                # this is so that we don't regenerate data/redraw graph
                if datCounter > 12: # 12 seconds
                    try:
                        if exchange == "Huobi":
                            # basically setting up the subplots, but there is no volume with Huobi so different
                            if topIndicator != "none":
                                a = plt.subplot2grid((6,4), (1,0), rowspan=5, colspan=4)
                                a0 = plt.subplot2grid((6,4), (0,0), rowspan=1, colspan=4, sharex=a)
                            else:
                                a = plt.subplot2grid((6,4), (0,0), rowspan=6, colspan=4)
                        
                        else:
                            if topIndicator != "none" and bottomIndicator != "none":
                                # Main graph
                                a = plt.subplot2grid((6,4), (1,0), rowspan=3, colspan=4)
                                # Volume graph
                                a2 = plt.subplot2grid((6,4), (4,0), rowspan=1, colspan=4, sharex=a)
                                # Bottom Indicator
                                a3 = plt.subplot2grid((6,4), (5,0), rowspan=1, colspan=4, sharex=a)
                                # Top Indicator
                                a0 = plt.subplot2grid((6,4), (0,0), rowspan=1, colspan=4, sharex=a)

                            elif topIndicator != "none":
                                # defactor, we don't have a bottom indicator
                                # Main graph
                                a = plt.subplot2grid((6,4), (1,0), rowspan=4, colspan=4)
                                # Volume graph
                                a2 = plt.subplot2grid((6,4), (5,0), rowspan=1, colspan=4, sharex=a)
                                # Top Indicator
                                a0 = plt.subplot2grid((6,4), (0,0), rowspan=1, colspan=4, sharex=a)

                            elif bottomIndicator != "none":
                                # defactor, we don't have a bottom indicator
                                # Main graph
                                a = plt.subplot2grid((6,4), (0,0), rowspan=4, colspan=4)
                                # Volume graph
                                a2 = plt.subplot2grid((6,4), (4,0), rowspan=1, colspan=4, sharex=a)
                                # Bottom Indicator
                                a3 = plt.subplot2grid((6,4), (5,0), rowspan=1, colspan=4, sharex=a)

                            else:
                                # Main graph
                                a = plt.subplot2grid((6,4), (0,0), rowspan=5, colspan=4)
                                # Volume graph
                                a2 = plt.subplot2grid((6,4), (5,0), rowspan=1, colspan=4, sharex=a)

                        print('http://seaofbtc.com/api/basic/price?key=1&tf='+dataPace+'&exchange='+programName)
                        # normalize the data
                        data = urllib.request.urlopen('http://seaofbtc.com/api/basic/price?key=1&tf='+dataPace+'&exchange='+programName).read()
                        data = data.decode()
                        data = json.loads(data)

                        dateStamp = np.array(data[0]).astype("datetime64[s]")
                        dateStamp = dateStamp.tolist()

                        df = pd.DataFrame({'Datetime':dateStamp})

                        # assign the price/vol/symbol column
                        df['Price'] = data[1]
                        df['Volume'] = data[2]
                        df['Symbol'] = "BTC/USD"
                        # plot these dates by conversion to MPL
                        df['MPLDate'] = df['Datetime'] #.apply(lambda date: mdates.date2num(date.to_pydatetime()))
                        df = df.set_index('Datetime')

                        # we'll need OHLC candlestick info here
                        OHLC = df['Price'].resample(reSampleSize, how="ohlc")
                        OHLC = OHLC.dropna()

                        volumeData = df['Volume'].resample(reSampleSize, how={'volume':'sum'})

                        OHLC["dateCopy"] = OHLC.index
                        OHLC["MPLDates"] = OHLC["dateCopy"] #.apply(lambda date: mdates.date2num(date.to_pydatetime()))

                        # this is after use
                        del OHLC["dateCopy"]

                        volumeData["dateCopy"] = volumeData.index
                        volumeData["MPLDates"] = volumeData["dateCopy"] #.apply(lambda date: mdates.date2num(date.to_pydatetime()))

                        # this is after use
                        del volumeData["dateCopy"]

                        priceData = OHLC['close'].apply(float).tolist()

                        # now let's plot it
                        a.clear()
                        if middleIndicator != "none":
                            for eachMA in middleIndicator:
                                # ewma = pd.stats.moments.ewma
                                if eachMA[0] == "sma":
                                    sma = pd.rolling_mean(OHLC["close"], eachMA[1])
                                    label = str(eachMA[1])+" SMA"
                                    a.plot(OHLC["MPLDates"], sma, label=label)

                                if eachMA[0] == "ema":
                                    ewma = pd.stats.moments.ewma
                                    label = str(eachMA[1])+" EMA"
                                    a.plot(OHLC["MPLDates"], ewma(OHLC["close"], eachMA[1]), label=label)

                            a.legend(loc=0)



                        # relative  strength index
                        if topIndicator[0] == "rsi":
                            rsiIndicator(priceData, "top")
                        elif topIndicator == "macd":
                            try:
                                computeMACD(priceData, location="top")
                            except Exception as e:
                                print(str(e))

                        if bottomIndicator[0] == "rsi":
                            rsiIndicator(priceData, "bottom")
                        elif bottomIndicator == "macd":
                            try:
                                computeMACD(priceData, location="bottom")
                            except Exception as e:
                                print(str(e))
                        

                        # now generate the graph, now that we have to rules
                        # subplot a
                        # list within DataFrame
                        csticks = candlestick_ohlc(a, OHLC[["MPLDates", "open","high", "low","close"]].values, width=candleWidth, colorup=lightColor, colordown=darkColor)
                        a.set_ylabel("price")
                        if exchange != "Huobi":
                            a2.fill_between(volumeData["MPLDates"], 0, volumeData['volume'], facecolor=darkColor)
                            a2.set_ylabel("volume")
                        
                        a.xaxis.set_major_locator(mticker.MaxNLocator(3))
                        # dont need sconds because not tick data, minute is even pushing it
                        a.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M"))

                        if exchange != "Huobi":
                            plt.setp(a.get_xticklabels(), visible = False)

                        if topIndicator != "none":
                            plt.setp(a0.get_xticklabels(), visible = False)

                        if bottomIndicator != "none":
                            plt.setp(a2.get_xticklabels(), visible = False)

                        # get the last element in the list
                        x = (len(OHLC['close']))-1

                        if dataPace == "1d":
                            title = exchange+" 1 Day Data with "+reSampleSize+" Bars\nLast Price: "+str(OHLC['close'][x])
                        if dataPace == "3d":
                            title = exchange+" 3 Day Data with "+reSampleSize+" Bars\nLast Price: "+str(OHLC['close'][x])
                        if dataPace == "7d":
                            title = exchange+" 7 Day Data with "+reSampleSize+" Bars\nLast Price: "+str(OHLC['close'][x])

                        if topIndicator != "none":
                            a0.set_title(title)
                        else:
                            a.set_title(title)
                        
                        # tell us a new graph is made
                        print("New Graph!")
                        datCounter = 0

                    except Exception as e:
                        print('failed in the animate: ', str(e))
                        # if fails, can attempt to go back to the start
                        datCounter = 9000

                else:
                    # only reupdate once >12
                    datCounter += 1
'''
#old animate using info from sampleData file
    pullData = open("sampleData.txt", "r").read()
    dataList = pullData.split('\n')
    xList = []
    yList = []
    for eachLine in dataList:
        if len(eachLine) > 1:
            x, y = eachLine.split(',')
            xList.append(int(x))
            yList.append(int(y))

    # now we want to clear all the data and redraw it
    a.clear()
    a.plot(xList, yList)
'''



# base for adding a frame
class SeaofBTCapp(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        # insert the icon int eh corner, rather than the feather
        tk.Tk.iconbitmap(self, default="favicon.ico")

        # change the title
        tk.Tk.wm_title(self, "Sea of BTC client")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # just some options in the menubar
        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Save settings", command=lambda: popupmsg("Not supported just yet!"))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=quit)
        # now place the menubar
        menubar.add_cascade(label="File", menu=filemenu)

        # new menu option
        exchangeChoice = tk.Menu(menubar, tearoff=1)
        exchangeChoice.add_command(label="Bitfinex",
                                    command=lambda: changeExchange("Bitfinex", "bitfinex"))
        exchangeChoice.add_command(label="Bitstamp",
                                    command=lambda: changeExchange("Bitstamp", "bitstamp"))
        exchangeChoice.add_command(label="Huobi",
                                    command=lambda: changeExchange("Huobi", "huobi"))
        # now place the exchange menubar
        menubar.add_cascade(label="Exchange", menu=exchangeChoice)


        # how much data are we going to be looking at
        dataTF = tk.Menu(menubar, tearoff=1)
        dataTF.add_command(label = "Tick",
                            command=lambda: changeTimeFrame('tick'))
        dataTF.add_command(label = "1 Day",
                            command=lambda: changeTimeFrame('1d'))
        dataTF.add_command(label = "3 Day",
                            command=lambda: changeTimeFrame('3d'))
        dataTF.add_command(label = "1 Week",
                            command=lambda: changeTimeFrame('7d'))
        menubar.add_cascade(label = "Data Time Frame", menu = dataTF)

        # Config the Open High, Low Close...(width of the candlestick)
        OHLCI = tk.Menu(menubar, tearoff=1)
        OHLCI.add_command(label = "Tick",
                            command=lambda: changeTimeFrame('tick'))
        OHLCI.add_command(label = "1 Minute",
                            command=lambda: changeSampleSize('1Min', 0.0005))
        OHLCI.add_command(label = "5 Minute",
                            command=lambda: changeSampleSize('5Min', 0.003))
        OHLCI.add_command(label = "15 Minute",
                            command=lambda: changeSampleSize('15Min', 0.008))
        OHLCI.add_command(label = "30 Minute",
                            command=lambda: changeSampleSize('30Min', 0.016))
        OHLCI.add_command(label = "1 Hour",
                            command=lambda: changeSampleSize('1H', 0.032))
        OHLCI.add_command(label = "3 Hour",
                            command=lambda: changeSampleSize('3H', 0.096))
        menubar.add_cascade(label = "OHLC Interval", menu = OHLCI)

        # with the graph, we wnat a TOP Indicator(RSI(relative strength index), or macd)
        topIndi = tk.Menu(menubar, tearoff=1)
        topIndi.add_command(label = "None",
                            command=lambda: addTopIndicator('none'))
        topIndi.add_command(label = "RSI",
                            command=lambda: addTopIndicator('rsi'))
        topIndi.add_command(label = "MACD",
                            command=lambda: addTopIndicator('macd'))
        menubar.add_cascade(label="Top Indicator", menu=topIndi)

        # we also want a MIDDLE Indicator(SMA(simple moving average), EMA(exponential moving average))
        mainI = tk.Menu(menubar, tearoff=1)
        mainI.add_command(label = "None",
                            command=lambda: addMiddleIndicator('none'))
        mainI.add_command(label = "SMA",
                            command=lambda: addMiddleIndicator('sma'))
        mainI.add_command(label = "EMA",
                            command=lambda: addMiddleIndicator('ema'))
        menubar.add_cascade(label="Main/middle Indicator", menu=mainI)

        # and now we want a BOTTOM Indicator
        bottomI = tk.Menu(menubar, tearoff=1)
        bottomI.add_command(label = "None",
                            command=lambda: addBottomIndicator('none'))
        bottomI.add_command(label = "RSI",
                            command=lambda: addBottomIndicator('rsi'))
        bottomI.add_command(label = "MACD",
                            command=lambda: addBottomIndicator('macd'))
        menubar.add_cascade(label="Bottom Indicator", menu=bottomI)




        # want people to be able to make trades.. buy/sell
        # we want to set up preset offers... anc bind it to keypresses
        tradeButton = tk.Menu(menubar, tearoff=1)
        # ppl trade with simple rules like SMA>10, trade, or< 10 trade
        tradeButton.add_command(label="Manual Trading",
                                command=lambda: popupmsg("This is not live yet!"))
        tradeButton.add_command(label="Automated Trading",
                                command=lambda: popupmsg("This is not live yet!"))

        # user can do quick buy and sell(fee for trading)
        # different amounts of buying and selling because of the fee.middleIndicator
        tradeButton.add_command(label="Quick Buy",
                                command=lambda: popupmsg("This is not live yet!"))
        tradeButton.add_command(label="Quick Sell",
                                command=lambda: popupmsg("This is not live yet!"))

        tradeButton.add_command(label="Set-up Quick Buy/Sell",
                                command=lambda: popupmsg("This is not live yet!"))

        menubar.add_cascade(label="Trading", menu=tradeButton)

        # want to start and stop so that when we zoom in, we want to freeze screen
        startStop = tk.Menu(menubar, tearoff=1)
        startStop.add_command(label="Resume",
                                command=lambda: loadChart('start'))
        startStop.add_command(label="Pause",
                                command=lambda: loadChart('stop'))                      
        menubar.add_cascade(label="Resume/Pause client", menu=startStop)

        # add a help Menu
        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Tutorial", command=tutorial)
        menubar.add_cascade(label="Help", menu=helpmenu)



        tk.Tk.config(self, menu=menubar)
        # when have a bunch of windows, can insert window here
        # then go down to StartPage class and create a for loop to choose one
        # every new page has to go throguh self.frames... just like StartPage
        # so just add a for loop
        self.frames = {}
        
        # says later on, "hey I want to show this frame"
        # add any newe pages to the tuple
        for F in (StartPage, BTCe_Page):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew") # alignment+stretch=sticky

        self.show_frame(StartPage)

    def show_frame(self, cont): # controller=cont

        frame = self.frames[cont] # tkRaise raises one of the hidden frame to front
        frame.tkraise()

def qf(param):
    print(param)

# Use lambda to create a quick function that can be thrown away


# Now we need to starta frame
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="""ALPHA Bitcoin Trading Application
        Use at your own risk. There is not promise
        of warranty.""", font=LARGE_FONT)
        label.pack(padx=10, pady=10)

        # button2 = tk.Button(self, text="Visit Page 1", command=qf("yoyoyoy"))
        # make s a throwaway function, and the point is so that it runs immediately rather than when called.
        # Can't pass through variables usng lambda, have to first tell the computer that 
        # that it is using a different button.
        button = ttk.Button(self, text="Agree", command=lambda: controller.show_frame(BTCe_Page))

        button.pack()

    # Add here if we want to insert a new page
        button2 = ttk.Button(self, text="Disagree", command=quit)

        button2.pack()

# PageOne is just a reference, it is not in main SeaofBTCapp
class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page 1!", font=LARGE_FONT)
        label.pack(padx=10, pady=10)

        # button1 = tk.Button(self, text="Visit Page 1", command=qf("yoyoyoy"))
        button1 = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage))

        button1.pack()

'''
        button2 = ttk.Button(self, text="Page two", command=lambda: controller.show_frame(PageTwo))

        button2.pack()
'''





'''
class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page 2!", font=LARGE_FONT)
        label.pack(padx=10, pady=10)

        # button1 = tk.Button(self, text="Visit Page 1", command=qf("yoyoyoy"))
        button1 = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage))

        button1.pack()

        button2 = ttk.Button(self, text="Page One", command=lambda: controller.show_frame(PageOne))

        button2.pack()
'''

# Page 3 for our graphs
class BTCe_Page(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Graph Page!", font=LARGE_FONT)
        label.pack(padx=10, pady=10)

        button1 = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage))

        button1.pack()



        # bring up the canvas
        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # we also want the navigation bar
        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # we want the graph to be autoupdating(maybe daemon working through tcl)
        # but not sure how to do it in tkinter, but can in matplotlib
        # we want live updates
        # we will use animation function to update/redraw graph every 2 secs



        # plot first, add the canvas, show it, put stuff to the canvas, add the navbar


# FOUNDATION FOR THE APP ABOVE
# adding more button and code affects PageOne function
app = SeaofBTCapp()

# make size of app, more than enouh for graph
app.geometry("1280x720")

#get the animation in before the mainloop
# 100 milliseconds = 1 sec
# need to make the text document with the sample data
ani = animation.FuncAnimation(f, animate, interval=5000)

app.mainloop()

# maybe check out matplotlib tutorial series