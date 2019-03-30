#! /usr/bin/python3


    # telegram bot
import telegram
from telegram.ext import Updater
import logging
from telegram.ext import CommandHandler
    # cowsays for telegram bot
import subprocess
    # reboot
import os

    # Homemade bits
from config import * 
import config as cfg
from utils import *


"""
    Telegram bot documentation : 
        https://github.com/python-telegram-bot/python-telegram-bot/wiki/Extensions-–-Your-first-Bot
        https://github.com/python-telegram-bot/python-telegram-bot/wiki/Code-snippets#post-an-image-file-from-disk
        https://python-telegram-bot.readthedocs.io/en/stable/
        
	Author : Quentin Bouvet
"""


class NotifyBot : 
    
    def __init__(self, cameraWrapper) :         
        
            # create new user/object
        def __userobj(update) : 
            convid = update.message.chat_id
            userid = update.message.from_user.id
            username = update.message.from_user.username
            newr = {"conv" : convid, "user" : userid, "name" : username}
            debug("Telegram bot initialized new user object : \n\t"+str(newr))
            return newr
        
        def start(bot, update) : 
            stamp("/start detected")
                # register
            newr = __userobj(update)
            if not newr in self.registered : 
                self.registered.append(newr)
                response = "You've been registered for updates. Currently registered are : \n " + self.registered_str()
            else : 
                response = "It seems you're already registered for updates : \n" +self.registered_str()
                # respond
            bot.send_message(chat_id=update.message.chat_id, text=response)
            return 
        
        def stop(bot, update) : 
            stamp("/stop detected")
                # process request
            newr = __userobj(update)
            if newr in self.registered : 
                self.registered.remove(newr)
                response = "You've been unregistered for notifications. Currently registered are : \n " + str(self.registered_str())
            else : 
                response = "It seems you're not currently registered Currently registered are : \n "+self.registered_str() 
            bot.send_message(chat_id=update.message.chat_id, text=response)
            return
        
        def reboot(bot, update) : 
            stamp("/reboot received")
                # process request
            user = __userobj(update)
            response = "@"+user["name"]+" initiatied reboot\n downtime will be ~90s\n\n Please /start again"
            for r in self.registered : 
                self.bot.send_message(chat_id=r["conv"], text=response)
            os.system("sudo systemctl reboot")
        
        def ping(bot, update) :
            #wisdom = subprocess.check_output(["cowsay $(fortune)"])
            ip = str(get_pub_ip())
            response = "Hello frend. You can stream at : http://watchbot.ddns.net\n[WAN] http://"+str(get_pub_ip())+"\n[LAN] 192.168.1.47:8384"
            bot.send_message(chat_id=update.message.chat_id, text=response)
            self.sendPhoto(chat_id=update.message.chat_id)
            return 
        
            # Camera wrapper
        self.cameraWrapper = cameraWrapper
        
            # Conversation IDs to send notifications to
        self.bot = telegram.Bot(token=TGTOKEN)
        self.registered = []
        for userobj in TG_DEFAULT_USERS : 
            self.registered.append(userobj)
            
            # updater polls telegram services and passes updates to dispatcher
        self.updater = Updater(token=TGTOKEN)
        self.dispatcher = self.updater.dispatcher
        
            # logging is probably optional for production
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
        
            # register handlers
        start_handler = CommandHandler('start', start)
        self.dispatcher.add_handler(start_handler)
        stop_handler = CommandHandler('stop', stop)
        self.dispatcher.add_handler(stop_handler)
        ping_handler = CommandHandler('ping', ping)
        self.dispatcher.add_handler(ping_handler)
        reboot_handler = CommandHandler('reboot', reboot)
        self.dispatcher.add_handler(reboot_handler)
        
            # Start 
        self.updater.start_polling()
        
            # Notify default users
        self.notifyStart()
    
    def registered_str(self) : 
        res = ""
        for r in self.registered : 
            res = res + str(r) + "\n"
        return res;
    
    def notifyStart(self) : 
        notification = "Watchbot has started. Congratulations, you're a default user ! \n\nYou'll be notified if activity is detected. Send '/stop' to stop notifications. \n\nStreaming is available at :\nhttp://watchbot.ddns.net\n[WAN] http://"+str(get_pub_ip())+"\n[LAN] 192.168.1.51:8384"
        cmdsstr = "Valid commands are :\n/start : to register for updates\n/stop : to stop receiving updates\n/ping : to ask for a picture\n/reboot : to restart the bot (you need to do it after streaming video)\n"
        for r in self.registered : 
            self.bot.send_message(chat_id=r["conv"], text=notification)
        for r in self.registered : 
            self.bot.send_message(chat_id=r["conv"], text=cmdsstr)
    
    def notify(self) : 
        notification = "Activity has been detected. Check : http://watchbot.ddns.net\n[WAN] http://"+str(get_pub_ip())+"\n[LAN] "+str(get_lan_ip())+":"+str(cfg.PORT)
        for r in self.registered : 
            self.bot.send_message(chat_id=r["conv"], text=notification)
    
    def sendPhoto(self, chat_id=None) : 
        fileObject = self.cameraWrapper.photo()
        stamp("sending photo", name="TelegramBot")
        if chat_id is None : 
            for r in self.registered : 
                # send times V quality = 15->default, 40->17s, 50->20s, 75->30s, 100->30s
                stamp("    | to "+str(r), name="TelegramBot")
                self.bot.send_photo(chat_id=r["conv"], photo=fileObject, timeout=PHOTO_SEND_TIMEOUT)
        else : 
            self.bot.send_photo(chat_id=chat_id, photo=fileObject, timeout=PHOTO_SEND_TIMEOUT)
        stamp("sending photo  ...  Done", name="TelegramBot")

