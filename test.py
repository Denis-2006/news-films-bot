import telebot
import configparser
import requests
import time
import sys
from bs4 import BeautifulSoup as bea

while True:
    try:
        
        config = configparser.ConfigParser()
        config.read("setings.ini")

        bot = telebot.TeleBot(config["Telebot"]["token"])

        main_keyboard = telebot.types.ReplyKeyboardMarkup(row_width = 1, resize_keyboard = True )
        top_fantasy = telebot.types.KeyboardButton( text = "новости фантастики" )
        top_thriller = telebot.types. KeyboardButton( text = "новости боевиков" )
        top_horror = telebot.types. KeyboardButton( text = "новости хоррора" )
        main_keyboard.add(top_fantasy, top_thriller, top_horror)

        empty_keyboard = telebot.types.ReplyKeyboardRemove(selective = False)
        
        print("Bot starting..")
        
        @bot.message_handler(commands = ["start", "news"])
        def commands_message(message):
            if message.text == "/start":
                bot.send_message(message.chat.id, "привеt", reply_markup = main_keyboard)
            elif message.text == "/news":
                bot.send_message(message.chat.id, "ну что, как дела?", reply_markup = empty_keyboard)
                
        @bot.message_handler(content_types=["text"])
        def site_message(message):
                        if message.text.lower() in "новости фантастики":
                                headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"}
                                s = requests.get("https://www.mirf.ru/category/news/", headers = headers)

                                html = bea(s.content, "html.parser")
                                #tmp = html.find("a", attrs={"class" : "attachment-home_article_big size-home_article_big wp-post-image"})
                                #bot.send_message(message.chat.id, f"https://www.kinopoisk.ru/{tmp['href']}")

                                news = html.find_all("div", attrs={"class" : "home_article_item_image"})
                                for i in range(5):
                                    #print(i)
                                    #print(news[i])
                                    temp = news[i].find("a")
                                    #print(temp)
                                    #print(temp["href"])
                                    bot.send_message(message.chat.id, temp["href"])
                                    #print()
                        
        @bot.message_handler(content_types = ["sticker"])
        def sticker_id(message):
            bot.send_message(message.chat.id, message.sticker.file_id)
            #bot.send_photo(message.chat.id,photo=open( 'out.png' , 'rb' ))
            #bot.send_photo(message.chat.id, photo = open ( 'out.png' , 'rb' ), reply_markup = keyboard )



        bot.polling(none_stop = True, interval = 0)
    except Exception as e:
        print(f"Error: {e}")
    #else:
    #    print("бот молодец")  
    finally:
        time.sleep(60)
        print("Restarting...")
