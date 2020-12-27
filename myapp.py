from __future__ import unicode_literals
import os
import string
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageMessage, ImageSendMessage, TemplateSendMessage, ButtonsTemplate, MessageTemplateAction, PostbackTemplateAction, PostbackEvent
import configparser

import random

import matplotlib.pyplot as plt

from fsm import TocMachine
from utils import *
import functools
print = functools.partial(print, flush=True)

machines = {}

def createMachine(id):
    machines[id] = TocMachine(
            states = ["menu", "management", "uploading", "deleting", "transfer_style", "selectMainImg", "selectStyleImg"],
            transitions = [
                {
                    "trigger": "advance",
                    "conditions": "menu",
                    "source": "*",
                    "dest": "menu",
                },
                {
                    "trigger": "advance",
                    "conditions": "manage",
                    "source": "menu",
                    "dest": "management",
                },
                {
                    "trigger": "advance",
                    "conditions": "upload",
                    "source": "management",
                    "dest": "uploading",
                },
                {
                    "trigger": "advance",
                    "conditions": "delete",
                    "source": "management",
                    "dest": "deleting",
                },
                {
                    "trigger": "advance",
                    "conditions": "transfer",
                    "source": "menu",
                    "dest": "transfer_style"
                },
                {
                    "trigger": "advance",
                    "conditions": "selectMain",
                    "source": "transfer_style",
                    "dest": "selectMainImg"
                },
                {
                    "trigger": "advance",
                    "conditions": "selectStyle",
                    "source": "transfer_style",
                    "dest": "selectStyleImg"
                },
                {
                    "trigger": "advance",
                    "conditions": "delete",
                    "source": "deleting",
                    "dest": "deleting"
                },
                {
                    "trigger": "advance",
                    "conditions": "uploadImgs",
                    "source": "uploading",
                    "dest": "uploading"
                },
                
                {
                    "trigger": "advance",
                    "conditions": "selectMain",
                    "source": "selectMainImg",
                    "dest": "selectMainImg"
                },
                {
                    "trigger": "advance",
                    "conditions": "selectStyle",
                    "source": "selectStyleImg",
                    "dest": "selectStyleImg"
                },
                {
                    "trigger": "advance",
                    "conditions": "back",
                    "source": ["uploading", "deleting"],
                    "dest": "management"
                },
                {
                    "trigger": "advance",
                    "conditions": "back",
                    "source": ["selectMainImg", "selectStyleImg"],
                    "dest": "transfer_style"
                },
                {
                    "trigger": "advance",
                    "conditions": "reset",
                    "source": "transfer_style",
                    "dest": "transfer_style"
                },
                {
                    "trigger": "advance",
                    "conditions": "Start_Transfer",
                    "source": "transfer_style",
                    "dest": "transfer_style"
                }
            ],
            initial = "menu",
            auto_transitions = False,
            show_conditions = True,
        )

app = Flask(__name__, static_url_path = '/static')

# config = configparser.ConfigParser()
# config.read('config.ini')
# line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
# handler = WebhookHandler(config.get('line-bot', 'channel_secret'))

