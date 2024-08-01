from PyQt5.QtWidgets import *
from pathlib import Path
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import numpy as np
import sys
import requests
import json
from bs4 import BeautifulSoup

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        # set the title of main window
        self.setWindowTitle('Sidebar layout - www.luochang.ink')

        # set the size of window
        self.Width = 800
        self.height = int(0.618 * self.Width)
        self.resize(self.Width, self.height)

        # add all widgets
        self.btn_1 = QPushButton('New', self)
        self.btn_2 = QPushButton('Import', self)
        self.btn_3 = QPushButton('Test', self)
        self.btn_4 = QPushButton('Collection', self)
        self.btn_5 = QPushButton('History', self)

        self.btn_1.setObjectName('left_button')
        self.btn_2.setObjectName('left_button')
        self.btn_3.setObjectName('left_button')
        self.btn_4.setObjectName('left_button')
        self.btn_5.setObjectName('left_button')

        self.btn_1.clicked.connect(self.button1)
        self.btn_2.clicked.connect(self.button2)
        self.btn_3.clicked.connect(self.button3)
        self.btn_4.clicked.connect(self.button4)
        self.btn_5.clicked.connect(self.button5)
        # self.savebtn.clicked.connect(self.add_to_collection)

        self.send = QPushButton('Send', self)
        self.raw = QPushButton('raw', self)
        self.pretty = QPushButton('Pretty', self)

        #self.send.clicked.connect(self.text_clean)
        #self.raw.clicked.connect(self.text_show)
        
        self.combo = QComboBox()
        self.combo2 = QComboBox()
        self.combo.addItem('GET')
        self.combo.addItem('PUT')
        self.combo.addItem('POST')
        self.combo.addItem('PATCH')
        self.combo.addItem('DELETE')
        
        self.combo2.addItem('TEXT')
        self.combo2.addItem('JSON')
        self.combo2.addItem('HTML')

        self.url_field = QLineEdit()
        
        self.result_field = QTextBrowser()

        #self.textBox = QTextEdit(self)

        self.showText = QLabel('')

        self.figure = plt.figure()

        self.canvas = FigureCanvas(self.figure)

        self.toolbar = NavigationToolbar(self.canvas, self)

        # initialize variable
        self.strList = np.array([])

        # add tabs
        self.tab1 = self.ui1()
        self.tab2 = self.ui2()
        self.tab3 = self.ui3()
        self.tab4 = self.ui4()
        self.tab5 = self.ui5()


        #Back_end functions---
        self.send.clicked.connect(self.sendrequest)
        self.combo2.currentIndexChanged.connect(self.set_response_mode)
        #-----
        self.initUI()

    def initUI(self):
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.btn_1)
        left_layout.addWidget(self.btn_2)
        left_layout.addWidget(self.btn_3)
        left_layout.addStretch()
        left_layout.addWidget(self.btn_4)
        left_layout.addWidget(self.btn_5)
        left_layout.setSpacing(5)
        left_widget = QWidget()
        left_widget.setLayout(left_layout)
