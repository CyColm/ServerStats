# -*- coding: utf-8 -*-
# coding=<UTF-8>
from telepot.namedtuple import ReplyKeyboardMarkup
from botglobalvars import MyGlobals
import os
import time
import shlex, subprocess
from subprocess import Popen, PIPE, STDOUT
startupScript = '/usr/sbin/serverstatsbot.sh'

myKeyboard = ReplyKeyboardMarkup(keyboard=[
    ['Compile LineageOs'],
    ['Status', 'Restart Bot'],
    ['<- RETOUR']])

def compile(bot, chat_id):
    #compuid = 1003
    buildScript = dict()
    buildScript['path'] = '/home/build/buildScript'
    buildScript['name'] = 'buildscript.sh'
    command_line = str("sudo -i -u build . " + buildScript['path'] + "/" + buildScript['name'] + " > /tmp/lastCompilation.log")
    #args = shlex.split(command_line)
    #comppid = os.fork()
    #if comppid:
    #print ("i am children ! \n PID %d\nrunning compilation before closing ;)" % comppid)
    #os.setgid(1003)
    #os.setuid(1003)
    #print("child my userid :: " + str(os.getuid()))
    p = Popen(command_line, shell=True, stdin=PIPE, stderr=STDOUT, stdout=PIPE, close_fds=True)
    #p.wait()
    #output = str(p.stdout.read())
    #log = open("/tmp/lastCompilation.log", "w")
    #log.write(str(output))
    #log.close()
    #f = open('/tmp/lastCompilation.log', 'rb')
    #bot.sendDocument(chat_id, f)
    #p = Popen("kill " + str(comppid), shell=True, stdin=PIPE, stderr=STDOUT, stdout=PIPE, close_fds=True)

    #else:
        #print("i am fatcher, i ll continue my job !")

#cpu usage alert
def restartBot(bot, chat_id, msg):
    MyGlobals.currentMenu = 'Restarting'
    bot.sendMessage(chat_id, "le bot redemarre", reply_markup=myKeyboard)
    command_line = str(startupScript + " start")
    args = shlex.split(command_line)
    pid = os.fork()
    if pid:
        print ("i am children ! restartin in 2 s")
        subprocess.Popen(args)
        time.sleep(5)
        os._exit(1)
    else:
        print("i am fatcher, retiring..")
        os._exit(0)
    #raise SystemExit

def compilStatus(bot, chat_id):
    command_line = str("tail -n5 /tmp/lastCompilation.log")
    p = Popen(command_line, shell=True, stdin=PIPE, stderr=STDOUT, stdout=PIPE, close_fds=True)
    output = p.stdout.read()
    bot.sendMessage(chat_id, output)

def main(bot, chat_id, msg):
    print(str("je suis dans " + __name__))
    if msg['text']=='Others':
        bot.sendMessage(chat_id, str("fonctionalités diverses "), reply_markup=myKeyboard)
        MyGlobals.currentMenu = 'Others'
    if msg['text']=='Restart Bot' and MyGlobals.currentMenu == 'Others':
        restartBot(bot, chat_id, msg)
    elif msg['text']=='Compile LineageOs' and MyGlobals.currentMenu == 'Others':
        if compile(bot, chat_id):
            bot.sendMessage(chat_id, str("compilation lancée en processus enfant"), reply_markup=myKeyboard)
        else:
            bot.sendMessage(chat_id, str("il y a eu un probleme en lancant la compilation en processus enfant"), reply_markup=myKeyboard)
    elif msg['text']=='Status' and MyGlobals.currentMenu=='Others':
            compilStatus(bot, chat_id)
    elif msg['text']=='<- RETOUR':
        MyGlobals.currentMenu = 'Main'
        bot.sendMessage(chat_id, "retour au menu principal", reply_markup=MyGlobals.mainKeyboard)