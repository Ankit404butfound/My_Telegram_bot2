import logging
from telegram.ext import Updater, CommandHandler, MessageHandler,InlineQueryHandler, Filters,CallbackContext
from telegram import Update, Bot
from telegram.utils.helpers import mention_markdown
import telegram
import os
import re
import randfacts
from bs4 import BeautifulSoup as bs4
from urllib.request import urlopen
import urllib.request
import random
import json
import time
import requests
import pytz
import datetime
import threading
import numpy as np
from PIL import Image
import cv2
import string
#import enchant

arr = string.ascii_letters
arr = arr + string.digits + "+,.-? "
PORT = int(os.environ.get('PORT', 5000))
count = 0
odusername = os.environ.get("USER")

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
TOKEN = os.environ.get("TOKEN")
chatid = 0
# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def joke(bot,update):
    req = requests.get("https://official-joke-api.appspot.com/random_joke").json()
        
    update.message.reply_text("Q. "+req["setup"]+"\n"+"-> "+req["punchline"])


##def keepalive():
##    robot = telegram.Bot(TOKEN)
##    while True:
##        robot.sendMessage(-403832831,"Hi")
##        time.sleep(5)

mybot = Bot(TOKEN)

###########################################################################################################################################################################
def getimg(case,col):
    global width,height,back
    img = cv2.imread(r"ChrImages\%s.png"%case)
    img = np.array(img)
    img[np.where((img!=[255,255,255]).all(axis=-1))] = col
    cv2.imwrite(r"ChrImages\chr.png",img)
    cases = Image.open(r"ChrImages\chr.png")
    back.paste(cases,(width,height))
    newwidth = cases.width
    width = width + newwidth

def download():
    """Downloads all images of handwritten characters,\nthey are written by the author of this library"""
    def down(char):
        url = "https://raw.githubusercontent.com/Ankit404butfound/HomeworkMachine/master/Image/%s"%char
        imglink=urllib.request.urlopen(url)
        imgNp=np.array(bytearray(imglink.read()))
        img = cv2.imdecode(imgNp,-1)
        cv2.imwrite(r"ChrImages\%s"%char.lower(),img)
        print(".",end="")
    try:
        getimg("zback")
    except:
        print("Installing some additional dependencies...",end="")
        if not os.path.exists("ChrImages"):
            os.makedirs("ChrImages")
        for letter in arr:
            if letter == " ":
                letter = "zspace"
            if letter.isupper():
                letter = "c"+letter.lower()
            if letter == ",":
                letter = "coma"
            if letter == ".":
                letter = "fs"
            if letter == "?":
                letter = "que"
            try:
                down(letter+".png")
            except:
                down(letter+".PNG")
        down("zback.png")
        print("\nDownload Complete!")

