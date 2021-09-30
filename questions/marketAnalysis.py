from pandas.core.frame import DataFrame
from questions.marketData import getAllStockPrices
import numpy as np
import pandas as pd



def stock_analysis(stock, _df):
    df_data = _df

    n = 20
    prices_hist = _df['DC'] #Để tìm điểm pivots
    prices_margins_hist = _df['%']  # Để tìm điểm pivots
    vols_hist = _df['KL']  # Để tìm điểm pivots
    
    #Tín hiệu chung
    vuotdinh_price = 0
    if prices_hist[0] >= np.max(prices_hist[1:]):
      vuotdinh_price = 1

    vuotdinh_vol = 0
    if prices_hist[0] >= np.max(prices_hist[1:]):
      vuotdinh_vol = 1

    #nn_hist = (df['NN Mua'] - df['NN Bán'])
    data_hist = _df.to_html()
    
    df = _df.head(n+1)
    
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
    #print(price_n)
    #print(price)
    
    rate_vol = vol/vol_avg
    rate_price = ((price-price_n)/price_n)*100
    #print(rate_price)
    #print(rate_vol)
    
    note = "Tín hiệu mạnh: "
    
    if(vol >= np.max(df['KL'])):
        note = note + "\nVượt đỉnh KL (" + str(n) + ") phiên"
        
    if(price >= np.max(df['DC'])):
        note = note + "\nVượt đỉnh Giá (" + str(n) + ") phiên"
    
    #ĐIỂM BREAK (VOL, PRICE)
    #print("Break")
    pivots = []
    for i in range(0,len(prices_hist)-3):
        x = ((prices_hist[i]-prices_hist[i+1])/prices_hist[i+1])*100
        if(x >= 3):
            note_pivot = ""
            #print('Break price')
            y = vols_hist[i] / \
                np.average([vols_hist[i], vols_hist[i+1], vols_hist[i+2]])
            if(y >= 1):
                #print("Break : " + str(i) + "(" + str(x) + "," + str(y) + ")")
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
    #print(np.max(prices))
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
    #print('Điểm 02')
    mark = mark_1 + mark_2
    #print("Điểm : " + str(mark))
    print(note)
    
    note_price = ""
    try:
        note_price = note_price + \
            "{:.2f}".format(((price-np.max(prices_hist[1:]))/np.max(prices_hist[1:]))*100) + " (%) vs Max(100 phiên)"
        #print("Điểm 03")
    except:
        print('Lỗi tính ở điểm 03')
    
    #Tính 03: Sức mạnh giá trong phiên
    margin_price_inday = ((df["CN"][0] - df["CN"][1])/df["CN"][1])*100
    margin_price_today = ((prices[0] - prices[1])/prices[1])*100
    
    #Tính 04: Số phiên tăng/giảm
    count_tang = 0
    margin_tang = 0 #Tổng giá trị tăng trong 100 phiên
    count_giam = 0
    margin_giam = 0 #Tổng giá trị giảm trong 100 phiên
    for i in prices_margins_hist[0:20]:
        if(i > 0):
            count_tang = count_tang + 1
            margin_tang = margin_tang + i
        elif(i < 0):
            count_giam = count_giam + 1
            margin_giam = margin_giam + i
    #print("Số phiên tăng: " + str(count_tang))
    #print("Số phiên giảm: " + str(count_giam))

    return [stock.upper(), n, price, vol, price_max, price_min, vol_max, #6
            vol_min, vol_avg, data_hist, rate_price, rate_vol, mark, pivots, #13
            note, note_price, margin_price_inday, margin_price_today, df_data, #18
            count_giam, margin_giam, count_tang, margin_tang, vuotdinh_price,vuotdinh_vol] #24

