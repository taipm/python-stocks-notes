from pandas.core.frame import DataFrame
from questions.crawler import importData
import numpy as np

def stock_analysis_result(stock, n):
    df_data = importData(stock)
    df = DataFrame(df_data)
    data_hist = df.to_html()
    df = df.head(n+1)
    
    price = df['DC'][0]
    vol = df['KL'][0]
    
    price_max = np.max(df['DC'][1:])
    price_min = np.min(df['DC'][1:])
    vol_max = np.max(df['KL'][1:])
    vol_min = np.min(df['KL'][1:])
    
    vol_avg = np.average(df['KL'][1:])
    
    price_n = df['DC'][n]
    print(price_n)
    print(price)
    
    rate_vol = vol/vol_avg
    rate_price = ((price-price_n)/price_n)*100
    print(rate_price)
    print(rate_vol)
    
    note = "Tín hiệu mạnh: "
    
    if(vol >= np.max(df['KL'])):
        note = note + "\nVượt đỉnh KL (" + str(n) + ") phiên"
        
    if(price >= np.max(df['DC'])):
        note = note + "\nVượt đỉnh Giá (" + str(n) + ") phiên"
        
    print(note)
    
    return [stock.upper(), n, price, vol, price_max, price_min, vol_max, vol_min, vol_avg, data_hist, rate_price, rate_vol, note]

#html = stock_analysis_result(STOCK)
#print(html)