def mytexttohand(bot,update):
    #bot.send_photo(chat_id = update.message.chat.id, photo=open(r'C:\Users\pc\Desktop\Python Test codes\me.png', 'rb'),reply_to_message_id=update.message.message_id)

  #print(update.effective.file_id)
  #bot.sendAnimation(update.message.chat.id,random.choice(ani_id),reply_to_message_id=update.message.message_id)
    global width,height,back
    width = 50
    height = 0
    newwidth = 0
    received_msg = update.message.text
    received_msg = received_msg.replace("/tth ","")
    print(received_msg)
    datalst = received_msg.split("rgb>>")
    text_to_cnvt = datalst[0].strip()
    try:
        comb = datalst[1].split(",")
        rgb_comb = [int(comb[0]),int(comb[1]),int(comb[2])]
        print(rgb_comb)
        for color in rgb_comb:
            if color > 255:
                update.message.reply_text("Error : Value cannot be greater than 255")
                return
    except Exception as e:
        rgb_comb = [0,0,138]
        print(e)


    def getimg(case,col):
        global width,height,back
        img = cv2.imread(r"ChrImages\%s.png"%case)
        img = np.array(img)
        img[np.where((img!=[255,255,255]).all(axis=-1))] = col
        cv2.imwrite(r"ChrImages\chr.png",img)
        cases = Image.open(r"ChrImages\chr.png")
        back.paste(cases,(width,height))
        newwidth = cases.width
        width = width + newwidth

    

    def text_to_handwriting(string,rgb=[0,0,138]):
        """Convert the texts passed into handwritten characters"""
        #update.message.reply_text("Conversion started...")
        try:
            global arr, width, height, back
            #rgb.reverse() not working, IDK why.
            back = Image.open(r"ChrImages\zback.png")
            rgb = [rgb[2],rgb[1],rgb[0]]
            count = -1
            lst = string.split()
            for letter in string:
                if width + 150 >= back.width or ord(letter) == 10:
                    height = height + 227
                    width = 50
                if letter in arr:
                    if letter == " ":
                        count += 1
                        letter = "zspace"
                        wrdlen = len(lst[count+1])
                        if wrdlen*110 >= back.width-width:
                            width = 50
                            height = height+227
                        
                    elif letter.isupper():
                        letter = "c"+letter.lower()
                    elif letter == ",":
                        letter = "coma"
                    elif letter == ".":
                        letter = "fs"
                    elif letter == "?":
                        letter = "que"
                        
                    getimg(letter,rgb)
                    
            #back.show()
            #update.message.reply_text("Sending...")
            back.save("img.png")
            bot.send_photo(chat_id = update.message.chat.id, photo = open('img.png', 'rb'),reply_to_message_id=update.message.message_id)
            back.close()
            back = Image.open(r"ChrImages\zback.png")
            #rgb = [0,0,138]
            width = 50
            height = 0
            newwidth = 0
        except Exception as e:
            try:
                # import cv2
                # global cv2
                # download()
                print(e)
            except:
                print("You must install opencv-python library to use this function...")
    if update.message.text == "/tth":
        update.message.reply_text("ERROR\nError Message : Hatttttt.....-_-")

    else:
        update.message.reply_text("Please wait, processing your request, this will take few moments...")
        if not os.path.exists(r"ChrImages\zback.png"):
            time.sleep(2)
            update.message.reply_text("Just a bit more...")
            download()
            update.message.reply_text("Please be patient...")
        #download()
        threading.Thread(target=lambda : text_to_handwriting(text_to_cnvt,rgb_comb)).start()
        
################################################################################################################################################################################

def Todays_history(bot=None,update=None):
    
    dateinfo = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
    date = str(dateinfo.date())
    DD,MM = int(date.split("-")[2]),int(date.split("-")[1])
    str_date = f"{MM}/{DD}"
    
    data = requests.get("https://history.muffinlabs.com/date/%s"%str_date)
    data = data.json()
    content = data["data"]["Events"]
    lenth = len(content)

    particular_year = content[random.randint(0,lenth)]
    year_num = particular_year["year"]

    try:
        update.message.reply_text(f"""Significance of todays' date\nOn {data["date"]} {year_num} {particular_year["text"]}""")

    except:
        mybot.sendMessage(-402125669,f"""Significance of todays' date\nOn {data["date"]} {year_num} {particular_year["text"]}""")
    


def add_bday(bot,update):
      #print(firstname)
    try:
        
        file_data = requests.get("http://rajma.pythonanywhere.com/retreve?uname=date&method=r").text
        uname = str(update.message.from_user.username)
        msg = update.message.text
        msg = msg.replace("/AddBday ","")
        month = int(msg.split("/")[1])
        date = int(msg.split("/")[0])
        datetime.datetime(year=2001,month=month,day=date)
        print(uname,date,month,msg)
        if f"@{uname}" in file_data:
            update.message.reply_text("You have already registered your birthday.")

        else:
            update.message.reply_text("Your Birthday (%s) has been added."%msg)
            requests.get("http://rajma.pythonanywhere.com/retreve?uname=date&method=a&data=@%s : %s/%s\n"%(uname,date,month))

    except Exception as e:
        update.message.reply_text("@Tag_Kiya_kya see, your friend is not providing correct date format.\n(Error message : %s)"%str(e))