def market_analysis_result():
  df_market = getAllStockPrices()
  #print(df_market)
  df = df_market

  #print(df)
  stocks = list(set(df['Stock']))
  stocks = sorted(stocks)
  #print(stocks)
  df_stocks = []
  i = 0
  count_tang = 0
  count_giam = 0

  results = []
  for stock in stocks:
    # i = i + 1
    # print(i)
    df_stock = df[df['Stock'] == stock]
    #_df = pd.DataFrame(df_stock)
    df_stock = df_stock.reset_index(drop = True)
    rs = stock_analysis(stock, df_stock) #margin_price_today
    rs_margin = rs[17]
    rs_mark = float("{:.2f}".format(rs[12]))
    rs_vuotdinh_gia = rs[23]
    rs_vuotdinh_vol = rs[24]
    #print(stock + " điểm: " + str(rs_mark))
    if(rs_margin > 0):
      count_tang = count_tang + 1
    elif (rs_margin ==0):
      count_giam = count_giam + 1
    df_stocks.append([stock,df_stock])
    results.append([stock, rs_mark, rs_vuotdinh_gia, rs_vuotdinh_vol])

  #01 - Cổ phiếu tăng/giảm
  #print("Số cổ phiếu tăng: " + str(count_tang))
  #print("Số cổ phiếu giảm: " + str(count_giam))
  count_stocks_decrease = df_market
  #return [df_market]

  new_df = pd.DataFrame(results, columns=['Stock','Mark','Over_Price','Over_Vol'])
  new_df = new_df.sort_values(by='Over_Price', ascending=False)
  return new_df



# def stock_analysis(stock, _df):
#     df_data = _df

#     n = 20
#     prices_hist = _df['DC']  # Để tìm điểm pivots
#     prices_margins_hist = _df['%']  # Để tìm điểm pivots
#     vols_hist = _df['KL']  # Để tìm điểm pivots

#     #nn_hist = (df['NN Mua'] - df['NN Bán'])
#     data_hist = _df.to_html()

#     df = _df.head(n+1)

#     prices = df['DC']
#     vols = df['KL']
#     #price_margins = df['%']
#     #print(price_margins)

#     price = df['DC'][0]
#     vol = df['KL'][0]

#     price_max = np.max(df['DC'][1:])
#     price_min = np.min(df['DC'][1:])
#     vol_max = np.max(df['KL'][1:])
#     vol_min = np.min(df['KL'][1:])

#     vol_avg = np.average(df['KL'][1:])

#     price_n = df['DC'][n]
#     #print(price_n)
#     #print(price)

#     rate_vol = vol/vol_avg
#     rate_price = ((price-price_n)/price_n)*100
#     #print(rate_price)
#     #print(rate_vol)

#     note = "Tín hiệu mạnh: "

#     if(vol >= np.max(df['KL'])):
#         note = note + "\nVượt đỉnh KL (" + str(n) + ") phiên"

#     if(price >= np.max(df['DC'])):
#         note = note + "\nVượt đỉnh Giá (" + str(n) + ") phiên"

#     #ĐIỂM BREAK (VOL, PRICE)
#     #print("Break")
#     pivots = []
#     for i in range(0, len(prices_hist)-3):
#         x = ((prices_hist[i]-prices_hist[i+1])/prices_hist[i+1])*100
#         if(x >= 3):
#             note_pivot = ""
#             #print('Break price')
#             y = vols_hist[i] / \
#                 np.average([vols_hist[i], vols_hist[i+1], vols_hist[i+2]])
#             if(y >= 1):
#                 #print("Break : " + str(i) + "(" + str(x) + "," + str(y) + ")")
#                 mark_pivot = float("{:.2f}".format(x*y))
#                 margin_from_pivot = float("{:.2f}".format(
#                     np.sum(prices_margins_hist[0:i])))

#                 note_pivot = note_pivot + str(margin_from_pivot) + ' (%)'
#                 if(mark_pivot >= 8):
#                     note_pivot = note_pivot + "] ==> Chú ý: Cực mạnh"
#                 pivots.append(
#                     [i, prices_hist[i], vols_hist[i], mark_pivot, note_pivot])
#             if(i <= 5):
#                 note = note + "\nLưu ý: Có điểm pivot rất gần"

#     #Tính điểm #01: Sức mạnh (Giá, KL)
#     price_avg_3 = np.average(prices[0:2])
#     vol_avg_5 = np.average(vols[0:4])

#     mark_vol = (vol-vol_avg_5)/vol_avg_5
#     mark_price = (price-price_avg_3)/price_avg_3
#     mark_1 = mark_vol*mark_price*100

