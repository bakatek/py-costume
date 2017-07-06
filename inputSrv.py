'''
Created on 15 dec. 2015
@author: epelorce
'''

import os
from time import sleep
from threading import Thread
from storageCtrl import storageCtrl
if storageCtrl.getIsWindows():
    import evdev

class inputSrv(Thread):
    '''
    classdocs
    '''
    def out(self, _txt):
        self.utils_c.echo("inputSrv:> "+_txt)
        
    def __init__(self, _utils_c, _refresh=1):
        super(inputSrv,self).__init__()
        #self.storageCtrl_t = _storageCtrl
        self.utils_c = _utils_c
        self.refreshRate = _refresh
        
        self.out("init inputSrv")
        
    def stop(self):
        self.out("stop inputSrv")
        storageCtrl.removeThreadToStop(self)
    
    def run(self):
        self.out("start inputSrv")
        storageCtrl.addThreadToStop(self)
        
        
        working_device = None
        
        while storageCtrl.getStopRequested() == False:
            try:
                devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
                for device in devices:
                    # /dev/input/event1    USB Keyboard        usb-0000:00:12.1-2/input0
                    if device.fn.find("Keyboard") != -1:
                        working_device = device;
                    print(device.fn, device.name, device.phys)
                if working_device:
                    for event in device.read_loop():
                        my_key = None
                        if event.type == evdev.ecodes.EV_KEY:
                            print(categorize(event))
                            if categorize(event).find("KEY_") and categorize(event).find("up") :
                                my_key = categorize(event).split(" (KEY_")[1].split("),")[0].lower()
                        if storageCtrl.getStopRequested() == True:
                            break;
                        if my_key:
                            allKWandCommands = storageCtrl.getkeywordsAndCommands()
                            for [kw, kb, command, gpio] in allKWandCommands:
                                if my_key == kb:
                                    if command != "":
                                        storageCtrl.pushWebRequest(command)
                                    elif gpio != "":
                                        storageCtrl.pushGpioRequest(gpio)
                else:
                    CMD = "echo -e 'power on\nconnect \t \nquit' | bluetoothctl"
                    self.utils_c.execute_cmd(CMD)
            except:
                self.out("Error on keypressed")
            # print(".2")
            sleep(self.refreshRate)
        my_kb.set_normal_term()
        storageCtrl.stopAcheived = storageCtrl.getStopAcheived() - 1