def check_bday():
    while True:
        file = requests.get("http://rajma.pythonanywhere.com/retreve?uname=date&method=r").text
        last_checked_date = file.split("\n")[0].replace("Today : ","")
        dateinfo = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
        date = str(dateinfo.date())
        DD,MM = int(date.split("-")[2]),int(date.split("-")[1])
        print(DD,MM)
        str_date = f"{DD}/{MM}"
        if last_checked_date == str_date:
            pass

        else:
            print(str_date)
            
            for details in file.split("\n"):
                if details != "" and "Today" not in details:
                    bday_info = details.split(" : ")[1]
                    birthdate = int(bday_info.split("/")[0])
                    birthmonth = int(bday_info.split("/")[1])
                    birthday = f"{birthdate}/{birthmonth}"
                    print(birthday)
                    if birthday == str_date:
                        mybot.sendMessage(-402125669,(f'Happy Birthday {details.split(" : ")[0]}, have a great centuary ahead.'))
        
            updated_data = file.replace(f"Today : {last_checked_date}",f"Today : {str_date}")
            requests.get("http://rajma.pythonanywhere.com/retreve?uname=date&method=w&data="+updated_data)
            Todays_history()
        time.sleep(300)
                                                      
def answer_question(bot,update):
    lst = ["CAACAgUAAxkBAAMSX2RmdEE9Z5hmeie8mb_nuliOeT0AAroAA_yrpx8-9s0_BpsZHBsE","CAACAgIAAxkBAAMWX2RnFvG4ksouaxn8_1mMnJzqINUAArIBAAJfaRgAAZbYero0RoCrGwQ","CAACAgIAAxkBAAMXX2RnUeDXsKr0_8UW0gXl9RKxQKsAAiQAA8GcYAxIJFq6JQ0ojhsE","CAACAgIAAxkBAAMYX2RnpSapRQmMqJrFQNh1AAFlpoc5AAKTAAP3AsgPJeWS_-k7iFUbBA","CAACAgEAAxkBAAMZX2Rn2HBekewcJ2n-xo1-d8MtAhcAAmEAA-QPqR_isdjgjI8yFxsE"]
                                                      
    cond = True
    count = 0
    msg = update.message.text
    query = msg.replace("/temme","")
    query = query.strip()
                                                      
                                                      
    if query == "":
        file_id = random.choice(lst)
        bot.sendSticker(update.message.chat.id,file_id,reply_to_message_id=update.message.message_id)
        return
                                                                                                                                                          
    data = requests.get("https://api.duckduckgo.com/?q=%s&format=json&pretty=1"%query).json()
    datalst = data["RelatedTopics"]
    lent = len(datalst)

    output = data["AbstractText"]

    if output:
        update.message.reply_text(output)

    elif lent > 0:

        while cond:
            count += 1
            if count > 21:
                update.message.reply_text("I failed to find any result.")
                cond = False
            index = random.randint(0,lent-1)
            try:
                update.message.reply_text(datalst[index]["Text"])
                cond = False
            except Exception as e:
                pass

    else:
        update.message.reply_text("Please specify, what did you mean by %s?"%query)


def start(bot,update):#(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi from Bot2!')

def help(bot,update):#(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')
                                                      

def what_do_you_think(bot,update):
    contents = requests.get('https://yesno.wtf/api').json()
    url = contents["image"]
    print(url)
    chat_id = update.message.chat_id
    bot.send_animation(chat_id=chat_id, animation=url)

def data(bot, update):
    chat_id = update.message.chat.id
    print(chat_id)
    bot.send_document(chat_id=chat_id, document=open("database.txt","rb"))

def facts(bot,update):
    #fact = randfacts.getFact()
    #update.message.reply_text(fact)
    try:
      data = requests.get("https://www.generatormix.com/random-facts-generator").content
      soup = bs4(data)
      fact = soup.find("blockquote",attrs = {'class':"text-left"})
     # print((fact.text))
      update.message.reply_text(fact.text)
    except Exception as e:
      update.message.reply_text(str(e))

def echo(bot,update):#, context):
    """Echo the user message."""
    global count
    chatid = update.message.chat.id
    msg = update.message.text
    print(chatid)
    cond = "@tag_ji_ka_bot"
    if chatid > 0:
        cond = ""
                                                      
