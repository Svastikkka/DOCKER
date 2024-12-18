# Get the stocks info
import yfinance as yf
 
# Ticker is a function responsible 
# for fetching the data MSFT is
# representing info about Microsoft 
# Corporation
msft = yf.Ticker('RELIANCE.NS')
 
# msft.info will return all information
# about microsoft corporation
data = msft.history()
 
# printing the data
print(data)