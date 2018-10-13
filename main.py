#! /usr/bin/python3

    # Homemade bits
from utils import *
from telegrambot import NotifyBot
from pirmanager import PIRManager
from camerawrapper import CameraWrapper
from webserver import WebServerApp


"""
    Main class of the picamera project

    Author : Quentin Bouvet
"""


stamp("Initializing ...")

cam = CameraWrapper()
stamp("(2/4) Camera wrapper initialized")

bot = NotifyBot(cam)
stamp("(1/4) Telegram bot ready")

pir = PIRManager()
pir.add_callback(lambda pinNumber : stamp("PIR sensor : activity detected"))
pir.add_callback(lambda pinNumber : bot.notify())
pir.add_callback(lambda pinNumber : bot.sendPhoto())
stamp("(3/4) PIR sensor ready")

httpserver = WebServerApp(cam)
httpserver.start()
stamp("(4/4) Webserver ready")



try:
    stamp("Application is running")
    while True :
        time.sleep(3600)
except KeyboardInterrupt:
    stamp("Cleaning up the GPIO")
    pir.cleanup()
    stamp("Exiting")
    exit()


stamp("Exiting")
exit()























########################################################################
#                           OLD CODE                                   #
########################################################################

print("You've reached deprecated code")
exit()



'''
    #
    #   Dummy websocket subclass made for testing
    #
class EchoWebSocket(WebSocketHandler):
    
    def initialize(self, hello="yo", **kwargs):
        self.hello = hello
        super().initialize(**kwargs)
    
    def open(self):
        print("WebSocket opened")

    def on_message(self, message):
        self.write_message(u"You said: " + message)

    def on_close(self):
        print("WebSocket closed")
'''
