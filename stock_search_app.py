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


class StockSearchApp:
  def __init__(self, 
               title:str="Window Application", 
               width:int=640, 
               height:int=480, 
               resize: tuple=(True, True)) -> None:
    self.MainWindow = StockSearchWin(self, title="주식 정보 검색", width=width, height=height)    
    
    self.li_url = {}
    
  @property
  def Window(self) -> tk.Tk:
    return self.MainWindow.Window
  
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
    config_path = MainWin.get_image_path('config.json')
    with open(config_path, 'r') as fconf:
      conf_data = json.load(fconf)      
    
    # 네이버 증권 홈페이지로 이동    
    url = conf_data['Search URL']
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
    self.__OnSearchComboSelected(win, win.cbSearched)
    
    driver.quit()
    
  #
  def OnSearchComboSelected(self, event, win:StockSearchWin, obj:ttk.Combobox):
    self.__OnSearchComboSelected(win, obj)

  #
  def __OnSearchComboSelected(self, win:StockSearchWin, obj:ttk.Combobox):
    '''콤보박스가 선택되면 종목이 선택된것이므로 해당 주식종목 페이지로 이동하여 모든 정보들을 받아와 화면에 출력하도록 한다'''
    
    # 종목명을 설정한다
    win.lbJong.configure(text=obj.get())
    
    # 검색단계에서 추출한 url을 불러온다
    url = self.li_url[obj.get()]  
    
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
    config_path = MainWin.get_image_path('config.json')
    with open(config_path, 'r') as fconf:
      conf_data = json.load(fconf)     
      
    win.daysStockList.delete(*win.daysStockList.get_children())
    
    for i in range(1,3):
      url = conf_data['Search URL']
      driver = webdriver.Chrome(options=chrome_options)
      url += f'/item/sise_day.naver?code={code}&page={i}'
      driver.get(url)
      
      time.sleep(1)   # 페이지가 로딩될때까지 잠깐 기다리기

      listock = []
      tbody = driver.find_element(By.XPATH, '/html/body/table[1]/tbody')
      trs = tbody.find_elements(By.TAG_NAME, 'tr')
      for tr in trs:
        up = True
        try:
          img = tr.find_element(By.TAG_NAME, 'img')
          up = True if img.get_attribute('alt')=='하락' else False
        except NoSuchElementException:
          continue
        
        try:    
          attr = tr.get_attribute('onmouseover')
          litmp = tr.text.split()
          if not up:
            litmp[2] = f'-{litmp[2]}'
        finally:
          listock.append(litmp)

      for stock_data in listock:
        win.daysStockList.insert("", "end", values=stock_data)
        
    
    
    
    
app = StockSearchApp(title="주식 정복 검색", width=1000, height=800)
app.Window.mainloop()