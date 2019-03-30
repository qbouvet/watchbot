#! /usr/bin/python3


from config import * 
from utils import *

import RPi.GPIO as GPIO
import time


"""

    Author : Quentin Bouvet
"""
    
class PIRManager : 
    
    def __init__(self, cyclePeriod) :  
        #try :
        #    GPIO.cleanup()
        #    time.sleep(0.5)
        #except : 
        #    print("")
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(PIR_pin, GPIO.IN)
        self.callbacks = []
        self.cyclePeriod = int(cyclePeriod);
        self.lastCallbackTimestamp = int(time.perf_counter());
        GPIO.add_event_detect(PIR_pin, GPIO.RISING, callback=self.global_callback)
        debug("PIR GPIO : init lastCallbackTimestamp to "+str(self.lastCallbackTimestamp))
        debug("PIR GPIO : init cyclePeriod to "+str(self.cyclePeriod))
    
    def add_callback(self, callbackFunction) : 
        self.callbacks.append(callbackFunction)
        debug("PIR GPIO : adding callback : "+str(self.callbacks))
    
    def global_callback(self, pin) : 
        if (int(time.perf_counter()) < int(self.lastCallbackTimestamp) + self.cyclePeriod) : 
            debug("PIR GPIO : Skipping callbacks, not enough time since last callbacks ... ")            
        else : 
            debug("PIR GPIO : Running callbacks ... ")
            for f in self.callbacks : 
                f(pin)
            debug("PIR GPIO : callbacks done")
            self.lastCallbackTimestamp = int(time.perf_counter());
    
    def cleanup(self) : 
        GPIO.cleanup()
    



