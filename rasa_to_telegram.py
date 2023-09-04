# from telegram import *
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler
from telegram.ext import filters
from telegram.ext import Update
from telegram.ext import Updater, MessageHandler, Filters
import speech_recognition as sr
from pydub import AudioSegment
import os
import requests
import ast
import json
from PIL import Image
import requests
from io import BytesIO



URL = 'http://79.143.84.170:7230' + '/webhooks/rest/webhook'

TOKEN = '6160410011:AAHBupnNkair5Cvl_twjw-_qCCA_0pgYyUg'

src = 'voice.mp3' #'voice.ogg'
trg = 'voice.wav'


def sendRequestToRasa(update, update_id):
    global URL

    headers = {'Content-Type': 'application/json; charset=utf-8'}

    ReceivedPacketFromRASA = requests.post(URL, headers=headers, json={'message': update.message.text,'sender':update.effective_user.id})
    ReceivedMessageFromRASA = json.loads(ReceivedPacketFromRASA.text)


    return ReceivedMessageFromRASA



def stt():
  sound = AudioSegment.from_ogg(src)
  Myfile = sound.export(format="wav")
  source = sr.AudioFile(Myfile)

  r = sr.Recognizer()
  with sr.AudioFile(Myfile) as source:
    audio = r.listen(source)

  try:
    message = r.recognize_google(audio,language='fa-IR')
  except sr.UnknownValueError:
    message = False
  except sr.RequestError as e:
    message = False

  return message




def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(text='سلام به زیچر خوش اومدی. من دستیار تو در زیچر هستم تا بتونم تجربه بهتری رو برات فراهم کنم.')
    bot = context.bot
   # bot.send_photo(chat_id=update.message.chat.id, photo=open('/home/shahla/zitureBot/Rasa_v2_server/media/LOGO.jpeg', 'rb'))


def voiceHandler(update: Update, context: CallbackContext) -> None:
    if update.message.voice:
        if os.path.exists(src):
          os.remove(src)
        if os.path.exists(trg):
          os.remove(trg)


        VoiceFile = context.bot.getFile(update.message.voice.file_id)
        VoiceFile.download(src)
        Text = stt()
        if Text:
          update.message.text = Text
          #update.message.reply_text(text="من این پیغام را از سمت شما دریافت کردم : ", quote=True)
          update.message.reply_text(text=update.message.text, quote=True)
        else:
          update.message.reply_text(text='صدای شما واضح نبود! 🤨 لطفا آرامتر و با صدای بلندتر تکرار کنید!😌')


    answer = sendRequestToRasa(update, update.update_id)
    request=update.message.text
    print(request)
    print()
    print(answer)
    #events_file = open("/home/shahla/zitureBot/Rasa_v2_server/conversation.txt", "a")
    #events_file.write('user_message : '+str(request)+'\n')
    #events_file.write('bot_response : '+str(answer)+ '\n')
    #events_file.close()
    #update.message.reply_text(text=str(request), quote=True)
    if not answer and request:
        update.message.reply_text(text='متوجه پیغام شما نشدم لطفا منظور خود را به گونه دیگری بیان کنید.')

    TextToUser = False
    ImageToUser = False
    MediaToUser = False
    customToUser = False
    for i in range(len(answer)):
        if 'text' in answer[i]:
            TextToUser = answer[i]['text']
        elif 'custom' in answer[i]:
            customToUser = answer[i]['custom']
        elif 'image' in answer[i]:
            ImageToUser = answer[i]['image']
            if 'http' in ImageToUser:
                DocImageToUser = ImageToUser
            else:
                DocImageToUser = open(ImageToUser, 'rb')
        elif 'attachment' in answer[i]:
            MediaToUser = answer[i]['attachment']['payload']['src']


    if TextToUser:
        update.message.reply_text(text=TextToUser, quote=True)
    if customToUser:
        # update.message.reply_text(text=customToUser.encode(encoding="UTF-8"), quote=True)
        update.message.reply_text(text=str(answer[0]['custom']), quote=True)
    if ImageToUser:
        context.bot.send_photo(chat_id=update.message.chat.id , photo=DocImageToUser)
    # if MediaToUser:
    #     context.bot.send_audio(chat_id=update.message.chat.id , audio=open(MediaToUser, 'rb'))
    if MediaToUser:
        context.bot.send_document(chat_id=update.message.chat.id , document=open(MediaToUser, 'rb'))
    




def main():
  global TOKEN
  updater = Updater(TOKEN, use_context=True)
  updater.dispatcher.add_handler(CommandHandler('start', start))
  updater.dispatcher.add_handler(MessageHandler(telegram.ext.filters.all & ~telegram.ext.filters.command, voiceHandler, run_async=True))
  updater.start_polling()
  updater.idle()


if __name__=='__main__':
  main()

