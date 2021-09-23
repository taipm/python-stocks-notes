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
    print("Break")
    pivots = []
    for i in range(0,len(prices_hist)-3):
        x = ((prices_hist[i]-prices_hist[i+1])/prices_hist[i+1])*100
        if(x >= 3):
            note_pivot = ""
            print('Break price')
            y = vols_hist[i] / \
                np.average([vols_hist[i], vols_hist[i+1], vols_hist[i+2]])
            if(y >= 1):
                print("Break : " + str(i) + "(" + str(x) + "," + str(y) + ")")
                mark_pivot = float("{:.2f}".format(x*y))
                margin_from_pivot = float("{:.2f}".format(
                    np.sum(prices_margins_hist[0:i])))
                
                note_pivot = note_pivot + str(margin_from_pivot) + ' (%)'
                if(mark_pivot >= 8):
                    note_pivot = note_pivot + "] ==> Chú ý: Cực mạnh"
                pivots.append(
                    [i, prices_hist[i], vols_hist[i], mark_pivot, note_pivot])
            if(i<=5):
                note = note + "\nLưu ý: Có điểm pivot rất gần"
    
    #Tính điểm #01: Sức mạnh (Giá, KL)
    price_avg_3 = np.average(prices[0:2])
    vol_avg_5 = np.average(vols[0:4])
    
    mark_vol = (vol-vol_avg_5)/vol_avg_5
    mark_price = (price-price_avg_3)/price_avg_3
    mark_1 = mark_vol*mark_price*100
    
    #Tính điểm #02: Đánh dấu cột mốc lịch sử (Giá vượt đỉnh lịch sử (cùng với KL tương xứng))
    print(np.max(prices))
    mark_2 = 0
    if(price >= np.max(prices_hist[1:])):
        note = note + "\nGhi chú đặc biệt:\n(1) Giá vượt đỉnh lịch sử"
        mark_2 = 10
        if(vol >= np.max(vols_hist[1:])):
            note = note + "\n(2) Vol & Giá cùng vượt đỉnh lịch sử"
            mark_2 = 15
        else: #Ghi chú về vol
            note = note + "\nVol ~ " + \
                "{:.2f}".format(((vol-np.max(vols_hist[1:]))/np.max(vols_hist[1:]))
                                * 100) + "(%) vs Max_Vol (100 phiên)"
    print('Điểm 02')
    mark = mark_1 + mark_2
    print("Điểm : " + str(mark))
    print(note)
    
    note_price = ""
    try:
        note_price = note_price + \
            "{:.2f}".format(((price-np.max(prices_hist[1:]))/np.max(prices_hist[1:]))*100) + " (%) vs Max(100 phiên)"
        print("Điểm 03")
    except:
        print('Lỗi tính ở điểm 03')
    
    #Tính 03: Sức mạnh giá trong phiên
    margin_price_inday = ((df["CN"][0] - df["CN"][1])/df["CN"][1])*100
    margin_price_today = ((prices[0] - prices[1])/prices[1])*100
    
    return [stock.upper(), n, price, vol, price_max, price_min, vol_max, 
            vol_min, vol_avg, data_hist, rate_price, rate_vol, mark, pivots, note, note_price, margin_price_inday, margin_price_today]

#def getMark(df):
    
