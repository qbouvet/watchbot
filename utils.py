#! /usr/bin/python3

import picamera
import time
import datetime
import subprocess
import io

    # Homemade bits
from config import * 

"""
    Misceleanous util function

    Author : Quentin Bouvet
"""

def stamp(text, name=None, do_print=True ) : 
    now=datetime.datetime.now()
    #msg = "[{:02d}:{:02d}:{:02d}@{:02d}/{:02d}] ".format(now.hour, now.minute, now.second, now.day, now.month) 
    msg = "[{:02d}:{:02d}:{:02d}] ".format(now.hour, now.minute, now.second) 
    if not name is None : 
        msg = msg + "{:.<17} ".format(name)
    msg = msg + text
    if do_print : 
        print(msg, flush=True)
    else : 
        return msg

def debug(text, name=None, do_print=True) : 
    if DEBUG : 
        stamp(text, name=name, do_print=do_print)

def get_pub_ip () : 
        # Alternatives :    curl ipinfo.io/ip
        #                   curl -s checkip.dyndns.org | sed -e 's/.*Current IP Address: //' -e 's/<.*$//'
    try :
        res = subprocess.check_output(['curl', '-s', 'ipinfo.io/ip'])
        res = res.decode('utf-8')
        res = res[:-1]
    except Exception as e : 
        res = ''.join(["Could not obtain public ip : ", str(e)])
    return res


''' Simulates a video stream from a file by slowing the file read rate 
    to the specified bitrate.
    Rudimentary, made for testing
'''
class DelayedBytesIo : 
    
    def __init__(self, filename, bytesPer100ms) : 
        self.file = open(filename, "rb")
        self.rate = bytesPer100ms
    
    def read(self, n=-1) : 
        buffered = b''
        while(n>0) : 
            buffered += self.file.read(self.rate)
            n = n-self.rate
            time.sleep(0.1)
        return buffered
     

def photo(camera, filename) : 
    camera.resolution = RES_PHOTO
    camera.start_preview()
        # Camera warm-up time
    stamp("Warming up camera")
    time.sleep(CAM_WARMUP_TIME)
        # recording
    stamp("Capturing image")
    camera.capture(filename+".jpg")
    stamp("Image has been captured\n")

def video(camera, filename) : 
    camera.resolution = RES_VIDEO
    camera.start_preview()
        # Camera warm-up time
    stamp("Warming up camera")
    time.sleep(CAM_WARMUP_TIME)
        # recording
    stamp("recording")
    camera.start_recording(filename+".h264")
    camera.wait_recording(6)
    camera.stop_recording()
    stamp("Recording finished\n")
