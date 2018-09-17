#! /usr/bin/python3

    # Tornado http server
import tornado.ioloop
import tornado.web
    # Tornado websocket server
from tornado.websocket import WebSocketHandler
import json
    # paths
import os
    # multiprocessing
import multiprocessing
from threading import Thread
    # Thread's own IO loop
import asyncio
    # Camera subprocess - raspivid version
from tornado.process import Subprocess
from tornado.ioloop import IOLoop
from tornado.iostream import StreamClosedError
from tornado import gen
    
    # homemade bits
from utils import *
from config import * 
from streamsplitter import StreamSplitter
from camerawrapper import CameraWrapper



"""
    
    Tornado websockets : 
        http://www.tornadoweb.org/en/stable/websocket.html#tornado.websocket.WebSocketHandler.write_message
    Tornado subprocess / callback examples : 
        https://pythonexample.com/code/tornado-subprocess-callback/

	Author : Quentin Bouvet
"""


    #
    # This is both the HTTP and websocket stream server
    #
class WebServerApp (Thread) : 
    
    def __init__ (self, camerawrapper) :
        Thread.__init__(self)
        self.daemon=True
        self.app = tornado.web.Application(
            [   (r"/websocket", StreamHandler, {'camerawrapper' : camerawrapper}),
                (r"/(.*)", tornado.web.StaticFileHandler, {"path": STATIC_WEB_RESSOURCES, "default_filename": "index.html"})
            ]
            #,websocket_ping_interval=WS_PING_INTERVAL
            #,websocket_ping_timeout=WS_NB_PING_TIMEOUT
        )
        self.port = 8384
        self.process = None

    def run (self) : 
        asyncio.set_event_loop(asyncio.new_event_loop())
        self.app.listen(self.port)
        tornado.ioloop.IOLoop.instance().start()



class StreamHandler (WebSocketHandler) : 
    
        # https://stackoverflow.com/questions/49627836/how-to-pass-arguments-to-tornados-websockethandler-class
    def initialize(self, camerawrapper, **kwargs) : 
        super().initialize(**kwargs)
        '''    # fields for the raspivid stream version
        self.xres, self.yres = RES_VIDEO
        self.fps=CAM_FPS
        self.streamproc=None
        self.streamsplitter = StreamSplitter(stream_separator, self._write_binary)
        '''
            # fields for the camerawrapper stream version
        self.xres, self.yres = RES_VIDEO
        self.fps=CAM_FPS
        self.camera=camerawrapper
    
    def open(self):
        stamp("WebSocket : new client")
            # Send initialization data to the client
        def alias_json_stringify (some_dict) : 
            return json.dumps(some_dict, separators=(',',':'))
        init_params = {"action":"init","width":self.xres,"height":self.yres}
        self.write_message(alias_json_stringify(init_params))
        
    def on_close(self):
        stamp("WebSocket closing")
        self.camera.shutdown()

    def on_message(self, message):
        cmd = str(message)
        stamp("RCVD : "+cmd)
        action = cmd.split(' ')[0]
            # switch(action) : 
        case = {
          'REQUESTSTREAM'   : self._start_stream, 
          'STOPSTREAM'      : self._stop_stream
        }.get(action, lambda : stamp("invalid action : "+action))()
    
    
        #
        # Private helpers
        #
    
    def _start_stream (self) : 
        debug("_start_stream() called", name="webserver")
        self.camera.start_stream(self._write_binary)
    
    def _stop_stream (self) : 
        self.camera.shutdown()
    
    def _write_binary(self, message) : 
        self.write_message(message, binary=True)
        debug("pushed " + str(len(message)) + " bytes", name="Websocket")
        
        
    ''' Raspivid subprocess version
        legacy stuff, used for debug, kept for reference
    '''
    def _start_feed_raspivid(self) : 
            #       The streaming part can be tested independantly of the raspivid command : 
            #    (1) make a test sample.h264 with 'raspivid -t 0 -o - -w 1296 -h 972 -fps 12 -pf baseline > sample.h264'
            #    (2) cmd = ['sh', '-c', 'cat /opt/camera/sample.h264 | pv -L 500000 -B 500000'] 
            #        The raspivid command can be tested over the nerwork with : 
            #    (1) raspivid -t 0 -o - -w 1296 -h 972 -fps 12 -pf baseline | netcat -l -p 9999
            #    (2) netcat 192.168.1.12 9999 | vlc --demux h264 -
    
        @gen.coroutine
        def stream_output():
            # https://stackoverflow.com/questions/41431882/live-stream-stdout-and-stdin-with-websocket
            try:
                while True:
                    buffered = yield self.streamproc.stdout.read_bytes(1024*1024*1, partial=True)
                    self.streamsplitter.process(buffered)
            except StreamClosedError as e :
                stamp("stream_output() coroutine closed with error : "+str(e))
                exit()
        
        debug("Opening raspivid process...")
        cmd = ["raspivid", "-t", "0", "-o", "-", "-w", str(self.xres), "-h", str(self.yres), "-fps", str(self.fps), "-pf", "baseline"]
        self.streamproc = Subprocess(cmd, stdout=Subprocess.STREAM)
        IOLoop.current().spawn_callback(stream_output)
        debug("...raspivid process opened")
    











