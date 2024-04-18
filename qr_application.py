import os
import json
import time
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1376, 1068)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(0, 0, 1381, 1011))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(400, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        
        
        self.photo = QtWidgets.QLabel(self.widget)
        self.photo.setText("")
        self.photo.setScaledContents(True)
        self.photo.setObjectName("photo")
        self.horizontalLayout.addWidget(self.photo)
        
        self.gif = QtGui.QMovie("qr_test.gif")
        
        spacerItem1 = QtWidgets.QSpacerItem(400, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1376, 32))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.text_value = ""
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        MainWindow.setStyleSheet("background-color: #11313F;")

    def text_update(self):
        self.label.setText("you clicked the button")
        self.update()
        self.label.adjustSize()

    def show_tick(self):
        self.filename = os.path.join(self.CURRENT_DIRECTORY, "assets/tick.jpg")
        self.photo.setPixmap(QtGui.QPixmap(self.filename))    

    def clear_json(self):
        data = {
            "name": " "
        }
        file_path = 'qr_test.json'

        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)

    def stop_gif_animation(self):
        self.clear_json()
        self.gif.stop()
        self.photo.clear()

    def read_json(self):
        file_path = 'qr_test.json'  # Replace 'your_file.json' with your JSON file path
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                json_data = json.load(f)
                name = json_data.get('name', '')  # Get the name field from JSON data
                if name != " ":
                    self.photo.setMovie(self.gif)
                    self.gif.start()
                    QtCore.QTimer.singleShot(6000, self.stop_gif_animation)
                    # time.sleep(5)
                    # self.clear_json()
                    # self.photo.setMovie(self.gif)
                    # self.gif.stop()

                self.label.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:22pt; color:#73d216;\">"+name+"</span></p></body></html>")

        else:
            self.label.setText('')

        QtCore.QTimer.singleShot(1000, self.read_json)  # Schedule next read in 1 second

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:22pt; color:#73d216;\">"+str(self.text_value)+"</span></p></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.read_json()  # Start reading JSON file
    MainWindow.show()
    sys.exit(app.exec_())
