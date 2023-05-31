'''
App 객체
MVC 모델의 Controller 역할을 담당하는 모듈임
이 모듈에서 앱을 실행함
'''


import time, json
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

from main_window import MainWin
from stock_search_window import StockSearchWin
from stock_data import StockData

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class StockSearchApp:
  def __init__(self, 
               title:str="Window Application", 
               width:int=640, 
               height:int=480, 
               resize: tuple=(True, True)) -> None:
    self.MainWindow = StockSearchWin(self, title="주식 정보 검색", width=width, height=height)    
    
    self.li_url = {}
    self.data = StockData()
        
    self.load_config_data()
    self.init_favorite_items() 
        
  @property
  def Window(self) -> tk.Tk:
    return self.MainWindow.Window
    
  
  def load_config_data(self):
    # config file 불러오기
    config_path = MainWin.get_current_path('config.json')
    with open(config_path, 'r', encoding='utf-8') as fconf:
      self.conf_data = json.load(fconf)
      
      
  def init_favorite_items(self):
    if 'Favorite' in self.conf_data:
      subjects:dict = self.conf_data['Favorite']    
      self.MainWindow.insert_list_box_items(subjects.keys())    
  
  
  ###
  # Go 버튼을 클릭했을때 발생한 이벤트를 처리하는 메소드
  def OnGoButtonClick(self, win:StockSearchWin, obj:ttk.Button):
    # 검색란에 있는 텍스트를 toFind 변수에 저장
    toFind = win.editSearch.get()
    
    # 검색 입력란이 비어있는 상태로 이 버튼을 클릭하면 아무일도 수행하지 않는다    
    if toFind=="":
      return
    
    # Chrome 옵션 설정
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 크롬 브라우저를 숨기는 옵션 추가
    chrome_options.add_argument("--disable-gpu")  # GPU 가속 비활성화 옵션 추가
    
    # config file 불러오기
    # config_path = MainWin.get_current_path('config.json')
    # with open(config_path, 'r', encoding='utf-8') as fconf:
    #   conf_data = json.load(fconf)      
    
    # 네이버 증권 홈페이지로 이동    
    url = self.conf_data['Search URL']
    # driver = webdriver.Chrome()
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    
    # 네이버 증권 검색란에 toFind에 입력된 내용을 입력함
    toSearchEntry = driver.find_element(By.XPATH, "//*[@id='stock_items']")
    toSearchEntry.send_keys(toFind)
    toSearchEntry.send_keys(Keys.ENTER)
    
    # 처리결과를 잠시 기다리기
    time.sleep(1)
           
    # 검색결과의 내용이 없다면 콤보박스의 내용을 '검색 결과 없음'으로 변경하고 처리를 종료함
    no_res = driver.find_element(By.XPATH, "//*[@id='content']/div[3]")  # no_data를 찾은 경우 검색결과가 없다
    if no_res.get_attribute('class')=='no_data':
      win.cbSearched['values'] = ['검색 결과 없음']
      win.cbSearched.current(0)
      return
    
    # 검색 결과에서 찾기     
    tbody = driver.find_element(By.XPATH, " //*[@id='content']/div[4]/table/tbody")
    name_elems = tbody.find_elements(By.CLASS_NAME, 'tit')    
    self.li_url = { elem.text:elem.find_element(By.TAG_NAME, 'a').get_attribute('href') for elem in name_elems }
    win.cbSearched['values'] = list(self.li_url.keys())
    win.cbSearched.current(0)
    self.__OnSearchComboSelected(win, win.cbSearched.get())
    
    driver.quit()
    
  # 콤보 박스가 선택되었을때 발생하는 이벤트, 여기서 아래에 __OnSearchComboSelected() 메소드를 재호출한다
  def OnSearchComboSelected(self, event, win:StockSearchWin, obj:ttk.Combobox):
    stock_name:str = obj.get()
    self.__OnSearchComboSelected(win, stock_name=stock_name)
    
  def OnSearchFavoriteListBoxSelected(self, event, win:StockSearchWin, obj:tk.Listbox):
    # 종목의 날짜별 url을 가져오는 방법이 다름
    # self.li_url.clear()
    
    stock_name:str = obj.get(obj.curselection())    
        
    code = self.conf_data['Favorite'][stock_name]
    add_url = f'https://finance.naver.com/item/sise.naver?code={code}'
    self.li_url[stock_name] = add_url
        
    self.__OnSearchComboSelected(win, stock_name=stock_name)

  # 
  def __OnSearchComboSelected(self, win:StockSearchWin, stock_name:str):
    '''콤보박스가 선택되면 종목이 선택된것이므로 해당 주식종목 페이지로 이동하여 모든 정보들을 받아와 화면에 출력하도록 한다'''
    
    # 종목명을 설정한다
    win.lbJong.configure(text=stock_name)
    
    # 검색단계에서 추출한 url을 불러온다
    url = self.li_url[stock_name]  
    
    # Chrome 옵션 설정
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 크롬 브라우저를 숨기는 옵션 추가
    chrome_options.add_argument("--disable-gpu")  # GPU 가속 비활성화 옵션 추가
    
    # 네이버 증권 홈페이지로 이동            
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    
    # 종목 코드
    code = driver.find_element(By.XPATH, '//*[@id="middle"]/div[1]/div[1]/div/span[1]').text
    win.lbCode.configure(text=f'CODE : {code}')
    
    # 현재가를 가져오기전에 주가가 올랐는지 내렸는지 검사한다
    color = 'black' # 기본 컬러는 블랙으로 설정
    no_today = driver.find_element(By.XPATH, '//*[@id="chart_area"]/div[1]/div/p[1]/em')
    if no_today.get_attribute('class')=='no_up':
      color = 'red'
    elif no_today.get_attribute('class')=='no_down':
      color = 'blue'    
    
    # 현재가
    jongga = driver.find_element(By.XPATH, '//*[@id="chart_area"]/div[1]/div/p[1]').text.strip('\n').replace('\n', '')    
    win.lbValue.configure(text=jongga, foreground=color)
    
    # 전일대비
    change = driver.find_element(By.XPATH, '//*[@id="chart_area"]/div[1]/div/p[2]').text.strip().replace('\n', '')
    change = change.replace('전일대비', '전일대비 : ')
    change = change.replace('상승', '상승 ')
    change = change.replace('하락', '하락 ')
    change = change.replace('l', ' 🔴 ')
    win.lbChange.configure(text=change, foreground=color) 
    
    # 전일  
    temp = driver.find_element(By.XPATH, '//*[@id="chart_area"]/div[1]/table/tbody/tr[1]/td[1]').text.strip().replace('\n', '')
    temp = temp.replace('전일', '전일 : ')
    win.lbValYester.configure(text=temp)
    
    #고가 
    temp = driver.find_element(By.XPATH, '//*[@id="chart_area"]/div[1]/table/tbody/tr[1]/td[2]').text.strip().replace('\n', '')
    temp = temp.replace('고가', '고가 : ')
    win.lbValGoga.configure(text=temp)
    
    # 거래량
    temp = driver.find_element(By.XPATH, '//*[@id="chart_area"]/div[1]/table/tbody/tr[1]/td[3]').text.strip().replace('\n', '')
    temp = temp.replace('거래량', '거래량 : ')
    win.lbValCount.configure(text=temp)
    
    # 시가
    temp = driver.find_element(By.XPATH, '//*[@id="chart_area"]/div[1]/table/tbody/tr[2]/td[1]').text.strip().replace('\n', '')
    temp = temp.replace('시가', '시가 : ')
    win.lbValSiga.configure(text=temp)
    
    # 저가
    temp = driver.find_element(By.XPATH, '//*[@id="chart_area"]/div[1]/table/tbody/tr[2]/td[2]').text.strip().replace('\n', '')
    temp = temp.replace('저가', '저가 : ')
    win.lbValJeoga.configure(text=temp)
    
    # 거래대금
    temp = driver.find_element(By.XPATH, '//*[@id="chart_area"]/div[1]/table/tbody/tr[2]/td[3]').text.strip().replace('\n', '')
    temp = temp.replace('거래대금', '거래대금 : ')
    win.lbValAmount.configure(text=temp)
    
    # 트리뷰에 날짜별 주가 입력하기
    # config file 불러오기
    # config_path = MainWin.get_current_path('config.json')
    # with open(config_path, 'r', encoding='utf-8') as fconf:
    #   conf_data = json.load(fconf)     
      
    # tree view에 모든 데이터 삭제
    win.daysStockList.delete(*win.daysStockList.get_children())
    
    # pandas DataFrame객체의 데이터 삭제
    self.data.remove_all()  
    
    for i in range(1,3):  # 1에서 시작, 3-1까지 반복
      url = self.conf_data['Search URL']   # Search URL 항목은 네이버 증권 홈페이지임
      driver = webdriver.Chrome(options=chrome_options) # 크롬을 히든으로 적용
      url += f'/item/sise_day.naver?code={code}&page={i}' # url을 만듬
      driver.get(url)
      
      time.sleep(1)   # 페이지가 로딩될때까지 잠깐 기다리기

      listock = []  # 주식 데이터를 임시 저장할 리스트 생성
      tbody = driver.find_element(By.XPATH, '/html/body/table[1]/tbody')  # tbody 엘리먼트 찾기
      trs = tbody.find_elements(By.TAG_NAME, 'tr')  # tbody 엘리먼트 아래 모든 tr 엘리먼트들을 찾음
      for tr in trs:  # 찾은 모든 tr 엘리먼트들을 순차적으로 반복하면서...
        up = True   # 일단 상승으로 가정
        try:
          img = tr.find_element(By.TAG_NAME, 'img')   # tr엘리먼트 하위에 img 엘리먼트가 있는지 검사
          up = True if img.get_attribute('alt')=='하락' else False  # img엘리먼트가 있고 'alt'속성이 '하락'이라면 up은 False
        except NoSuchElementException:
          continue  # img 엘리먼트를 찾지 못했다면 다음 tr 엘리먼트를 검사, 데이터 열이 아니므로 처리 진행을 할 필요도 없음
        
        try:    
          attr = tr.get_attribute('onmouseover')  # tr엘리먼트에 onmouseover 속성이 있다면 데이터 tr 엘리먼트임
          litmp = tr.text.split() # tr태그 하위의 모든 텍스트를 가져와 공백으로 분리하여 임시 리스트에 저장
          if not up:
            litmp[2] = f'-{litmp[2]}' # up==False이면 즉, 전일대비 하락이면 전일비 항목을 음수로 바꿈
        finally:
          listock.append(litmp)   # listock 또한 DataFrame에 담기 위한 2차원 List 객체임

      for stock_data in listock:  # 모든 listock 리스트의 아이템들을 순회하며...
        win.daysStockList.insert("", "end", values=stock_data)  # tree view에 데이터 입력
        self.data.insert_row(stock_name, stock_data)   # pandas DataFrame 객체에 데이터 입력
    
    # 그래프 생성
    self.data.sort_by(StockData.DATE)   # 날짜로 재정렬
    
    win.clear_graph_window()  # rpMidPanel의 child윈도우들을 삭제함
    
    fig, ax = plt.subplots()  # 피규어는 그래프 윈도우, Axes는 그래프가 실제로 그려지는 영역이다
    fig.set_size_inches(3,2)  # 피규어의 사이즈를 인치로 지정
    ax.plot(self.data.DataFrame['날짜'], self.data.DataFrame['종가']) # 그래프의 x, y축 데이터를 지정
    
    # 폰트 설정
    font = {'family': 'AppleGothic', 'size': 6}

    # 폰트 설정 적용
    plt.rc('font', **font)
     
    ax.tick_params(axis='x', rotation=45)   # x축의 Lable들을 45도 기울임
    canvas = FigureCanvasTkAgg(fig, master=win.rpMidPanel)  # 피규어를 이용하여 Tkinter Canvas 객체 생성
    canvas.draw() # 캔버스에 그래프를 그림
    
    # tkinter 캔버스를 윈도우에 배치
    canvas.get_tk_widget().pack(side='top', fill='both')
    
    # Matplotlib 인스턴스 종료
    plt.close()
    
  def OnAddFavorButtonClick(self, win:StockSearchWin, obj:ttk.Button):
    # config_path = MainWin.get_current_path('config.json')
    # with open(config_path, 'r', encoding='utf-8') as fconf:
    #   conf_data = json.load(fconf)    
      
    jong_mok = win.lbJong.cget('text')
    if jong_mok==StockSearchWin.INIT_SUBJECT:
      return
    
    code:str = win.lbCode.cget('text')
    index = code.find(':')
    code = code[index+1:]
    code = code.strip()
    
    subject = {jong_mok:code}
    
    if 'Favorite' in self.conf_data:
      favorite_dic = self.conf_data['Favorite']
    else:
      favorite_dic = {}
      
    # conf_dict = dict(self.conf_data)
    favorite_dic.update(subject)
    
    self.conf_data['Favorite'] = favorite_dic
    
    # JSON 파일로 저장
    with open('config.json', 'w', encoding='utf-8') as f:
      json.dump(self.conf_data, f, indent=4)
      
    # 환경 파일 다시 로드
    self.load_config_data()
      
    items = win.lboxFavor.get(0, tk.END)  # 리스트 박스내에 모든 데이터들을 가져옴
    if not jong_mok in items:
      win.lboxFavor.insert(0, jong_mok)
    
      
    
    
    
    
app = StockSearchApp(title="주식 정복 검색", width=1000, height=800)
app.Window.mainloop()