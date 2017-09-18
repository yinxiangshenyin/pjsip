from sip_dial import Ui_MainWindow
from sip_callinfo import Ui_sip_callinfo
from PyQt5 import QtWidgets
from PyQt5 import QtCore, QtGui
import sip_pjsua
import sys
import threading


class MainForm(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(MainForm, self).__init__()
        self.setupUi(self)
    def pushButton_Click(self):
        global MY_SIP_CLIENT
        sender=self.sender()
        if sender.text()!="呼叫":
            MY_SIP_CLIENT.AudioPlayer("keyclick")
            call_number=self.lineEdit.text()
            self.lineEdit.setText(call_number+sender.text())
        else:
            if self.lineEdit.text()!="":

                MY_SIP_CLIENT.MakeCall(self.lineEdit.text())
                # MakingCall

class Call_Dialog(QtWidgets.QDialog,Ui_sip_callinfo):
    def __init__(self,state,number):
        super(Call_Dialog, self).__init__()
        self.setupUi(self)
        if state=="outcall":
            self.pushButton_Answer.setVisible(False)
        self.Call_number.setText(str(number))
    def PushButton_Click(self):
        global MY_SIP_CLIENT
        sender=self.sender()
        if sender.text()=="取消":
            MY_SIP_CLIENT.call_control("cancel")
        elif sender.text()=="接听":
            MY_SIP_CLIENT.call_control("accept")
    def closeEvent(self, QCloseEvent):
        global MY_SIP_CLIENT
        MY_SIP_CLIENT.call_control("cancel")




class QThread(QtCore.QThread):
    My_signal = QtCore.pyqtSignal(str, str)
    def __init__(self, parent=None):
        super(QThread, self).__init__(parent)

    def SetValue(self,message,number=None):
        self.message=message
        self.number=str(number)
    def run(self):
        self.My_signal.emit(self.message,self.number)


def error_message(self,message):
    QtWidgets.QMessageBox.critical(self, "Critical",self.tr(message))


    #


def call_management(state,number=None):
    global CALL_DIALOG,WINDOWS
    thread = threading.current_thread()
    print('thread.getName=' + thread.getName())
    if state=="outcall" or state=="incomingcall":
        try:
            CALL_DIALOG=Call_Dialog(state=state,number=number)
            CALL_DIALOG.show()
            CALL_DIALOG.exec_()
        except:
            pass
    if state=="cancel":
        CALL_DIALOG.destroy()
        WINDOWS.lineEdit.setText("")
    if state=="accept":
        CALL_DIALOG.pushButton_Answer.setVisible(False)
        CALL_DIALOG.Call_number=number




Qthread = QThread()
Qthread.My_signal.connect(call_management)

MY_SIP_CLIENT=sip_pjsua.sip_pjsua(Qthread)
MY_SIP_CLIENT.set_account('192.168.1.17','2605','Sztttxsbc')
CALL_DIALOG=None
app = QtWidgets.QApplication(sys.argv)
WINDOWS = MainForm()
WINDOWS.show()


sys.exit(app.exec_())