#        left_widget.setStyleSheet('''
#            *{
#                background-color: rgb(20, 30, 50);
#                color: solid white;
#                font-style: bold;
#            }
#            QPushButton{
#                background-color: rgb(20, 30, 50);
#                color: white;
#                font-style: bold;
#                border-style: outset;
#                border-width: 2px;
#                border-radius: 4px;
#                border-color: rgb(80, 100, 120);
#                padding: 4px;
#                text-align:left;
#            }
#            QPushButton#left_button:hover{
#                background:rgb(80,100,120);
#                color: rgb(20, 30, 50);
#                font-style: bold;
#            }
#            QPushButton:pressed {
#                border-style: inset;
#                background-color: rgb(120, 150, 180);
#                font-style: bold;
#                color: rgb(20, 30, 50);
#            }
#            QWidget#left_widget{
#                background:rgb(80,100,120);
#                border-top:1px solid white;
#                border-bottom:1px solid white;
#                border-left:1px solid white;
#                border-top-left-radius:10px;
#                border-bottom-left-radius:10px;
#                font-style: bold;
#            }
#        ''')

        self.right_widget = QTabWidget()
        self.right_widget.tabBar().setObjectName("mainTab")

        self.right_widget.addTab(self.tab1, '')
        self.right_widget.addTab(self.tab2, '')
        self.right_widget.addTab(self.tab3, '')
        self.right_widget.addTab(self.tab4, '')
        self.right_widget.addTab(self.tab5, '')

        self.right_widget.setCurrentIndex(0)
        self.right_widget.setStyleSheet('''QTabBar::tab{width: 0; height: 0; margin: 0; padding: 0; border: none;}''')

        main_layout = QHBoxLayout()
        main_layout.addWidget(left_widget)
        main_layout.addWidget(self.right_widget)
        main_layout.setStretch(0, 40)
        main_layout.setStretch(1, 200)
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    # ----------------- 
    # buttons

    def button1(self):
        self.right_widget.setCurrentIndex(0)
        self.clean()
        self.btn_1.setStyleSheet('''font-style: bold; background:rgb(220,220,220);''')

    def button2(self):
        self.right_widget.setCurrentIndex(1)
        self.clean()
        self.btn_2.setStyleSheet('''font-style: bold; background:rgb(220,220,220);''')

    def button3(self):
        self.right_widget.setCurrentIndex(2)
        self.clean()
        self.btn_3.setStyleSheet('''font-style: bold; background:rgb(220,220,220);''')

    def button4(self):
        self.right_widget.setCurrentIndex(3)
        self.clean()
        self.btn_4.setStyleSheet('''font-style: bold; background:rgb(220,220,220);''')

    def button5(self):
        self.right_widget.setCurrentIndex(4)
        self.clean()
        self.btn_5.setStyleSheet('''font-style: bold; background:rgb(220,220,220);''')

    # ----------------- 
    # functions

    def clean(self):
        self.btn_1.setStyleSheet('''''')
        self.btn_2.setStyleSheet('''''')
        self.btn_3.setStyleSheet('''''')
        self.btn_4.setStyleSheet('''''')
        self.btn_5.setStyleSheet('''''')
    def sendrequest(self):
        # these should be added to the programm ---{
        # headers = self.headers.toPlainText()
        # request_body = self.body.toPlainText()
        #END }---
        url = self.url_field.text()
        method = self.combo.currentText()
        try:
            response = requests.request(
                method,
                url,
                # headers=self.parse_headers(headers),
                # data=request_body,
            )
            response_text = f"Status Code: {response.status_code}\n\n"
            response_text += response.text
        except requests.exceptions.RequestException as e:
            response_text = f"Error: {str(e)}"
        self.result_field.setText(response_text)
    def set_response_mode(self):
        mode = self.combo2.currentText()
        if mode == 'HTML':
            response_html = self.result_field.toPlainText()
            soup = BeautifulSoup(response_html, "html.parser")
            pretty_html = soup.prettify()
            self.result_field.setHtml(pretty_html)
        elif mode == "JSON":
            response_json = self.result_field.toPlainText()
            try:
                parsed_json = json.loads(response_json)
                pretty_json = json.dumps(parsed_json, indent=4)
                self.result_field.setPlainText(pretty_json)
            except json.JSONDecodeError:
                self.result_field.setPlainText(response_json)
        else:
            self.result_field.setPlainText(self.result_field.toPlainText())
    #def text_clean(self):
        #self.textBox.setText('')

    #def text_show(self):
        #self.showText.setText(self.textBox.toPlainText())

        #string = str(self.textBox.toPlainText())
        #for i in range(len(string)):
            #self.strList = np.append(self.strList, string[i])
        #self.plot()
        #self.strList = np.array([])

   # def plot(self):
        #ax = self.figure.add_subplot(111)
        #ax.clear()
        #ax.set(xlabel="character", ylabel="frequency")
        #ax.set(title="The frequency of characters")
        #ax.hist(self.strList, bins=24)
        #self.canvas.draw()
        
    # ----------------- 
    # pages

    def ui1(self):
        upper_layout = QHBoxLayout()
        upper_layout.addWidget(self.combo)
        upper_layout.addWidget(self.url_field)
        upper_layout.addWidget(self.send)
        middle_layout = QHBoxLayout()
        middle_layout.addWidget(self.raw)
        middle_layout.addWidget(self.pretty)
        middle_layout.addStretch()
        middle_layout.addWidget(self.combo2)
        lower_layout = QHBoxLayout()
        lower_layout.addWidget(self.result_field)
        main_layout = QVBoxLayout()
        main_layout.addLayout(upper_layout)
        main_layout.addStretch()
        main_layout.addLayout(middle_layout)
        main_layout.addLayout(lower_layout)
        
        main = QWidget()
        main.setLayout(main_layout)
        return main
    def ui2(self):
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.showText)
        main_layout.addStretch(5)
        main = QWidget()
        main.setLayout(main_layout)
        return main
        
    def ui3(self):
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.toolbar)
        main_layout.addWidget(self.canvas)
        main = QWidget()
        main.setLayout(main_layout)
        return main

    def ui4(self):
        ui4_label1 = QLabel('Sidebar Layout Demo')
        ui4_label1.setStyleSheet('''color:white;font-size:45px;background:rgb(200,220,220);''')
        ui4_label2 = QLabel('Author: Chang Luo\nGender: male\nWebsite: luochang212.github.io\nAvailable: yes')
        ui4_label2.setStyleSheet('''font-size:20px;''')
        ui4_label3 = QLabel('© 2019 Chang Luo')

        footer_layout = QHBoxLayout()
        footer_layout.addStretch(5)
        footer_layout.addWidget(ui4_label3)

        main_layout = QVBoxLayout()
        main_layout.addWidget(ui4_label1)
        main_layout.addWidget(ui4_label2)
        main_layout.addStretch(10)
        main_layout.addLayout(footer_layout)
        main = QWidget()
        main.setLayout(main_layout)
        return main
    
    def ui5(self):
        ui4_label1 = QLabel('Sidebar Layout Demo')
        ui4_label1.setStyleSheet('''color:white;font-size:45px;background:rgb(200,220,220);''')
        ui4_label2 = QLabel('Author: Chang Luo\nGender: male\nWebsite: luochang212.github.io\nAvailable: yes')
        ui4_label2.setStyleSheet('''font-size:20px;''')
        ui4_label3 = QLabel('© 2019 Chang Luo')

        footer_layout = QHBoxLayout()
        footer_layout.addStretch(5)
        footer_layout.addWidget(ui4_label3)

        main_layout = QVBoxLayout()
        main_layout.addWidget(ui4_label1)
        main_layout.addWidget(ui4_label2)
        main_layout.addStretch(10)
        main_layout.addLayout(footer_layout)
        main = QWidget()
        main.setLayout(main_layout)
        return main


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(Path('STYLE.qss').read_text())
    ex = Window()
    ex.show()
    sys.exit(app.exec_())