#     if update.message.from_user.username == odusername: ##################################################################################
#         ani_id = ["CgACAgQAAxkBAAEBekNfbWpy4pPPL6yBDCQzUAdi2aDSnwACUwIAAhtbhFKp4qp1w0VEtBsE","CgACAgQAAxkBAAEBekJfbWpyKbbMW5Z_kD1rKDb3i9o5jwACaAIAAhxGjFJ8iIwM98N8IBsE","CgACAgQAAxkBAAEBekFfbWpyzJjteChz_vtYJMfakEnRxgACdQIAAr_FnVK3Wb_dpDaDyBsE","CgACAgQAAxkBAAEBekBfbWpy8smpb8BsBjVuk5Mu0H7x1gACKAIAAj15jVIj43jz2xuOSxsE","CgACAgQAAxkBAAEBej5fbWpyzNjFdAsMFfIFl3tNoTx9jAACGQIAAmrhjFNV-NEpN8wTGBsE","CgACAgQAAxkBAAEBej9fbWpyWiBK-EpfCk0aObYfQ7rMfgACgwIAAnmolVJRfU8DEEirHRsE"]                                              
#         bot.sendAnimation(update.message.chat.id,random.choice(ani_id),reply_to_message_id=update.message.message_id)
                                                      
    if cond in msg:
        msg = msg.replace(cond,"")
        if "/train" in msg:
            if " : " in msg:
                msg = msg.replace("/train ","")
                file = open(r"database.txt","a")
                file.write(msg+"\n")
                file.close()
                update.message.reply_text("Trained")
            else:
                update.message.reply_text("Invalid command")
          
                                                      

        elif "/clear" in msg:
            msg = msg.replace("/clear ","")
            file =  open("database.txt")
            data = file.read()
            newcont = data.replace(msg+"\n","")
            file.close()
            with open("database.txt","w") as file:
                file.write(newcont)
                file.close()
            update.message.reply_text("Command deleted")

##        elif "/facts" in msg:
##            fact = randfacts.getFact()
##            update.message.reply_text(fact)

        elif "/news" in msg:
            news_url = "https://news.google.com/topstories?"
            Client = urlopen(news_url)
            xml_page = Client.read()
            Client.close()
            soup_page = BeautifulSoup(xml_page, "html.parser")
            news_list = soup_page.findAll("item")
            #print("Here are top 3 news")
            news = news_list[random.randint(0,len(news_list)-1)]
            news = news.title.text
            update.message.reply_text(news)

        
            
                
        else:
            with open("database.txt") as file:
                for line in file:
                    que = line.split(" :")[0]
                    msg = msg.lower()
                    msg = msg.strip()
                    if (msg in que) or (que in msg):
                        reply = re.search(': (.+)',line).group(1)
                        update.message.reply_text(reply)
                        if count > 0:
                            count = 1
                        break
                else:
                    if count < 1:
                        update.message.reply_text("I don't understand, help me reply better.")
                        update.message.reply_text("Type '/train message : reply' to train me")
                        update.message.reply_text("Here 'message' is what user will message and 'reply' is what I am supposed to reply.")
                        update.message.reply_text("Make sure there is proper spacing before and after ':'")
                        
                    if count == 1:
                        update.message.reply_text("Consider training me")

                    if count == 2:
                        update.message.reply_text("You are not intrested in training me, right?")

                    if count == 3:
                        update.message.reply_text("-_-")
                    if count >= 4:
                        st = "-"*(count-2)+"_"*(count-2)+"-"*(count-2)
                        
                        update.message.reply_text(st)
                    count += 1

