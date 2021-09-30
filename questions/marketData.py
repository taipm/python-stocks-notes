from urllib.request import urlopen
import json
import pandas as pd

def getAllStockPrices():
  url = "https://stock.kdtv4.vn/api/app/company-stock/stocks"

  # store the response of URL
  response = urlopen(url)

  data_json = json.loads(response.read())

  df = pd.json_normalize(data_json)
  df = df[['stockCode', 'giaTriTangGiam', 'phanTramTangGiam', 'dongCua', 'khoiLuong', 'moCua',
           'caoNhat', 'thapNhat', 'giaoDichThoaThuan', 'nuocNgoaiMua', 'nuocNgoaiBan', 'postedDate']]
  df.sort_values(["postedDate"], ascending=False)

  df['Stock'] = df['stockCode']
  del df['stockCode']

  df['+/-'] = df['giaTriTangGiam']
  del df['giaTriTangGiam']

  df['%'] = df['phanTramTangGiam']
  del df['phanTramTangGiam']

  df['DC'] = df['dongCua']
  del df['dongCua']

  df['KL'] = df['khoiLuong']
  del df['khoiLuong']

  df['MC'] = df['moCua']
  del df['moCua']

  df['CN'] = df['caoNhat']
  del df['caoNhat']

  df['TN'] = df['thapNhat']
  del df['thapNhat']

  df['NN Mua'] = df['nuocNgoaiMua']
  del df['nuocNgoaiMua']

  df['NN Ban'] = df['nuocNgoaiBan']
  del df['nuocNgoaiBan']

  df['TT'] = df['giaoDichThoaThuan']
  del df['giaoDichThoaThuan']
  #print(df)
  stocks = list(set(df['Stock']))
  stocks = sorted(stocks)
  print(stocks)
  df_stocks = []
  for stock in stocks:
    df_stock = df[df['Stock'] == stock]
    #print(df_stock)
    df_stocks.append(df_stock)

  return df


#getAllStockPrices("CTG")
