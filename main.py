import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget , QMainWindow
from PyQt5.QtGui import QPixmap
import csv
import datetime
from bs4 import BeautifulSoup
import re
import json
import requests
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from bs4 import BeautifulSoup
import numpy as np
from pathlib import Path
#combo_Box2---> combo2


#group project ap1402-2nd semester
#Sepehr Ahmadian - Faranak rezaee - Shadan Mojahednia
saves = []
saves2 = []
#The first screen choosing wheather create account or login
class mainwindow(QMainWindow):
    def __init__ (self):
        super(mainwindow, self).__init__()
        # Loading the user interface
        # set the title of main window
        self.setWindowTitle('Main Window')

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
        self.save = QPushButton("Save")
        self.header = QTextEdit()
        self.body = QTextEdit()
        self.l_body = QLabel("Body")
        self.l_header = QLabel("Header")
        self.random_btn = QPushButton('Random', self)

        self.send.setObjectName('new_button')
        self.raw.setObjectName('new_button')
        self.pretty.setObjectName('new_button')
        self.save.setObjectName('new_button')
        self.random_btn.setObjectName('new_button') 

        self.random_combo = QComboBox()                 
        self.random_combo.addItem('GET')                 
        self.random_combo.addItem('POST')                
        self.random_combo.addItem('PUT')                 
        self.random_combo.addItem('PATCH')              
        self.random_combo.addItem('DELETE')              


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
        self.random_line = QLineEdit()
        self.random_line_header = QLineEdit()
        self.random_header = QLabel('Header')
        self.random_line_body = QLineEdit()
        self.random_body = QLabel('Body')
        self.result_field = QTextBrowser()
        self.random_result = QTextBrowser()
        self.random_result.setObjectName('result_field')
       
        #drag & drop
        self.setAcceptDrops(True)
        self.dd_label = QLabel('Drag and drop a file here', self)
        self.menubar = QMenuBar()
        self.file_menu = self.menubar.addMenu('File')
        self.open_action = QAction('Open', self)
        self.open_action.triggered.connect(self.showFileDialog)

        self.collection_tree = QTreeWidget(self)                    
        self.collection_tree.setHeaderLabels(['COLLECTION' ])   
        tree_widget_item1 = QTreeWidgetItem(["GET"])
        self.collection_tree.addTopLevelItem(tree_widget_item1)
        tree_widget_item2 = QTreeWidgetItem(["POST"])
        self.collection_tree.addTopLevelItem(tree_widget_item2)
        tree_widget_item3 = QTreeWidgetItem(["PUT"])
        self.collection_tree.addTopLevelItem(tree_widget_item3)
        tree_widget_item4 = QTreeWidgetItem(["PATCH"])
        self.collection_tree.addTopLevelItem(tree_widget_item4)
        tree_widget_item5 = QTreeWidgetItem(["DELETE"])
        self.adding_collect(tree_widget_item1, tree_widget_item2 , tree_widget_item3 , tree_widget_item4 , tree_widget_item5)
        self.collection_tree.addTopLevelItem(tree_widget_item5)                  
                         
        self.history_tree = QTreeWidget(self)
        self.history_tree.setHeaderLabels(['History'])
        
        history_widget_item1 = QTreeWidgetItem(["Today"])
        self.history_tree.addTopLevelItem(history_widget_item1)
        
        history_widget_item2 = QTreeWidgetItem(["Yesterday"])
        self.history_tree.addTopLevelItem(history_widget_item2)
        
        history_widget_item3 = QTreeWidgetItem(["Last Week"])
        self.history_tree.addTopLevelItem(history_widget_item3)
        
        history_widget_item4 = QTreeWidgetItem(["Last Month"])
        self.adding(history_widget_item1 , history_widget_item2 , history_widget_item3 , history_widget_item4)
        self.history_tree.addTopLevelItem(history_widget_item4)      
    
        # initialize variable
        self.strList = np.array([])

        # add tabs
        self.tab1 = self.ui1()
        self.tab2 = self.ui2()
        self.tab3 = self.ui3()
        self.tab4 = self.ui4()
        self.tab5 = self.ui5()

        #collection tree                                            
        self.collection_tree.addTopLevelItem(tree_widget_item1)    
        self.collection_tree.addTopLevelItem(tree_widget_item2)    
        self.collection_tree.addTopLevelItem(tree_widget_item3)    
        self.collection_tree.addTopLevelItem(tree_widget_item4)    
        self.collection_tree.addTopLevelItem(tree_widget_item5)    

        #history tree
        self.history_tree.addTopLevelItem(history_widget_item1)    
        self.history_tree.addTopLevelItem(history_widget_item2)    
        self.history_tree.addTopLevelItem(history_widget_item3)     
        self.history_tree.addTopLevelItem(history_widget_item4)     


        #Back_end functions---
        self.send.clicked.connect(self.sendrequest)
        self.combo2.currentIndexChanged.connect(self.set_response_mode)
        self.save.clicked.connect(self.add_to_collection)
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

    def save_to_history(self , url , method):
            time = datetime.datetime.now()
            List = [method , url , str(time)]
            l = ','.join(List)
            with open('history.csv', 'a') as f_object:
                f_object.write(l + "\n")
                f_object.close()

    def dragEnterEvent(self, event: QDragEnterEvent):
        event.acceptProposedAction()
        def dropEvent(self, event: QDropEvent):
            path_list = [u.toLocalFile() for u in event.mimeData().rls()]
            self.dd_label.setText(f"File dropped: {path_list[0]}")

    def mousePressedEvent(self, event: QMouseEvent):
        if event.btton() == Qt.LeftButton:
            mime_data = QMimeData()
            mime_data.setText("Drag and drop a file here!")
            drag = QDrag(self)
            drag.setMimeData(mime_data)
            drag.exec__(Qt.CopyAction | Qt.MoveAction, Qt.CopyAction)

    def showFileDialog(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Open File')
        if filename:
            with open(filename, 'r') as file:
                # do something with the file
                pass

    #send button clicked
    def sendrequest(self):
        # these should be added to the programm ---{
        headers = self.header.toPlainText()
        request_body = self.body.toPlainText()
        #END }---
        url = self.url_field.text()
        method = self.combo.currentText()
        try:
            response = requests.request(
                method,
                url,
                headers=self.parse_headers(headers),
                data=request_body,
            )
            response_text = f"Status Code: {response.status_code}\n\n"
            response_text += response.text
            self.save_to_history(url , method)
        except requests.exceptions.RequestException as e:
            response_text = f"Error: {str(e)}"
        self.result_field.setText(response_text)
    #Parse Headers
    def parse_headers(self, headers):
        parsed_headers = {}
        lines = headers.split("\n")
        for line in lines:
            if ":" in line:
                key, value = line.split(":", 1)
                parsed_headers[key.strip()] = value.strip()
        return parsed_headers
    #changing the result field
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
    def showFileDialog(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Open File')
        if filename:
            with open(filename, 'r') as file:
                # do something with the file
                pass
    #add to collections
    def add_to_collection(self):
        try :
            url = self.url_field.text()
            txt = self.combo.currentText()
            response = requests.get(url)
            if response.status_code == 200:
                List = [txt , url] 
                l = ','.join(List)
                with open('collections.csv', 'a') as f_object:
                    f_object.write(l + "\n")
                    f_object.close()
        except :
            pass
    # adding to history page----
    def adding(self, history_widget_item1 , history_widget_item2 , history_widget_item3 , history_widget_item4):
        with open('history.csv', newline='') as csvfile2:
            spamreader = csv.reader(csvfile2, delimiter=' ', quotechar='|')
            for row in spamreader:
                saves.append(row[0].split(','))

        today = datetime.datetime.now().date()
        for save in saves:
            save_date = datetime.datetime.strptime(save[2], '%Y-%m-%d').date()
            delta = today - save_date
            
            if delta == datetime.timedelta(days=0):
                child_item = QTreeWidgetItem([save[0] + ',' + save[1]])
                history_widget_item1.addChild(child_item)
            
            elif delta == datetime.timedelta(days=1):
                child_item = QTreeWidgetItem([save[0] + ',' + save[1]])
                history_widget_item2.addChild(child_item)
            
            elif delta.days <= 7:
                child_item = QTreeWidgetItem([save[0] + ',' + save[1]])
                history_widget_item3.addChild(child_item)
            
            elif delta.days <= 30:
                child_item = QTreeWidgetItem([save[0] + ',' + save[1]])
                history_widget_item4.addChild(child_item)
    ##showing the collection part
    def adding_collect(self, tree_widget1, tree_widget2, tree_widget3, tree_widget4, tree_widget5):
        with open('collections.csv', newline='') as csvfile2:
            spamreader = csv.reader(csvfile2, delimiter=' ', quotechar='|')
            for row in spamreader:
                saves2.append(row[0].split(','))

        for save in saves2:
            if save[0] == "GET":
                child_item = QTreeWidgetItem([save[1]])
                tree_widget1.addChild(child_item)
            
            elif save[0] == "POST":
                child_item = QTreeWidgetItem([save[1]])
                tree_widget2.addChild(child_item)  # Add "POST" item directly to the parent
            
            elif save[0] == "PUT":
                child_item = QTreeWidgetItem([save[1]])
                tree_widget3.addChild(child_item)

            elif save[0] == "PATCH":
                child_item = QTreeWidgetItem([save[1]])
                tree_widget4.addChild(child_item)

            elif save[0] == "DELETE":
                child_item = QTreeWidgetItem([save[1]])
                tree_widget4.addChild(child_item)

                
    def ui1(self):
        upper_layout = QHBoxLayout()
        upper_layout.addWidget(self.combo)
        upper_layout.addWidget(self.url_field)
        upper_layout.addWidget(self.send)
        Vbox1_2 = QVBoxLayout()
        Vbox1_2.addWidget(self.l_header)
        Vbox1_2.addWidget(self.header)
        Vbox1_2.addWidget(self.l_body)
        Vbox1_2.addWidget(self.body)
        middle_layout = QHBoxLayout()
        middle_layout.addWidget(self.raw)
        middle_layout.addWidget(self.pretty)
        middle_layout.addStretch()
        middle_layout.addWidget(self.save)
        middle_layout.addWidget(self.combo2)
        lower_layout = QHBoxLayout()
        lower_layout.addWidget(self.result_field)
        main_layout = QVBoxLayout()
        main_layout.addLayout(upper_layout)
        main_layout.addLayout(Vbox1_2)
        main_layout.addLayout(middle_layout)
        main_layout.addLayout(lower_layout)
        main = QWidget()
        main.setLayout(main_layout)
        return main
    
    def ui2(self):
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.dd_label)
        main_layout.addWidget(self.menubar)
        main_layout.addStretch(5)
        main = QWidget()
        main.setLayout(main_layout)
        return main
    
    def ui3(self):
        upper_layout = QHBoxLayout()
        upper_layout.addWidget(self.random_combo)
        upper_layout.addWidget(self.random_line)
        upper_layout.addWidget(self.random_btn)
        inupper_layout = QVBoxLayout()
        inupper_layout.addWidget(self.random_header)
        inupper_layout.addWidget(self.random_line_header)
        inupper_layout.addWidget(self.random_body)
        inupper_layout.addWidget(self.random_line_body)
        lower_layout = QHBoxLayout()
        lower_layout.addWidget(self.random_result)
        main_layout = QVBoxLayout()
        main_layout.addLayout(upper_layout)
        main_layout.addLayout(inupper_layout)
        main_layout.addLayout(lower_layout)

        main = QWidget()
        main.setLayout(main_layout)
        return main

    def ui4(self):
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.collection_tree)
        main = QWidget()
        main.setLayout(main_layout)
        return main
   
    def ui5(self):
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.history_tree)
        main = QWidget()
        main.setLayout(main_layout)
        return main