##def error(bot,update):#(update, context):
##    """Log Errors caused by Updates."""
##    pass
    #logger.warning('Update "%s" caused error "%s"', update, context.error)
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
group_lst = []
#word = enchant.Dict("en_US")
class WordGame:
    def __init__(self,GROUP):
        self.GROUP = GROUP
        self.username_lst = []
        self.chatid_lst = []
        self.name_lst = []
        self.whose_chance = 0
        self.used_word_lst = []
        self.user_num = 0
        self.round = 1
        self.user_lst = []
        self.game_started = False
        self.start_time = 0
        self.end_time = 0
        self.user_point_dic = {}

    def end(self,bot,update):
        final_score = ""
        bot.sendMessage(self.GROUP,"Game ENDED!!!")
        for i in range(len(self.chatid_lst)):
            user = self.name_lst[i]
            score = self.user_point_dic[self.chatid_lst[i]]
            final_score = f"{final_score}\n{mention_markdown(self.chatid_lst[i],user)} : {score}"
        bot.sendMessage(self.GROUP,final_score,parse_mode="Markdown")
        self.GROUP = GROUP
        self.username_lst = []
        self.chatid_lst = []
        self.name_lst = []
        self.whose_chance = 0
        self.used_word_lst = []
        self.user_num = 0
        self.round = 1
        self.user_lst = []
        self.game_started = False
        self.start_time = 0
        self.end_time = 0
        self.user_point_dic = {}
        

    def join(self,bot,update):
        username = update.message.from_user.username
        name = update.message.from_user.first_name
        chat_id = update.message.from_user.id
        if chat_id not in self.chatid_lst:
            self.user_lst.append(f"{name}:{username}:{chat_id}")
            self.username_lst.append(username)
            self.chatid_lst.append(chat_id)
            self.name_lst.append(name)
            self.user_point_dic[chat_id] = 0
            bot.sendMessage(self.GROUP,text=f"{mention_markdown(chat_id,name)} joined the game, there are currently {len(self.user_lst)} players.",parse_mode="Markdown")

        else:
            update.message.reply_text("You have already joined the game")
       

    def start_game(self,bot,update):
        total_players = len(self.user_lst)

        if not self.game_started:
        
            if total_players > 1:
                bot.sendMessage(self.GROUP,f"Starting a game with {total_players} players")
                self.game_started = True
                self.incriment(bot=bot,update=update)

            else:
                 update.message.reply_text("Game must have atleast 2 players.")

        else:
            update.message.reply_text("Game has already started")

    def word(self,bot,update):
        chat_id = update.message.from_user.id
        name = update.message.from_user.first_name
        if self.whose_chance == chat_id:
            self.end_time = time.time()
            total_time = self.end_time - self.start_time
            message = update.message.text
            message = message.replace("/w ","")
            message = message.lower()
            total_time = round(total_time)
            points = 20 - total_time
            print(points)
            if message == "_pass":
                bot.sendMessage(self.GROUP,text=f"{mention_markdown(chat_id,name)} loses 5 points.",parse_mode="Markdown")
                score = self.user_point_dic[chat_id]
                self.user_point_dic[chat_id] = score - 5
                self.end_time = 0
                self.start_time = 0

            elif points < 0:
                bot.sendMessage(self.GROUP,text=f"{mention_markdown(chat_id,name)} loses 5 points as 20 seconds have passed.",parse_mode="Markdown")
                score = self.user_point_dic[chat_id]
                self.user_point_dic[chat_id] = score - 5
                self.end_time = 0
                self.start_time = 0
                
            else:
                total_words = len(self.used_word_lst)
                prev_word = self.used_word_lst[total_words-1]
                prev_let = prev_word[len(prev_word)-1]
                print(message[0])
                word_check = requests.get("http://rajma.pythonanywhere.com/check?word="+message)
                
                if word.check == "True" and message[0] == prev_let and message.lower() not in self.used_word_lst:
                    bot.sendMessage(self.GROUP,text=f"{mention_markdown(chat_id,name)} chose '{message.upper()}' which is a valid English word\nThey earned {points} points.",parse_mode="Markdown")
                    score = self.user_point_dic[chat_id]
                    self.user_point_dic[chat_id] = points + score
                    print(self.user_point_dic)
                    self.end_time = 0
                    self.start_time = 0
                    self.used_word_lst.append(message.lower())

                elif message.lower() in self.used_word_lst:
                    bot.sendMessage(self.GROUP,text=f"{mention_markdown(chat_id,name)} chose '{message.upper()}' which has been used before\nThey loses 5 points.",parse_mode="Markdown")
                    score = self.user_point_dic[chat_id]
                    self.user_point_dic[chat_id] = score - 5
                    self.end_time = 0
                    self.start_time = 0

                elif message[len(message)-1] != prev_let :
                    bot.sendMessage(self.GROUP,text=f"{mention_markdown(chat_id,name)} chose '{message.upper()}' which does *not* start with '{prev_let.upper()}'\nThey loses {points} points.",parse_mode="Markdown")
                    score = self.user_point_dic[chat_id]
                    self.user_point_dic[chat_id] = score - points
                    self.end_time = 0
                    self.start_time = 0

                else:
                    bot.sendMessage(self.GROUP,text=f"{mention_markdown(chat_id,name)} chose '{message.upper()}' which is *not* a valid English word\nThey loses {points} points.",parse_mode="Markdown")
                    score = self.user_point_dic[chat_id]
                    self.user_point_dic[chat_id] = score - points
                    self.end_time = 0
                    self.start_time = 0

            self.whose_chance = 0
            final_score = ""
            for i in range(len(self.chatid_lst)):
                user = self.name_lst[i]
                score = self.user_point_dic[self.chatid_lst[i]]
                final_score = f"{final_score}\n{mention_markdown(self.chatid_lst[i],user)} : {score}"
            bot.sendMessage(self.GROUP,final_score,parse_mode="Markdown")
            self.incriment(bot,update)
            
                


    def incriment(self,bot,update):
        name = self.name_lst[self.user_num]
        chat_id = self.chatid_lst[self.user_num]
        #bot.sendMessage(self.GROUP,f"""*Round {self.round}*\n{mention_markdown(chat_id,name+"'s")} chance.""",parse_mode="Markdown")
        total_words = len(self.used_word_lst)
        self.whose_chance = chat_id
        if total_words < 1:
            bot.sendMessage(self.GROUP,f"""*Round {self.round}*\n{mention_markdown(chat_id,name+"'s")} chance.

Starting word is 'PYTHON', {mention_markdown(chat_id,name)} you have to say a word starting with 'N'

*Message like this* - /w THE WORD HERE.

You will have 20 seconds to reply, the points you earn will be determined by how fast you replied.

If you replied within first 'n' seconds you earn 20 - n points, *if you fail to reply, type '/w pass', you will lose 5 points*.""",parse_mode="Markdown")
            self.used_word_lst.append("python")

        else:
            prev_word = self.used_word_lst[total_words-1]
            time.sleep(3)
            bot.sendMessage(self.GROUP,f"""*Round {self.round}*\n{mention_markdown(chat_id,name+"'s")} chance.\nPrevious word was *'{prev_word.upper()}'*
You have to say a word starting with {(prev_word[len(prev_word)-1]).upper()}
*Message like this* - /w THE WORD HERE.""",parse_mode="Markdown")

        self.start_time = time.time()
        self.user_num = self.user_num+1
        self.round = self.round+1
        if len(self.chatid_lst)-1 < self.user_num:
            self.user_num = 0

             

