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
    
    self._initLayout()
    self.set_min_size()    
    
  @property
  def Window(self) -> tk.Tk:
    return self._win
  
  def set_min_size(self, width:int=300, height:int=300) -> None:
    self._win.minsize(width, height)
    
  @abstractmethod
  def _initLayout(self): pass
  
  @staticmethod
  def get_image_path(image_file_name:str) -> str:
    # print('here')
    # 현재 스크립트 파일의 경로 가져오기
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # 이미지 파일의 상대 경로 구성
    image_path = os.path.join(script_dir, image_file_name)
    # print(image_path)
    return image_path
  
  @staticmethod
  def getSystemFonts():
    # 시스템에서 사용 가능한 TTF 폰트 목록 가져오기
    available_fonts = font.families()
    # 폰트 목록 출력
    liFonts = [ font_name for font_name in available_fonts ]
    return liFonts