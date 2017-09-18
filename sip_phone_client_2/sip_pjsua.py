import pjsua as pj
import socket
import threading
import os
import wave
from time import sleep

CURRENT_CALLL=None
LIB=None

class sip_pjsua():

    # <editor-fold desc="init">
    def __init__(self,call_management_dialog):
        global CURRENT_CALLL,LIB
        CURRENT_CALLL=None
        LIB=None


        self.register_ok=False
        self.account=""
        self.lib = pj.Lib()
        self.call_management_dialog=call_management_dialog



    # </editor-fold>


    # <editor-fold desc="find the a port in local,if exist,return the port else return False">
    def IsOpen(self,ip, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((ip, int(port)))
            s.shutdown(2)
            s.close()
            return False
        except socket.error as e:
            return True

    def find_free_port(self,ip, port_start=5000, port_end=20000):
        for port in range(port_start, port_end + 1):
            if self.IsOpen('localhost', port):
                free_port = port
                return free_port
        return False
    # </editor-fold>

    # <editor-fold desc="the message for return back">

    class Return_Message():

        def __init__(self,is_ok,message):
            self.IsOk=is_ok
            self.Message=message
    # </editor-fold>

    # <editor-fold desc="the log callback">
    def log_cb(self, level, str, len):
        print('--------------------------------------------------------------------------------------------------')
        print(str)

    def cb_func(self, pid):
        global current_call
        print('%s playback is done' % pid)
        if current_call:
            current_call.hangup()
    # </editor-fold>

    # <editor-fold desc="the Account callback which is userd for account register and the incoming call">
    class MyAccountCallback(pj.AccountCallback):
        sem = None

        def __init__(self, account=None,playAudiofunction=None,call_management_dialog=None):
            pj.AccountCallback.__init__(self, account)
            self.PlayAudio=playAudiofunction
            self.call_management_dialog=call_management_dialog

        def wait(self):
            self.sem = threading.Semaphore(0)
            self.sem.acquire()

        def on_reg_state(self):
            if self.sem:
                if self.account.info().reg_status >= 200:
                    self.sem.release()

        def on_incoming_call(self, call):
            global CURRENT_CALLL
            if CURRENT_CALLL:
                call.answer(486, "Busy")
                return

            CURRENT_CALLL = call
            self.play_id = self.PlayAudio("incomingcall")
            call_cb = sip_pjsua.MyCallCallback(CURRENT_CALLL,playAudiofunction=self.PlayAudio,incomingcall_playid=self.play_id,call_management_dialog=self.call_management_dialog)
            CURRENT_CALLL.set_callback(call_cb)
            CURRENT_CALLL.answer(180)
            call_number = CURRENT_CALLL._obj_name.split(':')[1].split('@')[0]
            self.call_management_dialog.SetValue("incomingcall",call_number)
            self.call_management_dialog.start()

           #
           # self.PlayAudio("incomingcall")
            #mycallback

    # </editor-fold>

    # <editor-fold desc="the call callback which is userd for call">
    class MyCallCallback(pj.CallCallback):
        def __init__(self, call=None,playAudiofunction=None,incomingcall_playid=None,call_management_dialog=None):
            pj.CallCallback.__init__(self, call)
            self.PlayAudio = playAudiofunction
            self.play_id = incomingcall_playid
            self.call_management_dialog=call_management_dialog


        def on_state(self):
            global  CURRENT_CALLL
            global current_call,mycallback
            if self.call.info().state == pj.CallState.DISCONNECTED:
                self.call_management_dialog.SetValue("cancel")
                self.call_management_dialog.start()
                CURRENT_CALLL = None
                if self.play_id!=None:
                    self.PlayAudio("destory", self.play_id)
                    self.play_id=None

            elif self.call.info().state == pj.CallState.CONFIRMED:
                CURRENT_CALLL=self.call
                self.call_management_dialog.SetValue("accept")
                self.call_management_dialog.start()
                if self.play_id!=None:
                    self.PlayAudio("destory", self.play_id)
                    self.play_id = None
            elif self.call.info().state==pj.CallState.CALLING:
                CURRENT_CALLL = self.call
                call_number = self.call._obj_name.split(':')[1].split('@')[0]
                self.play_id=self.PlayAudio("outcall")
                self.call_management_dialog.SetValue("outcall",call_number)
                self.call_management_dialog.start()
            # elif self.call.info().state==pj.CallState.INCOMING:
            #     CURRENT_CALLL.answer(180)
            #     self.play_id = self.PlayAudio("incomingcall")
            #     print(self.play_id)


        def on_media_state(self):
            global LIB
            if self.call.info().media_state == pj.MediaState.ACTIVE:
                try:
                    call_slot = self.call.info().conf_slot
                    LIB.conf_connect(call_slot, 0)
                    LIB.conf_connect(0, call_slot)
                except pj.Error as e:
                    print("Exception: " + str(e))
            else:
                pass
    # </editor-fold>



    # <editor-fold desc="Play autio file">
    def Play_audio_file(self,autio_file,des_slot,loop):

        swav_player_id = LIB.create_player(autio_file, loop=loop)
        wav_slot = LIB.player_get_slot(swav_player_id)
        LIB.conf_connect(wav_slot, des_slot)
        return  swav_player_id

    def AudioPlayer(self,state,player_id=None):
        global  CURRENT_CALLL,LIB
        if state=="incomingcall":
            call_slot = 0
            player_id=self. Play_audio_file(autio_file='Incomingcall.wav',des_slot=call_slot,loop=True)

        elif state=="outcall":
            call_slot = 0
            player_id=self.Play_audio_file(autio_file='Outcall.wav', des_slot=call_slot, loop=True)

        elif state=="keyclick":
            call_slot = 0
            player_id = self.Play_audio_file(autio_file='Keytone.wav', des_slot=call_slot, loop=False)

        elif state=="destory":
            LIB.player_destroy(player_id)
        return player_id
    # </editor-fold>

    def call_control(self,state):
        global CURRENT_CALLL
        if state=="cancel":
            if CURRENT_CALLL:
                CURRENT_CALLL.hangup()
                CURRENT_CALLL=None

        elif state=="accept":
            if CURRENT_CALLL:
                CURRENT_CALLL.answer(200)

   #def current_call_

    # <editor-fold desc="find the port for register the account,and register the account in the server">
    def set_account(self, ip, username, password):
        port=self.find_free_port('127.0.0.1')
        if (port):
            result=self.creat_account(ip, username, password, port)
        else:
            result=self.Return_Message(False,"No free port in local in rang(5000,20000)")
        return result
    #assign the self variable lib acc account register_ok
    def creat_account(self, ip, username, password, port):
        global LIB
        try:
            self.lib.init(log_cfg=pj.LogConfig(level=4, callback=self.log_cb))
            self.lib.create_transport(pj.TransportType.UDP, pj.TransportConfig(port))
            self.lib.start()
            LIB=self.lib
            acc_cfg = pj.AccountConfig()
            acc_cfg.id = "sip:" + username + "@" + ip
            acc_cfg.reg_uri = "sip:" + ip
            acc_cfg.proxy = [acc_cfg.reg_uri]
            acc_cfg.auth_cred = [pj.AuthCred("*", username + "@" + ip, password)]
            acc_cb = self.MyAccountCallback(playAudiofunction=self.AudioPlayer,call_management_dialog=self.call_management_dialog)
            self.acc = self.lib.create_account(acc_cfg, cb=acc_cb)
            self.register_ok = True
            self.account = username
            self.ip=ip
            message = self.Return_Message(self.register_ok, None)
        except pj.Error as  e:
            self.register_ok = False
            message = self.Return_Message(self.register_ok, e)
        return message

    # </editor-fold>


    def MakeCall(self,number):
        global CURRENT_CALLL
        try:
            call_url= "sip:" + number + "@" + self.ip
            CURRENT_CALLL = self.acc.make_call(call_url, cb=self.MyCallCallback(playAudiofunction=self.AudioPlayer,call_management_dialog=self.call_management_dialog))
            message=self.Return_Message(True,None)
        except pj.Error as e:
            message = self.Return_Message(False, str(e))
        return message






























