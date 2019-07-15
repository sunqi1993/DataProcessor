from PyQt5.QtWidgets import QWidget,QApplication,QGraphicsScene
from PyQt5.QtWidgets import *
from PyQt5.Qt import QStandardPaths
from PyQt5 import QtGui
from Form import Ui_MainWindow
from datetime import datetime
from PyQt5.QtCore import pyqtSlot,QSettings
import pandas as pd
import sys,os,logging

def process_data(file_path,out_file_dir=""):
    now=datetime.now()
    timeStr=now.strftime("_%Y-%m-%d_%H时%M分")
    out_file_name='';
    if out_file_dir=='':
        out_file_name="./data"+timeStr+".csv"
    else:
        out_file_name=out_file_dir+"/data"+timeStr+".csv"
    s = pd.read_csv(file_path, skiprows=18)
    res = s.query("(Evnt_Name=='Whisker - Display Image' and Group_ID==6) or (Evnt_Name=='Touch Down Event' and Group_ID==7 and Arg2_Name!='(NoImageOrVideo)')")
    print(res)
    res = res.sort_values(by=['Evnt_Time', 'Arg1_Value'])
    res.to_csv(out_file_name, sep=',', header=True, index=False)
    return os.path.abspath(out_file_name)

#用于处理日志的模块
class QPlainTextEditLogger(logging.Handler):
    def __init__(self, parent):
        super().__init__()
        self.widget = parent.plainTextEdit
        self.widget.setReadOnly(True)

    def emit(self, record):
        msg = self.format(record)
        self.widget.appendPlainText(msg)

class MyForm(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(MyForm, self).__init__()
        self.setupUi(self)
        self.btn1.clicked.connect(self.openCSV_file)
        self.btn2.clicked.connect(self.select_outDir)
        self.btn.clicked.connect(self.process)
        self.lineEdit_2.returnPressed.connect(self.LineEditEnter)

        logTextBox=QPlainTextEditLogger(self)
        logTextBox.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logging.getLogger().addHandler(logTextBox)
        # You can control the logging level
        logging.getLogger().setLevel(logging.DEBUG)

        self.readSetting()

    def openCSV_file(self):
        self.file_name = QFileDialog.getOpenFileName(self, "open file dialog", self.DesktopPath(),
                                                "CSV files(*.csv)")[0]
        ##"open file Dialog "为文件对话框的标题，第三个是打开的默认路径，第四个是文件类型过滤器
        self.lineEdit.setText(self.file_name)
        logging.info(f"选择待处理文件：{self.file_name}")

    def select_outDir(self):
        self.dirName=directory1 = QFileDialog.getExistingDirectory(self,
                  "选取文件夹",
                  "./")       #起始路径
        self.lineEdit_2.setText(self.dirName)
        logging.info(f"选择输出文件目录：{self.dirName}")

    def LineEditEnter(self):
        self.dirName=self.lineEdit_2.text()
        logging.info(f"选择输出文件目录：{self.dirName}")
        return

    @pyqtSlot(result=str)
    def DesktopPath(self):
        return QStandardPaths.writableLocation(QStandardPaths.DesktopLocation)

    #读取上次使用的路径信息
    def readSetting(self):
        self.setting=QSettings("Data Processor","sunqi")

        self.file_name=self.setting.value("file_name","")
        self.file_name=self.file_name if os.path.exists(self.file_name) else ""
        self.lineEdit.setText(self.file_name)

        self.dirName=self.setting.value("dir_name","")
        self.dirName=self.dirName if os.path.exists(self.dirName) else self.DesktopPath()
        self.lineEdit_2.setText(self.dirName)
        logging.info("读取上次记录完毕")
    #退出时候保存数据
    def writeSetting(self):
        file_name1 = self.file_name if os.path.exists(self.file_name) else ""
        self.setting.setValue("file_name",file_name1)
        DirName = self.dirName if os.path.exists(self.dirName) else self.DesktopPath()
        self.setting.setValue("dir_name",DirName)
        logging.info("存储本次记录完毕")

    def closeEvent(self, event):
        self.writeSetting()

    def process(self):
        try:
            assert os.path.exists(self.file_name)
        except:
            logging.warning(f"待处理文件的路径:{self.file_name} 不存在")
            # self.textEdit.setText(f"待处理文件的路径:{self.file_name} 不存在")
            return
        if  not os.path.exists(self.dirName):
            os.makedirs(self.dirName)

        file=process_data(self.file_name,self.dirName)
        logging.info(f"文件处理结果已经写入到 {file}")
if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo =MyForm()
    demo.show()
    sys.exit(app.exec_())