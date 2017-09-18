# coding=utf-8
__author__ = 'a359680405'

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import threading


class mythread(QThread):
    send=pyqtSignal(str,int)
    def __int__(self):
        super(mythread, self).__init__()
    def setValue(self,state,number):
        self.state=state
        self.number=number
    def run(self):
        thread = threading.current_thread()
        print('run.getName=' + thread.getName())
        self.send.emit(self.state,self.number)

def get(state,number):
    thread = threading.current_thread()
    print('get.getName=' + thread.getName())
    print(state+str(number))

def work():
    thread = threading.current_thread()
    print('work.getName=' + thread.getName())
    testthread = threading.Thread(target=work2, args=(workThread,))
    testthread.start()

def work2(myworkThread):
    thread = threading.current_thread()
    print('work2.getName=' + thread.getName())
    myworkThread.setValue("ceshi", 123)
    myworkThread.start()


app = QApplication([])
top = QWidget()
layout = QVBoxLayout(top)  # 垂直布局类QVBoxLayout；
button = QPushButton("测试")
layout.addWidget(button)
button.clicked.connect(work)


workThread = mythread()
workThread.send.connect(get)
testthread=threading.Thread(target=work2,args=(workThread,))

top.show()
app.exec()