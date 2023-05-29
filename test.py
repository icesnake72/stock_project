# import tkinter as tk
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# # 임의의 데이터 생성
# x = [1, 2, 3, 4, 5]
# y = [2, 4, 6, 8, 10]

# # Tkinter 윈도우 생성
# window = tk.Tk()
# window.title("Graph Example")

# # Matplotlib Figure 생성
# fig = plt.Figure()

# # Figure에 그래프 추가
# ax = fig.add_subplot(111)
# ax.plot(x, y)

# # Figure를 Tkinter Canvas에 추가
# canvas = FigureCanvasTkAgg(fig, master=window)
# canvas.draw()
# canvas.get_tk_widget().pack()


# # import subprocess

# # # 시스템 명령 실행하여 한글을 지원하는 폰트 목록 가져오기
# # result = subprocess.run("system_profiler SPFontsDataType | grep 'Family:.*Korean'", capture_output=True, text=True, shell=True)

# # # 출력 결과에서 한글 폰트 목록 가져오기
# # font_list = result.stdout.splitlines()
# # print(font_list)

# # # 폰트 목록 출력
# # for font_info in font_list:
# #     font_family = font_info.split(":")[-1].strip()
# #     print(font_family)


# # Tkinter 윈도우 실행
# # window.mainloop()

# import tkinter as tk
# from tkinter import ttk

# def button_clicked():
#     print("Button Clicked")

# # Tkinter 윈도우 생성
# window = tk.Tk()
# window.title("Custom Button Example")

# # ttk 스타일 설정
# style = ttk.Style()

# # 버튼에 적용할 스타일 정의
# style.configure("CustomButton.TButton",
#                 font=("Helvetica", 12),
#                 padding=(10,10,10,10),
#                 width=200,
#                 background="#4CAF50",
#                 foreground="black")

# # 아이콘 이미지 가져오기 (예시로 사용하는 이미지 파일 경로에 따라 수정해주세요)
# icon_image = tk.PhotoImage(file="go.png")

# # 버튼 생성
# button = ttk.Button(window, text="Click Me", image=icon_image, compound="left", style="CustomButton.TButton")
# button.pack()

# # 버튼 클릭 이벤트 연결
# button.configure(command=button_clicked)

# # Tkinter 윈도우 실행
# window.mainloop()




# import tkinter as tk
# from tkinter import ttk

# # Tkinter 윈도우 생성
# window = tk.Tk()
# window.title("PanedWindow Example")

# # PanedWindow 생성
# paned_window = ttk.Panedwindow(window, orient=tk.HORIZONTAL)
# paned_window.pack(fill=tk.BOTH, expand=True)

# # 버튼 생성
# button = ttk.Button(paned_window, text="Button")
# paned_window.add(button, weight=1)

# # 콤보 박스 생성
# combobox = ttk.Combobox(paned_window, values=["Option 1", "Option 2", "Option 3"])
# paned_window.add(combobox, weight=1)

# # Tkinter 윈도우 실행
# window.mainloop()




# import tkinter as tk
# from tkinter import ttk

# # 윈도우 생성
# window = tk.Tk()

# # Treeview 생성
# tree = ttk.Treeview(window, columns=("column1", "column2"), show="headings")

# # 각 컬럼에 컬럼 헤더 지정
# tree.heading("column1", text="Column 1")
# tree.heading("column2", text="Column 2")

# # 각 컬럼의 넓이 지정
# tree.column("column1", width=100)
# tree.column("column2", width=100)

# # 데이터 추가
# tree.insert("", "end", values=("Value 1", "Value 2"))
# tree.insert("", "end", values=("Value 3", "Value 4"))
# tree.insert("", "end", values=("Value 5", "Value 6"))

# # 특정 셀의 태그에 글자 색상 설정
# tree.item("I001", values=("Value 1", "Value 2"), tags=("colored_cell",))
# tree.item("I002", values=("Value 3", "Value 4"), tags=("colored_cell",))

# # 색상 설정을 위한 스타일 생성
# tree.tag_configure("colored_cell", foreground="blue")

# # 표시
# tree.pack()

# # 메인 루프 실행
# window.mainloop()


# from stock_data import StockData

# sd = StockData()
# data = sd.DataFrame

# li = [ col for col in data.columns ]
# print(li)

# print(data.columns)

# import pandas as pd
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# import tkinter as tk

# # 데이터가 포함된 DataFrame 생성
# data = {'Year': [2010, 2011, 2012, 2013, 2014],
#         'Value': [5, 3, 7, 2, 4]}
# df = pd.DataFrame(data)

# # 윈도우 생성
# root = tk.Tk()

# # Figure 객체 생성
# fig = plt.figure(figsize=(5, 4))

# # Axes 객체 생성
# ax = fig.add_subplot(111)

# # 그래프 그리기
# ax.plot(df['Year'], df['Value'])

# # 그래프를 Tkinter 윈도우에 표시하기 위한 FigureCanvasTkAgg 객체 생성
# canvas = FigureCanvasTkAgg(fig, master=root)
# canvas.draw()
# canvas.get_tk_widget().pack()

# # 그래프 지우기
# ax.clear()

# # 새로운 그래프 그리기
# ax.plot(df['Year'], df['Value'] * 2)

# # 그래프를 Tkinter 윈도우에 다시 표시하기
# canvas.draw()

# # Tkinter 윈도우 실행
# root.mainloop()


for i in range(1,3):
  print(i)