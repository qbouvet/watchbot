#! /usr/bin/python3


from config import * 
from utils import *

import RPi.GPIO as GPIO
import time


"""
    TODO : handle multiple callbacks in here

	Author : Quentin Bouvet
"""
    
class PIRManager : 
    
    def __init__(self) :  
        #try :
        #    GPIO.cleanup()
        #    time.sleep(0.5)
        #except : 
        #    print("")
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(PIR_pin, GPIO.IN)
        self.callbacks = []
        GPIO.add_event_detect(PIR_pin, GPIO.RISING, callback=self.global_callback)
    
    def add_callback(self, callbackFunction) : 
        self.callbacks.append(callbackFunction)
        debug("PIR GPIO : adding callback : "+str(self.callbacks))
    
    def global_callback(self, pin) : 
        debug("PIR GPIO : Running callbacks ... ")
        for f in self.callbacks : 
            f(pin)
        debug("PIR GPIO : callbacks done")
    
    def cleanup(self) : 
        GPIO.cleanup()
    



