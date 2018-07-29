# -*- coding: utf-8 -*-
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
from botglobalvars import MyGlobals
import botConfig as config
import os
import time
import shlex
import subprocess
from subprocess import Popen, PIPE, STDOUT
startupScript = '/usr/sbin/serverstatsbot.sh'

    #myKeyboard = ReplyKeyboardMarkup(keyboard=[
        #['Compile LineageOs'],
        #['Status', 'Restart Bot'],
        #['Restart Emby'],
        #['<- Back']])

def createKb():
    print("create kb")
    keyboard=[['Compile LineageOs'],
            ['Status', 'Restart Bot']]
    keyboardrow = []
    if config.getConfig('settings.ini', 'Bot', 'isEmbyPresent', 'bool'):
        print("emby present")
        keyboardrow.append('Restart Emby')
    keyboardrow.append('<- Back')
    keyboard.append(keyboardrow)
    myKeyboard = ReplyKeyboardMarkup(keyboard=keyboard)
    return myKeyboard


 #Done : auto set send alert Off when starting the build
def compile(bot, chat_id):
    config.setConfig('settings.ini', 'Alerts', 'sendAlerts', 1)
    MyGlobals.sendAlerts = config.getConfig('settings.ini',
                                'Alerts', 'sendAlerts', 'bool')
    buildScript = dict()
    buildScript['path'] = '/home/build/buildScript'
    buildScript['name'] = 'buildscript.sh'
    command_line = str("sudo -i -u build . "
                   + buildScript['path'] + "/"
                   + buildScript['name'] + " > /tmp/lastCompilation.log")
    p = Popen(command_line, shell=True, stdin=PIPE, stderr=STDOUT, stdout=PIPE, close_fds=True)


def restartBot(bot, chat_id, msg):
    MyGlobals.currentMenu = 'Restarting'
    bot.sendMessage(chat_id, "le bot redemarre", reply_markup=myKeyboard)
    command_line = str(startupScript + " start")
    args = shlex.split(command_line)
    pid = os.fork()
    if pid:
        #print ("i am children ! restartin in 2 s")
        subprocess.Popen(args)
        time.sleep(5)
        os._exit(1)
    else:
        #print("i am fatcher, retiring..")
        os._exit(0)


def compilStatus(bot, chat_id):
    command_line = str("tail -n5 /tmp/lastCompilation.log")
    p = Popen(command_line, shell=True, stdin=PIPE,
              stderr=STDOUT, stdout=PIPE, close_fds=True)
    output = p.stdout.read()
    bot.sendMessage(chat_id, output)


def main(bot, chat_id, msg):
    print((str("je suis dans " + __name__)))
    if msg['text'] == 'Others':
        bot.sendMessage(chat_id, str("fonctionalités diverses "),
                        reply_markup=createKb())
        MyGlobals.currentMenu = 'Others'
    if (msg['text'] == 'Restart Bot'
        and MyGlobals.currentMenu == 'Others'):
        restartBot(bot, chat_id, msg)
    elif (msg['text'] == 'Compile LineageOs'
          and MyGlobals.currentMenu == 'Others'):
        if MyGlobals.isCompillinlling is False:
            if compile(bot, chat_id):
                bot.sendMessage(chat_id,
                                str("compilation lancée en processus enfant"),
                                reply_markup=myKeyboard)
            else:
                bot.sendMessage(chat_id,
                                str("il y a eu un probleme en lancant la"
                                + " compilation en processus enfant"),
                                reply_markup=myKeyboard)
        else:
            bot.sendndMessage(chat_id, "Une compillation est deja en cours !")
    elif (msg['text'] == 'Status'
          and MyGlobals.currentMenu == 'Others'):
            compilStatus(bot, chat_id)
    elif (msg['text'] == 'Restart Emby'
          and MyGlobals.currentMenu == 'Others'):
            command_line = str("systemctl restart emby-server")
            p = Popen(command_line, shell=True, stdin=PIPE,
                stderr=STDOUT, stdout=PIPE, close_fds=True)
            output = p.stdout.read()
            bot.sendMessage(chat_id, output)
    elif msg['text'] == '<- Back':
        MyGlobals.currentMenu = 'Main'
        bot.sendMessage(chat_id,
                        "retour au menu principal",
                        reply_markup=MyGlobals.mainKeyboard)
