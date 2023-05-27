import time, json
import tkinter as tk
import tkinter.ttk as ttk

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

from main_window import MainWin
from stock_search_window import StockSearchWin


class StockSearchApp:
  def __init__(self, 
               title:str="Window Application", 
               width:int=640, 
               height:int=480, 
               resize: tuple=(True, True)) -> None:
    self.MainWindow = StockSearchWin(self, title="주식 정보 검색", width=800, height=800)    
    
    # 웹드라이버 초기화
    self.driver = webdriver.Chrome()
    
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
    # chrome_options = Options()
    # chrome_options.add_argument("--headless")  # 크롬 브라우저를 숨기는 옵션 추가
    # chrome_options.add_argument("--disable-gpu")  # GPU 가속 비활성화 옵션 추가
    
    config_path = MainWin.get_image_path('config.json')
    conf_data = json.loads(config_path)
    print(conf_data)    
    
    # 네이버 증권 홈페이지로 이동    
    url = 'https://finance.naver.com'
    driver = webdriver.Chrome()
    # driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    
    # 네이버 증권 검색란에 toFind에 입력된 내용을 입력함
    toSearchEntry = driver.find_element(By.XPATH, "//*[@id='stock_items']")
    toSearchEntry.send_keys(toFind)
    toSearchEntry.send_keys(Keys.ENTER)
    
    
    
    # driver.quit()

    
    



app = StockSearchApp(title="주식 정복 검색", width=800, height=800)
app.Window.mainloop()