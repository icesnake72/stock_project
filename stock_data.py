'''
Model : 데이터 저장 및 관리
'''

import pandas as pd
from typing import Final

class StockData:
  SUBJECT:Final = '종목'
  DATE:Final = '날짜'
  F_VALUE:Final = '종가'
  CHANGE:Final = '전일비'
  C_VALUE:Final = '시가'
  H_VALUE:Final = '고가'
  L_VALUE:Final = '저가'
  COUNT:Final = '거래량'
  
  def __init__(self) -> None:
    self._init_data()
    
  def _init_data(self):
    self.data = pd.DataFrame({StockData.SUBJECT:[],     # 종목명
                          StockData.DATE:[],        # 날짜
                          StockData.F_VALUE:[],     # 종가
                          StockData.CHANGE:[],      # 전일비
                          StockData.C_VALUE:[],     # 시가
                          StockData.H_VALUE:[],     # 고가
                          StockData.L_VALUE:[],     # 저가
                          StockData.COUNT:[]}       # 거래량
                          )
    self.keys = [ col for col in self.data.columns ]
    
  
  @property
  def DataFrame(self):
    return self.data

  def remove_all(self):
    self.data.drop(self.data.index, inplace=True)
    self._init_data()
  
  def insert_row(self, name:str, rec:list):
    liTmp = []
    for item in rec:
      try:
        liTmp.append( int(item.replace(',','')) )
      except:
        liTmp.append(item)  # , 가 없는 경우 날짜 정보이기 때문에 형변환없이 입력한다
      
    liTmp.insert(0, name)
    # self.data.loc[0] = liTmp
    self.data.loc[self.data.shape[0]] = liTmp
    
  def sort_by(self, col:str):
    self.data = self.data.sort_values(col)
  
    
    
    
  
  