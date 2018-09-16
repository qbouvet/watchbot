#! /usr/bin/python3
    
    # multiprocessing
import multiprocessing
from threading import Thread
    # Thread's own IO loop (butwhy.jpg?)
import asyncio
    # pi camera stream
import io
import picamera
    # Error handling
from tornado.iostream import StreamClosedError
from tornado.websocket import WebSocketClosedError

    # homemade bits
from streamsplitter import StreamSplitter
from utils import *
from config import * 


"""

	Author : Quentin Bouvet
"""

class CameraWrapper : 

    def __init__(self) : 
        self.streamprocess = None
        self.camera = None
        self.camstream = None
        self.streamsplitter = None
    
    def shutdown(self) : 
        stamp("Shutting down ...", name="CameraWrapper") 
        if not self.streamprocess is None :
            if self.streamprocess.is_alive() : 
                self.streamprocess.terminate()
                self.streamprocess.join()
                self.streamprocess = None
                stamp("    streamprocess terminated", name="CameraWrapper") 
        if not self.camera is None : 
            # most important for power saving
            self.camera.close()
            self.camera = None
            stamp("    picamera closed", name="CameraWrapper") 
        if not self.camstream is None : 
            self.camstream = None
        if not self.streamsplitter is None : 
            self.streamsplitter = None
        stamp("Done", name="CameraWrapper") 
    
    def save_picture(self, filename) : 
        stamp("Not implemented")

    def start_stream(self, callbackFunction) :
        
        debug("start_stream() called", name="camerawrapper")
            
        if not self.streamsplitter is None : 
            stamp("CameraWrapper::stream_to_websocket() : streamsplitter exists already")
            return
        self.streamsplitter = StreamSplitter(STREAM_SEPARATOR, callbackFunction)
        
        if not self.camstream is None : 
            stamp("CameraWrapper::stream_to_websocket() : camstream is already opened")
            return
        self.camstream = FifoBytesIO()
        #   For testing, use : 
        #self.camstream = DelayedBytesIo("sample2.h264", 50000)
        
        if self.camera is None : 
            self.camera = picamera.PiCamera()
        self.camera.resolution = RES_VIDEO
        self.camera.framerate = CAM_FPS
        debug("starting recording", name="camerawrapper")
        self.camera.start_recording(self.camstream, format='h264', profile='baseline')
        debug("recording didn't block", name="camerawrapper")
        
            # Multiprocess stuff
            #
        def _process_stream(bytesStream, streamsplitter) : 
            stamp("Starting  _process_stream")
            asyncio.set_event_loop(asyncio.new_event_loop())
            try : 
                while True : 
                    buffered = bytearray(bytesStream.read(CAMERA_WRAPPER_BUFFER_SIZE))
                    streamsplitter.process(buffered)
                    time.sleep(0.5 * (1/CAM_FPS))
            except Exception as e : 
                stamp("CameraWrapper::_process_stream() : closed with Exception : \n"+repr(e))
                exit()
                
        self.streamprocess = Thread(target=_process_stream, args=(self.camstream, self.streamsplitter))
        self.streamprocess.daemon = True
        self.streamprocess.start()


''' A socket-like, "file-like as far as picamera is concerned" object 
    that can write the video stream from the camera and read it to the 
    socket-streaming process in a FIFO manner.
    
    Source : 
        https://stackoverflow.com/questions/33395004/python-streamio-reading-and-writing-from-the-same-stream
'''
class FifoBytesIO : 
    
    def __init__(self, inputBytes=b''):
        self.buf = inputBytes
        
    def read(self, n=-1):
        inp = io.BytesIO(self.buf)
        b = inp.read(n)
        self.buf = self.buf[len(b):]
        return b
        
    def readinto(self, b):
        inp = io.BytesIO(buf)
        l = inp.readinto(b)
        self.buf = self.buf[l:]
        return l
        
    def write(self, b):
        outp = io.BytesIO()
        l = outp.write(b)
        self.buf += outp.getvalue()
        return l
        
    def getvalue(self):
        return self.buf



''' This could simplify the desing of the streaming part by simply 
    writing to the socket at each new frame (eliminating reading into 
    buffers, sleeping, ...) but it doesn't work yet.
    
    It is a "file-like object as far as picamera is concerned"
    https://picamera.readthedocs.io/en/release-1.10/recipes2.html#custom-outputs
'''
class CallbackBytesIo :
    
    def __init__(self, callbackFunction):
        self.callback = callbackFunction
        
    def write(self, bytesString):
        # TODO : do streamsplitter.process() here ?
        print("callbacking")
        self.callback(bytesString)
        print("callbacked")
        return len(bytesString)
