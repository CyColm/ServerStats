# coding=<UTF-8>
from telepot.namedtuple import ReplyKeyboardMarkup
from botglobalvars import MyGlobals

submenus = ['settinghoursth', 'setmem', 'settingmemth', 'setcpu', 'settingcputh', 'setpoll', 'settingpollth']

myKeyboard = ReplyKeyboardMarkup(keyboard=[
    ['setmem','setcpu'],
    ['setpoll', 'Surveille'],
    ['nb d heures graphique'],
    ['<- RETOUR']])

setKeyboard = ReplyKeyboardMarkup(keyboard=[
    ['70', '80'],
    ['Cancel']])

setPollKeyboard = ReplyKeyboardMarkup(keyboard=[
    ['10', '30'],
    ['60', '300'],
    ['Cancel']])

sethoursKeyboard = ReplyKeyboardMarkup(keyboard=[
    ['1', '2'],
    ['3', '6'],
    ['12', '24'],
    ['Cancel']])

def setgraphichours(bot, chat_id, msg):
    bot.sendChatAction(chat_id, 'typing')
    MyGlobals.currentMenu = 'settinghoursth'
    bot.sendMessage(chat_id, "combien d'heures a afficher dans le graphique ?", reply_markup=sethoursKeyboard)

def settinggraphichours(bot, chat_id, msg):
    bot.sendChatAction(chat_id, 'typing')
    if msg['text'] == 'Cancel':
        MyGlobals.currentMenu = 'Settings'
        bot.sendMessage(chat_id, "All set!", reply_markup=myKeyboard)
    else:
        try:
            MyGlobals.GraphicHours = float(msg['text'])
            if MyGlobals.GraphicHours < 49:
                bot.sendMessage(chat_id, "All set!", reply_markup=myKeyboard)
                MyGlobals.currentMenu = 'Settings'
            else:
                1/0
        except:
            bot.sendMessage(chat_id, "Please send a proper numeric value below 49 hours")



def setmem(bot, chat_id, msg):
    bot.sendChatAction(chat_id, 'typing')
    MyGlobals.settingmemth.append(chat_id)
    bot.sendMessage(chat_id, "Send me a new memory threshold to monitor?", reply_markup=setKeyboard)
    MyGlobals.currentMenu = 'settingmemth'

def settingmemth(bot, chat_id, msg):
    bot.sendChatAction(chat_id, 'typing')
    if msg['text'] == 'Cancel':
        MyGlobals.currentMenu = 'Settings'
        bot.sendMessage(chat_id, "All set!", reply_markup=myKeyboard)
    else:
        try:
            MyGlobals.memorythreshold = int(msg['text'])
            if MyGlobals.memorythreshold < 100:
                bot.sendMessage(chat_id, "All set!", reply_markup=myKeyboard)
                MyGlobals.currentMenu = 'Settings'
            else:
                1/0
        except:
            bot.sendMessage(chat_id, "Please send a proper numeric value below 100.")


#cpu usage alert
def setcpu(bot, chat_id, msg):
    bot.sendChatAction(chat_id, 'typing')
    MyGlobals.currentMenu = 'settingcputh'
    bot.sendMessage(chat_id, "Send me a new cpu usage threshold to monitor?", reply_markup=setKeyboard)

def settingcputh(bot, chat_id, msg):
    bot.sendChatAction(chat_id, 'typing')
    if msg['text'] == 'Cancel':
        MyGlobals.currentMenu = 'Settings'
        bot.sendMessage(chat_id, "All set!", reply_markup=myKeyboard)
    else:
        try:
            MyGlobals.usagethreshold = int(msg['text'])
            if MyGlobals.usagethreshold < 100:
                bot.sendMessage(chat_id, "All set!", reply_markup=myKeyboard)
                MyGlobals.currentMenu = 'Settings'
            else:
                1/0
        except:
            bot.sendMessage(chat_id, "Please send a proper numeric value below 100.")

def setpoll(bot, chat_id, msg):
    bot.sendChatAction(chat_id, 'typing')
    MyGlobals.currentMenu = 'settingpollth'
    bot.sendMessage(chat_id, "Send me a new polling interval in seconds? (higher than 10)", reply_markup=setPollKeyboard)

def settingpollth(bot, chat_id, msg):
    bot.sendChatAction(chat_id, 'typing')
    if msg['text'] == 'Cancel':
        MyGlobals.currentMenu = 'Settings'
        bot.sendMessage(chat_id, "All set!", reply_markup=myKeyboard)
    else:
        try:
            MyGlobals.poll = int(msg['text'])
            if MyGlobals.poll > 9:
                bot.sendMessage(chat_id, "All set!", reply_markup=myKeyboard)
                MyGlobals.currentMenu = 'Settings'
            else:
                1/0
        except:
            bot.sendMessage(chat_id, "Please send a proper numeric value higher than 10.")


def activeSurv(bot, chat_id):
    bot.sendChatAction(chat_id, 'typing')
    MyGlobals.surveillanceActive = not MyGlobals.surveillanceActive
    if MyGlobals.surveillanceActive:
        bot.sendMessage(chat_id, "Je vais t'envoyer des rapports toutes les " + str(MyGlobals.poll) + " secondes", disable_web_page_preview=True)
    else:
        bot.sendMessage(chat_id, "Surveillance active desactivee", disable_web_page_preview=True)




def main(bot, TOKEN, chat_id, msg):
    print(str ("je suis dans " + __name__))
    if msg['text']=='Settings':
        bot.sendMessage(chat_id, str("Bienvenue dans les parametres du bot"), reply_markup=myKeyboard)
        MyGlobals.currentMenu = 'Settings'
    elif msg['text'] == 'setmem':
        setmem(bot, chat_id, msg)
    elif MyGlobals.currentMenu == 'settingmemth':
        settingmemth(bot, chat_id, msg)
    elif msg['text'] == "setcpu" and MyGlobals.currentMenu == 'Settings':
        setcpu(bot, chat_id, msg)
    elif MyGlobals.currentMenu=='settingcputh':
        settingcputh(bot, chat_id, msg)
    #set graph interval
    elif msg['text'] == 'setpoll' and MyGlobals.currentMenu == 'Settings':
        setpoll(bot, chat_id, msg)
    elif MyGlobals.currentMenu =='settingpollth':
        settingpollth(bot, chat_id, msg)
    elif msg['text'] == 'nb d heures graphique'and MyGlobals.currentMenu == 'Settings':
        setgraphichours(bot, chat_id, msg)
    elif MyGlobals.currentMenu =='settinghoursth':
        settinggraphichours(bot, chat_id, msg)
    elif msg['text'] == 'Surveille':
        activeSurv(bot, chat_id)
    elif msg['text']=='<- RETOUR':
        MyGlobals.currentMenu = 'Main'
        bot.sendMessage(chat_id, "retour au menu principal", reply_markup=MyGlobals.mainKeyboard)