#  def __init__ (self):
#         super(mainwindow, self).__init__()
#         # Loading the user interface
#         loadUi("mainwindow2.ui",self)
#         #connecting to postman
#         self.sendbtn.clicked.connect(self.sendrequest)
#         self.comboBox.currentIndexChanged.connect(self.set_response_mode)
#         self.savebtn.clicked.connect(self.add_to_collection)
#     def sendrequest(self):
#         url = self.url_field.text()
#         txt = self.comboBox_2.currentText()
#         try:
#             response = requests.request(
#                 txt,
#                 url,
#             )
#             response_text = f"Status Code: {response.status_code}\n\n"
#             response_text += response.text
#         except requests.exceptions.RequestException as e:
#             response_text = f"Error: {str(e)}"
#         self.result_field.setText(response_text)
#     def set_response_mode(self):
#         mode = self.comboBox.currentText()
#         if mode == "HTML":
#             response_html = self.result_field.toPlainText()
#             soup = BeautifulSoup(response_html, "html.parser")
#             pretty_html = soup.prettify()
#             self.result_field.setHtml(pretty_html)
#         elif mode == "JSON":
#             response_json = self.result_field.toPlainText()
#             try:
#                 parsed_json = json.loads(response_json)
#                 pretty_json = json.dumps(parsed_json, indent=4)
#                 self.result_field.setPlainText(pretty_json)
#             except json.JSONDecodeError:
#                 self.result_field.setPlainText(response_json)
#         else:
#             self.result_field.setPlainText(self.result_field.toPlainText())
#     def add_to_collection(self):
#         try :
#             url = self.url_field.text()
#             txt = self.comboBox_2.currentText()
#             response = requests.get(url)
#             if response.status_code == 200:
#                 List = [txt , url] 
#                 l = ','.join(List)
#                 with open('collections.csv', 'a') as f_object:
#                     f_object.write(l + "\n")
#                     f_object.close()
#         except :
#             pass