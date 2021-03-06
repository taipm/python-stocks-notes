import tabulate as tabulate
import pandas as pd
import re
from html_table_extractor.extractor import Extractor
import sys
import numpy as np
import requests
from bs4 import BeautifulSoup
import urllib.request
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from urllib.request import urlopen
import json
import pandas as pd 

def buildDetailUrl(stock):
    url = 'https://www.cophieu68.vn/snapshot.php?id=' + stock
    return url


def buildUrl(stock, n):
    url = 'https://www.cophieu68.vn/historyprice.php?currentPage=' + \
        str(n) + '&id=' + stock
    return url


def buildSoup(url):
   page = urllib.request.urlopen(url)
   soup = BeautifulSoup(page, 'html.parser')
   return soup.encode("utf-8")

def getStocks():
  url = 'https://vuichungkhoan.blogspot.com/2020/11/danh-muc-quan-trong.html'
  response = requests.get(url, verify=False)
  soup = BeautifulSoup(response.text, "html.parser")
  html = soup.findAll(
      'div', {"class": "post-body entry-content float-container"})[0].get_text()
  if(len(html) == 0):
    print("Mã cổ phiếu sai hoặc không lấy được thông tin cổ phiếu")
    return -1
  else:
    try:
      stocks = html.split(', ')
      items = []
      for _stock in stocks:
        if ',' in _stock:
          items.append(_stock.split(',')[0].strip())
          items.append(_stock.split(',')[1].strip())
        else:
          items.append(_stock.strip().upper())
      items = list(items)
      items.sort()
      return items
    except:
      print("Không lấy được dữ liệu")
      return -1
  
def getStockPrices(stock):
  url = "https://stock.kdtv4.vn/api/app/company/by-stock-code?stockCode=" + stock.upper()

  # store the response of URL
  response = urlopen(url)

  data_json = json.loads(response.read())

  df = pd.json_normalize(data_json['companyStocks'])
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

  return df

def importData(stock):
    #print(stock)
    if(stock == "INDEX"):
        return
    elif (len(stock.strip()) > 3):
        return
    elif (len(stock.strip()) < 3):
        return
    else:
        url = buildUrl(stock, 1)
        response = requests.get(url, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.findAll('table', {"class": "stock"})
        if(len(table) == 0):
            print("Mã cổ phiếu sai hoặc không lấy được thông tin cổ phiếu")
            return -1
        else:
            try:
                tr = table[0].findAll(['tr'])[1:]
                tablePrices = []
                i = 0
                for cell in tr:
                    th = cell.find_all('th')
                    th_data = [col.text.strip('\n') for col in th]
                    td = cell.find_all('td')
                    row = [i.text.replace('\n', '').replace('%','') for i in td]
                    # row = [i.text.replace('\n', '') for i in td]
                    #print(row[0])
                    if(row[0].startswith('#')):
                      tablePrices.insert(
                          i, [row[5], row[4], row[6], row[8], row[9], row[11], row[12]])
                      i = i+1

                #Thêm vào dữ liệu của phiên gần nhất (do cophieu68 thiếu dữ liệu)

                df = pd.DataFrame(
                    tablePrices, columns=['DC', '%', 'KL', 'CN','TN', 'NN Mua', 'NN Ban'])

                df = df.replace(',', '', regex=True)
                df = df.apply(pd.to_numeric, errors='ignore')
                df['KL'] = df['KL']/1000
                df['NN Mua'] = df['NN Mua']/1000
                df['NN Ban'] = df['NN Ban']/1000
                df["NN"] = df['NN Mua'] - df['NN Ban']
                df["KL(NN)"] = df['NN Mua'] + df['NN Ban']
                df["KL(NN)/KL)"] = (df['KL(NN)']/df['KL'])*100
                #print(df)
                return df
            except:
                print("Không lấy được dữ liệu")
                return
                #return None
            #return None
            return


#print(importData("MSN"))

def getDetail(stock):
    if(stock == "INDEX"):
        return
    elif (len(stock.strip()) > 3):
        return
    elif (len(stock.strip()) < 3):
        return
    else:
        url = buildDetailUrl(stock)
        response = requests.get(url, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.findAll('div', {"id": "snapshot_trading"})
        if(len(table) == 0):
            print("Mã cổ phiếu sai hoặc không lấy được thông tin cổ phiếu")
            return -1
        else:
            try:
                tr = table[0].findAll(['tr'])[1:]
                tablePrices = []
                i = 0
                for cell in tr:
                    th = cell.find_all('th')
                    th_data = [col.text.strip('\n') for col in th]
                    td = cell.find_all('td')
                    row = [i.text.replace('\n', '') for i in td]
                    #print(row.decode('utf-8'))
                    #print (row)
                    tablePrices.insert(
                        i, [row[0], row[1]])
                    i = i+1
                #print(tablePrices)
                max_52_tuan = tablePrices[5][1]
                min_52_tuan = tablePrices[6][1]
                min_in_day = tablePrices[1][1].strip().split(' ')[0]
                max_in_day = tablePrices[1][1].strip().split('\t')[1].strip()

                # print("Max: " + str(max_52_tuan))
                # print("Min: " + str(min_52_tuan))
                # print("Max in day: " + max_in_day)
                # print("Min in day: " + min_in_day)

                return [max_52_tuan, min_52_tuan, max_in_day, min_in_day]
            except:
                print("Không lấy được dữ liệu")
                return

              #return None
            #return None


#STOCK = "HPG"
#max_52 = getDetail(STOCK)[0]
#print(getDetail(STOCK))
