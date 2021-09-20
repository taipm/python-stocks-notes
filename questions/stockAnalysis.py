from pandas.core.frame import DataFrame
from questions.crawler import importData
import numpy as np

def stock_analysis_result(stock, n):
    df_data = importData(stock)
    df = DataFrame(df_data)
    
    prices_hist = df['DC'] #Để tìm điểm pivots
    prices_margins_hist = df['%']  # Để tìm điểm pivots
    vols_hist = df['KL']  # Để tìm điểm pivots
    data_hist = df.to_html()
    
    df = df.head(n+1)
    
    prices = df['DC']
    vols = df['KL']
    #price_margins = df['%']
    #print(price_margins)
    
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
    
    #ĐIỂM BREAK (VOL, PRICE)
    pivots = []
    for i in range(0,len(prices_hist)-3):
        x = ((prices_hist[i]-prices_hist[i+1])/prices_hist[i+1])*100
        if(x >= 3):
            print('Break price')
            y = vols_hist[i] / \
                np.average([vols_hist[i], vols_hist[i+1], vols_hist[i+2]])
            if(y >= 1):
                print("Break : " + str(i) + "(" + str(x) + "," + str(y) + ")")
                mark_pivot = float("{:.2f}".format(x*y))
                note_pivot = ""
                
                margin_from_pivot = float("{:.2f}".format(
                    np.sum(prices_margins_hist[0:i])))
                
                note_pivot = note_pivot + str(margin_from_pivot) + ' (%)'
                if(mark_pivot >= 8):
                    note_pivot = note_pivot + "] ==> Chú ý: Cực mạnh"
                pivots.append(
                    [i, prices_hist[i], vols_hist[i], mark_pivot, note_pivot])
    
    #Tính điểm #01: Sức mạnh (Giá, KL)
    price_avg_3 = np.average(prices[0:2])
    vol_avg_5 = np.average(vols[0:4])
    
    mark_vol = (vol-vol_avg_5)/vol_avg_5
    mark_price = (price-price_avg_3)/price_avg_3
    mark_1 = mark_vol*mark_price*100
    
    #Tính điểm #02: Xu hướng (số phiên tăng nhiều hơn số phiên giảm)
    
    mark = mark_1
    print(note)
    
    return [stock.upper(), n, price, vol, price_max, price_min, vol_max, 
            vol_min, vol_avg, data_hist, rate_price, rate_vol, mark, pivots, note]

#def getMark(df):
    