@app.route("/callback", methods=['GET', 'POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    
    try:
        print(body, signature)
        handler.handle(body, signature)
        
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent)#, message = TextMessage)
def echo(event):
    print(type(event), "\n\n")
    if event.message.type == "text" and event.message.text == "fsm":
        machines[event.source.user_id].get_graph().draw(os.path.join("static", "fsm.jpg"), prog = "dot", format = "jpg")
        send_image_message(event.reply_token, "fsm.jpg")
        return "OK"
    if event.source.user_id not in machines.keys():
        print("createMachine")
        path = os.path.join("static", event.source.user_id)
        if not os.path.exists(path):
            os.mkdir(path)
        createMachine(event.source.user_id)
        sendMenu(event.reply_token)
        return "OK"
    if not machines[event.source.user_id].advance(event):
        send_text_message(event.reply_token, "Invalid command, try again")
    print(machines[event.source.user_id].state)
    return "OK"


@handler.add(PostbackEvent)
def echo(event):
    print(type(event), "\n\n")

    if event.source.user_id not in machines.keys():
        print("createMachine")
        createMachine(event.source.user_id)
        sendMenu(event.reply_token)
        return "OK"
    # machines[event.source.user_id].get_graph().draw("fsm.jpg", prog = "dot", format = "jpg")
    if event.postback.data[:4] == "http":
        send_image_message(event.reply_token, event.postback.data)
        return "OK"

    if event.postback.data in os.listdir(os.path.join("static", event.source.user_id)):
        if machines[event.source.user_id].state == "selectMainImg":
            if event.source.user_id not in contentImgs.keys():
                contentImgs[event.source.user_id] = []
            s = ""
            if event.postback.data in contentImgs[event.source.user_id]:
                s += "請不要玩我啦QQ\n人家debug很辛苦誒><\n還故意選重複的圖片...\n你以為我那麼笨嗎XDDD\n\n"
            else:
                contentImgs[event.source.user_id].append(event.postback.data)
            s += "Main Images:\n" + contentImgs[event.source.user_id][0]
            for img in contentImgs[event.source.user_id][1:]:
                s += "\n" + img
            send_text_message(event.reply_token, s)
            return "OK"
        elif machines[event.source.user_id].state == "selectStyleImg":
            if event.source.user_id not in styleImgs.keys():
                styleImgs[event.source.user_id] = []
            s = ""
            if event.postback.data in styleImgs[event.source.user_id]:
                s += "請不要玩我啦QQ\n人家debug很辛苦誒><\n還故意選重複的圖片...\n你以為我那麼笨嗎XDDD\n\n"
            else:
                styleImgs[event.source.user_id].append(event.postback.data)
            s += "Style Images:\n" + styleImgs[event.source.user_id][0]
            for img in styleImgs[event.source.user_id][1:]:
                s += "\n" + img
            send_text_message(event.reply_token, s)
            return "OK"

    if event.postback.data[:4] == "menu" or event.postback.data[:4] == "back":
        return "OK"
    if not machines[event.source.user_id].advance(event):
        send_text_message(event.reply_token, "Invalid command, try again")
    print(machines[event.source.user_id].state)
    return "OK"

# @handler.add(ImageMessage)
# def echo(event):
#     print(type(event), "\n\n")

#     if event.source.user_id not in machines.keys():
#         print("createMachine")
#         createMachine(event.source.user_id)
#         sendMenu(event.reply_token)
#         return "OK"
#     # machines[event.source.user_id].get_graph().draw("fsm.jpg", prog = "dot", format = "jpg")
#     if not machines[event.source.user_id].uploadImgs(event):
#         send_text_message(event.reply_token, "Invalid command, try again")
#     print(machines[event.source.user_id].state)
#     return "OK"
    
    

    # if event.message.type == "text":
    #     line_bot_api.reply_message(
    #         event.reply_token,
    #         TextSendMessage(text = event.message.text)
    #     )
    # elif event.message.type == "image":
    #     path = os.path.join("static", event.source.user_id)

    #     if not os.path.exists(path):
    #         os.mkdir(path)

    #     image_name = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(4))
    #     image_content = line_bot_api.get_message_content(event.message.id)
    #     image_name = image_name.upper() +'.jpg'

    #     path = os.path.join(path, image_name)
    #     with open(path, 'wb') as fd:
    #         for chunk in image_content.iter_content():
    #             fd.write(chunk)

    #     path = "https://381f20a31e66.ngrok.io/" + path
    #     # print("\n\n", path)

    #     # for windows
    #     path = "https://381f20a31e66.ngrok.io/static/" + event.source.user_id + "/" + image_name;

    #     line_bot_api.reply_message(
    #             event.reply_token,
    #             ImageSendMessage(original_content_url = path, preview_image_url = path)
    #         )

if __name__ == "__main__":
    app.debug = True
    # machine.get_graph().draw("fsm.jpg", prog = "dot", format = "jpg")
    app.run()