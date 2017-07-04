'''
Created on 15 dec. 2015
@author: epelorce
'''

import time
import Adafruit_PCA9685
from storageCtrl import storageCtrl

class gpioEx(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.storageCtrl_t = storageCtrl
        # Initialise the PCA9685 using the default address (0x40).
        self.pwm = Adafruit_PCA9685.PCA9685()

        # Alternatively specify a different address and/or bus:
        #pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)

        # Configure min and max servo pulse lengths
        self.servo_min = 150  # Min pulse length out of 4096
        self.servo_max = 600  # Max pulse length out of 4096
        # Set frequency to 60hz, good for servos.
        self.pwm.set_pwm_freq(60)

        
    def get_pulse_from_percent(self, _percent):
        return ((_percent * (self.servo_max - self.servo_min))/ 100) + self.servo_min
    
    # Helper function to make setting a servo pulse width simpler.
    def set_servo_pulse(self, channel, pulse):
        pulse_length = 1000000    # 1,000,000 us per second
        pulse_length //= 60       # 60 Hz
        print('{0}us per period'.format(pulse_length))
        pulse_length //= 4096     # 12 bits of resolution
        print('{0}us per bit'.format(pulse_length))
        pulse *= 1000
        pulse //= pulse_length
        self.pwm.set_pwm(channel, 0, pulse)
        
    def move_servo(self, channel, position):
        pwm.set_pwm(channel, 0, self.get_pulse_from_percent(position))
        time.sleep(1)
        pwm.set_pwm(channel, 0, 0)
            