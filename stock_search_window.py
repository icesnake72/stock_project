import tkinter as tk
import tkinter.ttk as ttk
from typing import Final
from main_window import MainWin


class StockSearchWin(MainWin):
  def __init__(self, 
               event_handler,
               title: str = "Main Window", 
               width: int = 640, 
               height: int = 480, 
               resize: tuple = (True, True)) -> None:
    super().__init__(title, width, height, resize)
    self.eh = event_handler
  
  
  def _initLayout(self):
    self.style = ttk.Style()
    
    self.topPanel = tk.PanedWindow(self._win,                                    
                                   height=30,
                                   relief='groove',
                                  #  bg='black',
                                   orient=tk.HORIZONTAL)
    self.topPanel.pack(side='top', fill='x')
    
    self.leftPanel = tk.PanedWindow(self._win,                                    
                                    width=150,                                    
                                    # bg='red',     
                                    relief='groove',                               
                                    orient=tk.VERTICAL)
    self.leftPanel.pack(side='left', fill='y')
    
    self.rightPanel = tk.PanedWindow(self._win, bg='red')
    self.rightPanel.pack(side='left', fill='both', expand=True)        
    
    self.__initTopPanelLayout()
    self.__initLeftPaneLayout()
    self.__initRightPanelLayout()
  
  
  def __initTopPanelLayout(self):
    # ttk 스타일 설정
    self.lbSearch = ttk.Label(self.topPanel, text='검색')
    self.lbSearch.grid(row=0, column=0)#.pack(side='left')    
    
    self.editSearch = ttk.Entry(self.topPanel,
                                width=30)
    self.editSearch.grid(row=0, column=1)#pack(side='left')
        
    self.icon_image1 = tk.PhotoImage(file=MainWin.get_image_path('go.png'))    
    self.btnGo = ttk.Button(self.topPanel, 
                            text='Go!', 
                            image=self.icon_image1, 
                            width=10,                                                         
                            compound='left',
                            command=lambda:self.eh.OnGoButtonClick(self, self.btnGo)
                            )
    self.btnGo.grid(row=0, column=2)#.pack(side='left')
    
    self.cbSearched = ttk.Combobox(self.topPanel, state='readonly')
    self.cbSearched['values'] = ('1','2','3')
    self.cbSearched.current(0)
    self.cbSearched.place(x=466, y=5)
    
  def __initLeftPaneLayout(self):
    self.lbFavor = ttk.Label(self.leftPanel, text='즐겨찾기')
    self.lbFavor.pack(side='top', fill='x')
    
    self.lboxFavor = tk.Listbox(self.leftPanel,
                                width=30,
                                selectmode='single')
    self.lboxFavor.pack(side='top', fill='both', expand=True)
  
  def __initRightPanelLayout(self):
    width_big:Final = 30
    width_field:Final = 15
    height_mid_panel:Final = 300
    ftBig:Final = 20
    ftNormal = 12
    ftMalgun:Final = 'Malgun Gothic'
    
    self.rpTopPanel = tk.PanedWindow(self.rightPanel)
    self.rpTopPanel.pack(side='top', fill='x')
    
    self.lbCode = ttk.Label(self.rpTopPanel, text='CODE', width=width_field)
    self.lbCode.grid(row=0, column=0, sticky='w')
        
    self.lbJong = ttk.Label(self.rpTopPanel, text='종목.........................', width=width_big, font=(ftMalgun, 24, 'bold'))
    self.lbJong.grid(row=1, column=0, columnspan=4, sticky='w')
    
    self.lbValue = ttk.Label(self.rpTopPanel, text='종가', width=width_field, font=(ftMalgun, ftBig), foreground='red')
    self.lbValue.grid(row=2, column=0, rowspan=2, sticky='nsw')
    
    self.lbValYester = ttk.Label(self.rpTopPanel, text='전일', width=width_field, font=(ftMalgun, ftNormal))
    self.lbValYester.grid(row=2, column=1)
    
    self.lbValGoga = ttk.Label(self.rpTopPanel, text='고가', width=width_field, font=(ftMalgun, ftNormal))
    self.lbValGoga.grid(row=2, column=2)
    
    self.lbValCount = ttk.Label(self.rpTopPanel, text='거래량', font=(ftMalgun, ftNormal))
    # self.lbValCount = ttk.Label(self.rpTopPanel, text='거래량', width=width_field, font=(ftMalgun, ftNormal))
    self.lbValCount.grid(row=2, column=3, sticky='ew')
    
    self.lbValSiga = ttk.Label(self.rpTopPanel, text='시가', width=width_field, font=(ftMalgun, ftNormal))
    self.lbValSiga.grid(row=3, column=1)
    
    self.lbValJeoga = ttk.Label(self.rpTopPanel, text='저가', width=width_field, font=(ftMalgun, ftNormal))
    self.lbValJeoga.grid(row=3, column=2)
    
    self.lbValAmount = ttk.Label(self.rpTopPanel, text='거래대금', width=width_field, font=(ftMalgun, ftNormal))
    self.lbValAmount.grid(row=3, column=3,sticky='ew')  
    
    self.rpMidPanel = tk.PanedWindow(self.rightPanel, bg='black', height=height_mid_panel)
    self.rpMidPanel.pack(side='top', fill='x')
    
    self.rpBottomPanel = tk.PanedWindow(self.rightPanel, bg='white')
    self.rpBottomPanel.pack(side='top', fill='both', expand=True)
    