#@run_async
def new_word_game(bot,update):
    group_id = update.message.chat_id
    if group_id not in group_lst:
        new_game = WordGame(group_id)
        group_lst.append(group_id)
        dp.add_handler(CommandHandler("join_word_game",new_game.join))
        dp.add_handler(CommandHandler("start_word_game",new_game.start_game))
        dp.add_handler(CommandHandler("w",new_game.word))
        dp.add_handler(CommandHandler("end_game",new_game.end))
        update.message.reply_text("Starting new game\nType /join_word_game to join.")
    else:
        update.message.reply_text("A game is already running")
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
dp = ""
def main():
    """Start the bot."""
    global dp
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN)#, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("data", data))
    dp.add_handler(CommandHandler("facts", facts))
    dp.add_handler(CommandHandler("what_do_you_think", what_do_you_think))
    dp.add_handler(CommandHandler("joke", joke))
    dp.add_handler(CommandHandler("AddBday", add_bday))
    dp.add_handler(CommandHandler("todays_significance", Todays_history))
    dp.add_handler(CommandHandler("temme", answer_question))
    dp.add_handler(CommandHandler("tth", mytexttohand))
    dp.add_handler(CommandHandler('new_word_game', new_word_game))
                                                      

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))
                                                      

    # log all errors
    #dp.add_error_handler(error)
##    updater.start_polling()
    # Start the Bot
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook('https://rajmatelebot.herokuapp.com/' + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    threading.Thread(target=check_bday).start()                                                   
    #keepalive()
    try:                                             
        open("database.txt")
                                                      

    except:
        file = open("database.txt","w")
        file.write("""hi : Hello there
how are you : I am fine Thank you
how do you do : I am fine Thank you
awesome : Glad you liked it
thank you : You're welcome
your name : My name is AnkitBot
wow : Thank you :-)
your creator : My creator is Ankit Raj Mahapatra
hello : Hi there.
birthday : I don't know, maybe 31st June.
favourite season : Winter
favourite person : You :-)
your phone number : 101100100001101011000011010110001100100101011011001000011011010101010010101010101
wonderful : Glag you liked it.
do you like me : Why wouldn't I?
/start : Hello there!
""")
        file.close()
    main()
