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
from utils import *


"""
    Telegram bot documentation : 
        https://github.com/python-telegram-bot/python-telegram-bot/wiki/Extensions-–-Your-first-Bot
        
	Author : Quentin Bouvet
"""


class NotifyBot : 
    
    def __init__(self) :         
        
            # create new user/object
        def __userobj(update) : 
            convid = update.message.chat_id
            userid = update.message.from_user.id
            username = update.message.from_user.username
            newr = {"conv" : convid, "user" : userid, "name" : username}
            #newr = {"conv" : convid, "user" : userid}
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
                response = "You've been unregistered for notifications. Currently registered are : \n " + str(self.convs)
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
            response = "Public ip : "+ip+"\nYou can stream at http://"+str(get_pub_ip())+":"+str(PORT)
            bot.send_message(chat_id=update.message.chat_id, text=response)
            return 
        
            # Conversation IDs to send notifications to
        self.bot = telegram.Bot(token=TGTOKEN)
        self.registered = []
            
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
    
    def registered_str(self) : 
        res = ""
        for r in self.registered : 
            res = res + str(r) + "\n"
        return res;
    
    def notify(self) : 
        notification = "Activity has been detected. Your can stream at : http://"+str(get_pub_ip())+":"+str(PORT)
        for r in self.registered : 
            self.bot.send_message(chat_id=r["conv"], text="@"+str(r["name"])+"\n"+notification)

