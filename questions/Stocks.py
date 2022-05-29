# -*- coding: utf-8 -*- 
from bs4 import BeautifulSoup
from PIL import Image
import os.path
import requests
from requests.exceptions import HTTPError
import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt
#from matplotlib import pyplot as plt, scale
#import plotly.graph_objects as go
#from plotly.subplots import make_subplots
import json
from urllib.request import urlopen
#import Helper
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

STOCKS = "HPG,FPT,HBC,MWG,FRT"

def get_stock_data_from_api(stock):
        
        url = "https://stock.kdtv4.vn/api/app/company/by-stock-code?stockCode=" + stock.upper()
        ssl._create_default_https_context = ssl._create_unverified_context
        
        response = urlopen(url)
        
        data_json = json.loads(response.read())
        #print(data_json)
        df = pd.json_normalize(data_json['companyStocks'])
        df = df[['stockCode','giaTriTangGiam','phanTramTangGiam','dongCua','khoiLuong','moCua','caoNhat','thapNhat','giaoDichThoaThuan','nuocNgoaiMua','nuocNgoaiBan','postedDate']]        
       
        df['Date'] = pd.to_datetime(df['postedDate']).dt.date        
        df = df.sort_values(['Date'], ascending=False)
        del df['postedDate']

        df['Stock'] = df['stockCode']
        del df['stockCode']

        df['+/-'] = df['giaTriTangGiam']
        del df['giaTriTangGiam']

        df['%'] = df['phanTramTangGiam']
        del df['phanTramTangGiam']

        df['Close'] = df['dongCua']
        del df['dongCua']

        df['Volume'] = df['khoiLuong']
        del df['khoiLuong']

        df['Open'] = df['moCua']
        del df['moCua']

        df['High'] = df['caoNhat']
        del df['caoNhat']

        df['Low'] = df['thapNhat']
        del df['thapNhat']

        df['NN Mua'] = df['nuocNgoaiMua']
        del df['nuocNgoaiMua']

        df['NN Ban'] = df['nuocNgoaiBan']
        del df['nuocNgoaiBan']

        df['TT'] = df['giaoDichThoaThuan']
        del df['giaoDichThoaThuan']

        #STEP 2: MỞ RỘNG DỮ LIỆU
        df['Money'] = (df['Close']*df['Volume']*1000*100)/1000000000 #Giá trị giao dịch (tỷ)
        df['NN'] = df['NN Mua'] - df['NN Ban']
        df['M(NN)'] = df['NN']*df['Volume']*1000*100/1000000000 #Giá trị giao dịch của khối ngoại (tỷ)

        df = df.drop_duplicates()
        return df