######################################################################
class WelcomeScreen(QDialog):
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        # Loading the user interface
        loadUi("welcomescreen.ui",self)
        #connecting to Login page
        self.login.clicked.connect(self.gotologin)
        #connecting to create an account page
        self.create.clicked.connect(self.gotocreate)

    def gotologin(self):
        login = LoginScreen()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotocreate(self):
        create = CreateAccScreen()
        widget.addWidget(create)
        widget.setCurrentIndex(widget.currentIndex() + 1)

# Logging in ------------------------------
class LoginScreen(QDialog):
    def __init__(self):
        super(LoginScreen, self).__init__()
        loadUi("login.ui",self)
        #Hide the password field
        self.passwordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        #clicking login button
        self.login.clicked.connect(self.loginfunction)
        #if back clicked
        self.back.clicked.connect(self.gotowelcome)
    
    def gotowelcome(self):
        welcome = WelcomeScreen()
        widget.addWidget(welcome)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
    def check_the_account(self , usr , pasw):
        accounts = list()
        #if the fields were empty
        if len(usr) == 0 or len(pasw) == 0:
            self.error.setText("Please input all fields.")

        else :
            #opening the csv file(database)...
            with open('data.csv', newline='') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
                for row in spamreader :
                    #appending every row as a list to accounts list
                    accounts.append(row[0].split(','))
            for acc in accounts :
                if usr == acc[0] :
                    if pasw == acc[1]:
                        # if the password and username were correct
                        print('Successfully logged in.')
                        self.error.setText("")
                        csvfile.close()
                        postman = mainwindow()
                        widget.addWidget(postman)
                        widget.setCurrentIndex(widget.currentIndex()+1)
                        break   # will replace with return true and access the main app
                    else :
                        #if the password and username does not match
                        self.error.setText("Invalid username or password")
                        csvfile.close()
                        break # will replace with false 
            else :
                #if there is not such username in our csv file (database)
                self.error.setText("Invalid username or password")
                csvfile.close()
                # I will write return false

    def loginfunction(self):
        #user ans password fields
        user = self.emailfield.text()
        password = self.passwordfield.text()
        #check if the account is valid
        self.check_the_account(user , password)