#     #Tính điểm #02: Đánh dấu cột mốc lịch sử (Giá vượt đỉnh lịch sử (cùng với KL tương xứng))
#     #print(np.max(prices))
#     mark_2 = 0
#     if(price >= np.max(prices_hist[1:])):
#         note = note + "\nGhi chú đặc biệt:\n(1) Giá vượt đỉnh lịch sử"
#         mark_2 = 10
#         if(vol >= np.max(vols_hist[1:])):
#             note = note + "\n(2) Vol & Giá cùng vượt đỉnh lịch sử"
#             mark_2 = 15
#         else:  # Ghi chú về vol
#             note = note + "\nVol ~ " + \
#                 "{:.2f}".format(((vol-np.max(vols_hist[1:]))/np.max(vols_hist[1:]))
#                                 * 100) + "(%) vs Max_Vol (100 phiên)"
#     #print('Điểm 02')
#     mark = mark_1 + mark_2
#     #print("Điểm : " + str(mark))
#     print(note)

#     note_price = ""
#     try:
#         note_price = note_price + \
#             "{:.2f}".format(
#                 ((price-np.max(prices_hist[1:]))/np.max(prices_hist[1:]))*100) + " (%) vs Max(100 phiên)"
#         #print("Điểm 03")
#     except:
#         print('Lỗi tính ở điểm 03')

#     #Tính 03: Sức mạnh giá trong phiên
#     margin_price_inday = ((df["CN"][0] - df["CN"][1])/df["CN"][1])*100
#     margin_price_today = ((prices[0] - prices[1])/prices[1])*100

#     #Tính 04: Số phiên tăng/giảm
#     count_tang = 0
#     margin_tang = 0  # Tổng giá trị tăng trong 100 phiên
#     count_giam = 0
#     margin_giam = 0  # Tổng giá trị giảm trong 100 phiên
#     for i in prices_margins_hist[0:20]:
#         if(i > 0):
#             count_tang = count_tang + 1
#             margin_tang = margin_tang + i
#         elif(i < 0):
#             count_giam = count_giam + 1
#             margin_giam = margin_giam + i
#     #print("Số phiên tăng: " + str(count_tang))
#     #print("Số phiên giảm: " + str(count_giam))

#     return [stock.upper(), n, price, vol, price_max, price_min, vol_max,
#             vol_min, vol_avg, data_hist, rate_price, rate_vol, mark, pivots,
#             note, note_price, margin_price_inday, margin_price_today, df_data,
#             count_giam, margin_giam, count_tang, margin_tang]


# def market_analysis_result():
#   df_market = getAllStockPrices()
#   #print(df_market)
#   df = df_market

#   #print(df)
#   stocks = list(set(df['Stock']))
#   stocks = sorted(stocks)
#   #print(stocks)
#   df_stocks = []
#   i = 0
#   count_tang = 0
#   count_giam = 0

#   results = []
#   for stock in stocks:
#     # i = i + 1
#     # print(i)
#     df_stock = df[df['Stock'] == stock]
#     #_df = pd.DataFrame(df_stock)
#     df_stock = df_stock.reset_index(drop=True)
#     rs = stock_analysis(stock, df_stock)  # margin_price_today
#     rs_margin = rs[17]
#     rs_mark = float("{:.2f}".format(rs[12]))
#     print(stock + " điểm: " + str(rs_mark))
#     if(rs_margin > 0):
#       count_tang = count_tang + 1
#     elif (rs_margin == 0):
#       count_giam = count_giam + 1
#     df_stocks.append([stock, df_stock])
#     results.append([stock, rs_mark])

#   #01 - Cổ phiếu tăng/giảm
#   #print("Số cổ phiếu tăng: " + str(count_tang))
#   #print("Số cổ phiếu giảm: " + str(count_giam))
#   count_stocks_decrease = df_market
#   #return [df_market]

#   new_df = pd.DataFrame(results, columns=['Stock', 'Mark'])
#   new_df = new_df.sort_values(by='Mark', ascending=False)
  
#   return new_df
