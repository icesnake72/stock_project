'''
주식 정보 검색 메인 윈도우
MVC 모델에서 View 역할을 담당함

'''

import tkinter as tk
import tkinter.ttk as ttk
from typing import Final
from main_window import MainWin


class StockSearchWin(MainWin):
  def __init__(self, 
               event_handler, # 이벤트를 처리할 Controller 객체
               title: str = "Main Window", 
               width: int = 640, 
               height: int = 480, 
               resize: tuple = (True, True)) -> None:
    super().__init__(title, width, height, resize)  # 부모 클래스의 생성자를 호출하는것으로 메인 윈도우 생성
    self.eh = event_handler   # 이벤트를 처리할 Controller 객체
    
  def __del__(self):
    '''메인 윈도우가 제거될때 matplotlib에서 생성한 윈도우들도 같이 제거해줘야 됨!!! (필수)'''
    # self.clear_graph_window() # matplotlib에서 생성한 윈도우 제거함
  
  
  def _initLayout(self):
    '''메인 윈도우의 레이아웃을 만듬'''
    
    # 상단의 검색 영역
    self.topPanel = tk.PanedWindow(self._win,                                    
                                   height=30,
                                   relief='groove',
                                  #  bg='black',
                                   orient=tk.HORIZONTAL)
    self.topPanel.pack(side='top', fill='x')
    
    # 즐겨찾기를 위한 왼쪽 패널 윈도우 영역
    self.leftPanel = tk.PanedWindow(self._win,                                    
                                    width=150,                                    
                                    # bg='red',     
                                    relief='groove',                               
                                    orient=tk.VERTICAL)
    self.leftPanel.pack(side='left', fill='y')
    
    # 데이터를 표현하는 오른쪽 패널 윈도우 영역
    self.rightPanel = tk.PanedWindow(self._win, bg='red')
    self.rightPanel.pack(side='left', fill='both', expand=True)        
    
    self.__initTopPanelLayout()   # top 영역 하위의 위젯들 생성 및 배치
    self.__initLeftPaneLayout()   # left 영역 하위의 위젯들 생성 및 배치
    self.__initRightPanelLayout() # right 영역 하위의 위젯들 생성 및 배치
  
  
  def __initTopPanelLayout(self):
    '''top 영역 하위의 위젯들 생성 및 배치'''
    
    # '검색' 레이블 
    self.lbSearch = ttk.Label(self.topPanel, text='검색')
    self.lbSearch.grid(row=0, column=0) # grid로 배치함
    
    # '검색' 입력 Entry 위젯 생성
    self.editSearch = ttk.Entry(self.topPanel,
                                width=30)
    self.editSearch.grid(row=0, column=1)
        
    # 버튼에 표시할 이미지 불러옴
    self.icon_image1 = tk.PhotoImage(file=MainWin.get_current_path('go.png'))
    
    # 버튼 위젯 생성
    self.btnGo = ttk.Button(self.topPanel, 
                            text='Go!', 
                            image=self.icon_image1, 
                            width=10,                                                         
                            compound='left',
                            command=lambda:self.eh.OnGoButtonClick(self, self.btnGo)
                            )
    self.btnGo.grid(row=0, column=2) # grid로 배치
    
    # 검색 결과를 저장할 Combobox 위젯 생성
    self.cbSearched = ttk.Combobox(self.topPanel, state='readonly')
    # self.cbSearched['values'] = ('1','2','3')
    # self.cbSearched.current(0)
    self.cbSearched.place(x=466, y=5)   # place()를 이용해 배치함
        
    # ComboBox가 선택될때 이벤트 처리, Controller 객체의 OnSearchComboSelected 메소드를 호출함
    self.cbSearched.bind("<<ComboboxSelected>>", lambda event : self.eh.OnSearchComboSelected(event, self, self.cbSearched))
    
    # 즐겨찾기 버튼 생성
    self.btnAddFavor = ttk.Button(self.topPanel, 
                                  text='즐겨찾기',                                   
                                  width=10,                                                                  
                                  command=lambda:self.eh.OnAddFavorButtonClick(self, self.btnAddFavor)
                                )
    
    self.btnAddFavor.place(x=672, y=1)   # place()를 이용해 배치함
    
    
  def __initLeftPaneLayout(self):
    '''left 영역 하위의 위젯들 생성 및 배치'''
    
    # '즐겨찾기'를 표시하는 Label 생성 및 배치
    self.lbFavor = ttk.Label(self.leftPanel, text='즐겨찾기')
    self.lbFavor.pack(side='top', fill='x')
    
    # ListBox 생성 및 배치
    self.lboxFavor = tk.Listbox(self.leftPanel,
                                width=20,
                                selectmode='single')
    self.lboxFavor.pack(side='top', fill='both', expand=True)
  
  
  def __initRightPanelLayout(self):
    '''right 영역 하위의 위젯들 생성 및 배치'''
    
    # 배치될 항목들의 넓이, 높이, 폰트등의 상수들을 정의함
    width_big:Final = 25
    width_field:Final = 20
    width_field_small:Final = 15
    height_mid_panel:Final = 300
    ftBig:Final = 20
    ftNormal = 12
    ftMalgun:Final = 'Malgun Gothic'
    
    # right panel을 다시 상, 중, 하 3등분 함
    
    # right panel의 top panel 생성
    self.rpTopPanel = tk.PanedWindow(self.rightPanel)
    self.rpTopPanel.pack(side='top', fill='x')
    
    # 종목 코드 레이블 위젯 생성
    self.lbCode = ttk.Label(self.rpTopPanel, text='CODE', width=width_field)
    self.lbCode.grid(row=0, column=0, sticky='w')
        
    # 종목명 레이블 위젯 생성
    self.lbJong = ttk.Label(self.rpTopPanel, text='종목.........................', width=width_big, font=(ftMalgun, 24, 'bold'))
    self.lbJong.grid(row=1, column=0, columnspan=4, sticky='w')
    
    # 종가 레이블 위젯 생성
    self.lbValue = ttk.Label(self.rpTopPanel, text='종가', width=width_field, font=(ftMalgun, ftBig), foreground='red')
    self.lbValue.grid(row=2, column=0, sticky='nsw')
    
    # 전일비 레이블 위젯 생성
    self.lbChange = ttk.Label(self.rpTopPanel, text='전일대비', width=width_big+5, font=(ftMalgun, ftNormal), foreground='red')
    self.lbChange.grid(row=3, column=0, sticky='nsw')
    
    # 전일 레이블 위젯 생성
    self.lbValYester = ttk.Label(self.rpTopPanel, text='전일', width=width_field_small, font=(ftMalgun, ftNormal))
    self.lbValYester.grid(row=2, column=1)
    
    # 고가 레이블 위젯 생성
    self.lbValGoga = ttk.Label(self.rpTopPanel, text='고가', width=width_big, font=(ftMalgun, ftNormal))
    self.lbValGoga.grid(row=2, column=2)
    
    # 거래량 레이블 위젯 생성
    self.lbValCount = ttk.Label(self.rpTopPanel, text='거래량', font=(ftMalgun, ftNormal))
    # self.lbValCount = ttk.Label(self.rpTopPanel, text='거래량', width=width_field, font=(ftMalgun, ftNormal))
    self.lbValCount.grid(row=2, column=3, sticky='ew')
    
    # 시가 레이블 위젯 생성
    self.lbValSiga = ttk.Label(self.rpTopPanel, text='시가', width=width_field_small, font=(ftMalgun, ftNormal))
    self.lbValSiga.grid(row=3, column=1)
    
    # 저가 레이블 위젯 생성
    self.lbValJeoga = ttk.Label(self.rpTopPanel, text='저가', width=width_big, font=(ftMalgun, ftNormal))
    self.lbValJeoga.grid(row=3, column=2)
    
    # 거래대금 레이블 위젯 생성
    self.lbValAmount = ttk.Label(self.rpTopPanel, text='거래대금', width=width_field, font=(ftMalgun, ftNormal))
    self.lbValAmount.grid(row=3, column=3,sticky='ew')  
    
    # right panel의 Middle panel 생성, 그래프가 표시될 영역
    self.rpMidPanel = tk.PanedWindow(self.rightPanel, bg='black', height=height_mid_panel)
    self.rpMidPanel.pack(side='top', fill='x')
    
    # right panel의 Bottom panel 생성, 일별 주식정보를 위한 트리뷰 위젯이 표시될 영역
    self.rpBottomPanel = tk.PanedWindow(self.rightPanel, bg='white')
    self.rpBottomPanel.pack(side='top', fill='both', expand=True)
    
    # Bottom Panel 영역에 일별 주가를 표시할 Treeview 위젯 생성
    self.daysStockList = ttk.Treeview(self.rpBottomPanel, 
                         columns=("날짜", "종가", "전일비", "시가", "고가", "저가", "거래량"), 
                         show="headings")
    # 각 컬럼에 컬럼 헤더 지정
    self.daysStockList.heading("날짜", text="날짜")
    self.daysStockList.heading("종가", text="종가")
    self.daysStockList.heading("전일비", text="전일비")
    self.daysStockList.heading("시가", text="시가")
    self.daysStockList.heading("고가", text="고가")
    self.daysStockList.heading("저가", text="저가")
    self.daysStockList.heading("거래량", text="거래량")
    
    # 각 컬럼의 넓이 지정
    self.daysStockList.column("날짜", width=80, anchor="e")
    self.daysStockList.column("종가", width=80, anchor="e")
    self.daysStockList.column("전일비", width=80, anchor="e")
    self.daysStockList.column("시가", width=80, anchor="e")
    self.daysStockList.column("고가", width=80, anchor="e")
    self.daysStockList.column("저가", width=80, anchor="e")
    self.daysStockList.column("거래량", width=80, anchor="e")
    
    self.daysStockList.pack(side='top', fill='both', expand=True)
    
    # self.daysStockList.insert("", "end", values=("2023.05.26", "100,000", "100,000", "100,000", "100,000", "100,000", "100,000"))
    
  def clear_graph_window(self):    
    '''PanedWindow 내부의 모든 위젯 완전히 삭제'''
    for widget in self.rpMidPanel.winfo_children():
      try:
        widget.destroy()
      except:
        print(f'{widget}.destroy() 에서 에러가 발생함')
        
        
  def _OnClosingMainWindow(self):
    self.clear_graph_window()
    super()._OnClosingMainWindow()