#Create an account page ---------------
class CreateAccScreen(QDialog):
    def __init__(self):
        super(CreateAccScreen, self).__init__()
        loadUi("createacc.ui",self)
        #Hide password and confirm password fields
        self.passwordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmpasswordfield.setEchoMode(QtWidgets.QLineEdit.Password)

        self.signup.clicked.connect(self.signupfunction)

    def is_valid_password(self , pasw):
        if len(pasw) < 8 :
            self.error.setText("The password should contain at least 8 characters")
            return False
        # check if password have numbers or do not have numbers
        if not bool(re.search(r'\d' , pasw)):
            self.error.setText("The password should contain at least one number")
            return False
        return True
    def signupfunction(self):
        #getting username , password and confirm password from the corresponding fields
        user = self.emailfield.text()
        password = self.passwordfield.text()
        confirmpassword = self.confirmpasswordfield.text()
        #if fields were empty
        if len(user)==0 or len(password)==0 or len(confirmpassword)==0:
            self.error.setText("Please fill in all inputs.")
        
        #if password and confirm password did not match
        elif password!=confirmpassword:
            self.error.setText("Passwords do not match.")


        else:
            if self.is_valid_password(password):
                accounts = list()
                List = [user , password]
                with open('data.csv', newline='') as csvfile:
                    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
                    for row in spamreader :
                        accounts.append(row[0].split(','))
                    for acc in accounts :
                        #if username inserted exsists in csvfile(database)---
                        if acc[0] == user :
                            self.error.setText("An account with this username exists")
                            csvfile.close()
                            break
                    else :
                        #now writing the new username and password in csvfile(database)
                        l = ','.join(List)
                        with open('data.csv', 'a') as f_object:
                            f_object.write(l + "\n")
                            f_object.close()
                        #connecting to filling the profile
                        welcome = WelcomeScreen()
                        widget.addWidget(welcome)
                        widget.setCurrentIndex(widget.currentIndex()+1)
# main
# with open('collections.csv', newline='') as csvfile:
#         spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
#         for row in spamreader :
#             saves.append(row[0].split(','))
#         csvfile.close()
# with open('history.csv', newline='') as csvfile:
#         spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
#         for row in spamreader :
#             saves2.append(row[0].split(','))
#         csvfile.close()
app = QApplication(sys.argv)
app.setStyleSheet(Path('STYLE.qss').read_text())
welcome = WelcomeScreen()
widget = QtWidgets.QStackedWidget()
widget.addWidget(welcome)
widget.setFixedHeight(800)  #Can be changed
widget.setFixedWidth(1200)  #Can be changed
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exiting")
