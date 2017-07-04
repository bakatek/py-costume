'''
Created on 15 dec. 2015
@author: epelorce
'''

import time
#import Adafruit_PCA9685
from storageCtrl import storageCtrl
if not storageCtrl.getIsWindows():
    import Adafruit_PCA9685
    from pyA20.gpio import gpio
    from pyA20.gpio import port
    
class gpioEx(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.storageCtrl_t = storageCtrl
        if not storageCtrl.getIsWindows():
            # Initialise the PCA9685 using the default address (0x40).
            self.pwm = Adafruit_PCA9685.PCA9685()
            #initialize the gpio module
            gpio.init()

        # Alternatively specify a different address and/or bus:
        #pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)

        # Configure min and max servo pulse lengths
        self.servo_min = 150  # Min pulse length out of 4096
        self.servo_max = 600  # Max pulse length out of 4096
        if not storageCtrl.getIsWindows():
            # Set frequency to 60hz, good for servos.
            self.pwm.set_pwm_freq(60)

        
    def get_pulse_from_percent(self, _percent):
        return ((int(_percent) * (int(self.servo_max) - int(self.servo_min)))/ 100) + int(self.servo_min)
    
    # Helper function to make setting a servo pulse width simpler.
    def set_servo_pulse(self, channel, pulse):
        pulse_length = 1000000    # 1,000,000 us per second
        pulse_length //= 60       # 60 Hz
        print('{0}us per period'.format(pulse_length))
        pulse_length //= 4096     # 12 bits of resolution
        print('{0}us per bit'.format(pulse_length))
        pulse *= 1000
        pulse //= pulse_length
        if not storageCtrl.getIsWindows():
            self.pwm.set_pwm(channel, 0, pulse)
        else:
            print(">> PWM >> channel:" + str(channel) + " pulse:" + str(pulse))
            
    def move_servo(self, channel, position):
        channel = int(channel)
        position = int(position)
        if not storageCtrl.getIsWindows():
            pwm.set_pwm(channel, 0, self.get_pulse_from_percent(position))
        else:
            print(">> PWM >> channel:" + str(channel) + " position:" + str(position) + " pulse:"+str(self.get_pulse_from_percent(position)))
        time.sleep(1)
        
        if not storageCtrl.getIsWindows():
            pwm.set_pwm(channel, 0, 0)
            
    def set_gpio(self, gpioId, val):
        if storageCtrl.getIsWindows():
            print(">> GPIO >> ID:%s VAL:%s", gpioId, val)
            return
        #setup the port (same as raspberry pi's gpio.setup() function)
        gpio.setcfg(port[gpioId], gpio.OUTPUT)

        #now we do something (light up the LED)
        if val == 1:
            gpio.output(port[gpioId], gpio.HIGH)
        else:
            gpio.output(port[gpioId], gpio.LOW)