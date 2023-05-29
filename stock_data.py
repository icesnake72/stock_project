'''
Model : 데이터 저장 및 관리
'''

import pandas as pd
from typing import Final

class StockData:
  '''주식 데이터셋을 저장하고 관리하는 객체'''
  
  # 클래스 상수를 정의
  SUBJECT:Final = '종목'
  DATE:Final = '날짜'
  F_VALUE:Final = '종가'
  CHANGE:Final = '전일비'
  C_VALUE:Final = '시가'
  H_VALUE:Final = '고가'
  L_VALUE:Final = '저가'
  COUNT:Final = '거래량'
  
  def __init__(self) -> None:
    self._init_data()   # _init_data()에서 데이터 초기화를 진행하는 이유는 모든 데이터들을 삭제하고 다시 로드할 필요가 있기 때문이다   
  
  def _init_data(self):
    '''모든 데이터들을 삭제하고 다시 로드할 필요가 있기 때문에 초기화 메소드를 별도로 만듬'''
    
    # DataFrame 객체 생성
    self.data = pd.DataFrame({StockData.SUBJECT:[],     # 종목명
                          StockData.DATE:[],        # 날짜
                          StockData.F_VALUE:[],     # 종가
                          StockData.CHANGE:[],      # 전일비
                          StockData.C_VALUE:[],     # 시가
                          StockData.H_VALUE:[],     # 고가
                          StockData.L_VALUE:[],     # 저가
                          StockData.COUNT:[]}       # 거래량
                          )
    
    # 키값들만 리스트에서 따로 관리 (빠른 처리와 코드를 줄이기 위함)
    self.keys = [ col for col in self.data.columns ]
    
  
  @property
  def DataFrame(self):  # DataFrame 객체를 외부에 노출시킴
    return self.data
  
  def remove_all(self):
    '''DataFrame내의 모든 데이터들을 삭제하고 초기화 시킴'''
    self.data.drop(self.data.index, inplace=True) # DataFrame내의 모든 데이터 삭제
    self._init_data()   # 주식 데이터 형식으로 초기화
  
  def insert_row(self, name:str, rec:list):
    '''
    Row (Record, 열) 데이터 추가 메소드
    name : 주식 종목 이름
    rec : 해당 종목에 대한 데이터 클래스 상수에 지정된 종목명 제외한 7개의 데이터를 리스트 형태로 받음
    '''
    
    # 문자열 데이터를 숫자로 변환
    liTmp = []
    for item in rec:
      try:
        liTmp.append( int(item.replace(',','')) ) # 문자열에 ','를 제거하고 정수형으로 변환하여 임시 리스트에 입력함
      except:
        liTmp.append(item)  # , 가 없는 경우 날짜 정보이기 때문에 형변환없이 입력한다
      
    liTmp.insert(0, name) # 임시 리스트의 첫번째 항목에는 종목명을 입력함
    # self.data.loc[0] = liTmp
    self.data.loc[self.data.shape[0]] = liTmp # 매 0번째 인덱스에 현재 받은 데이터를 입력함
    
    
  def sort_by(self, col:str):
    '''DataFrame내의 객체들을 col 행에 의해 정렬'''
    self.data = self.data.sort_values(col)
  
    
    
    
  
  