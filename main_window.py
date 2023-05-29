'''
Tkinter를 사용하여 윈도우 프로그램을 만들기 위한 기본 메인 윈도우 클래스를 정의함
여기에서 기본 틀을 만들고 이 클래스를 상속받아 Application에 필요한 메인 윈도우를 만듬
'''

import os
import tkinter as tk
from tkinter import font

from abc import ABC, abstractmethod

class MainWin:
  def __init__(self, 
               title:str="Main Window",
               width:int=640,
               height:int=480,
               resize:tuple=(True, True)) -> None:
    
    self._win = tk.Tk()
    self._win.title(title)
    left = ( self._win.winfo_screenwidth() - width) // 2
    top = ( self._win.winfo_screenheight() - height) // 2
    coordination = f'{width}x{height}+{left}+{top}'
    self._win.geometry(coordination)
    self._win.resizable(resize[0], resize[1])
    
    self._initLayout()    # 상속받는 클래스에서 _initLayout()메소드를 무조건 구현해야함, 규칙을 만듬
    self.set_min_size()   # 최소사이즈를 초기화함
    
    
  @property
  def Window(self) -> tk.Tk:
    '''메인 윈도우 객체를 반환함'''
    return self._win
  
  def set_min_size(self, width:int=300, height:int=300) -> None:
    self._win.minsize(width, height)
    
    
  @abstractmethod
  def _initLayout(self): pass   # 추상 메소드로서 반드시 상속받는 서브 클래스에서 구현해야됨
  
  @staticmethod
  def get_current_path(image_file_name:str) -> str:    
    # 현재 실행 파일의 경로 가져오기
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # 이미지 파일의 상대 경로 구성
    image_path = os.path.join(script_dir, image_file_name)
    
    return image_path
  
  @staticmethod
  def getSystemFonts():
    # 시스템에서 사용 가능한 TTF 폰트 목록 가져오기
    available_fonts = font.families()
    # 폰트 목록 출력
    liFonts = [ font_name for font_name in available_fonts ]
    return liFonts