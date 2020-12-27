from transitions.extensions import GraphMachine
from utils import *
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageMessage, ImageSendMessage, TemplateSendMessage, ButtonsTemplate, MessageTemplateAction, PostbackTemplateAction, ImageCarouselTemplate, ImageCarouselColumn, PostbackEvent
import random
import string
from image import Transfer
import PIL.Image
# import time

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def on_enter_menu(self, event):
        # time.sleep(60)
        sendMenu(event.reply_token)
        print("menu state")

    def on_enter_management(self, event):
        sendManagement(event.reply_token)
        print("management state")

    def on_enter_transfer_style(self, event):
        sendTransfer(event.reply_token)
        print("transfer_style state")

    def on_enter_uploading(self, event):
        showImgsinfo(event, self.state)
        print("uploading state")

    def on_enter_deleting(self, event):
        deleteImgs(event)
        print("deleting state")

    def on_enter_selectMainImg(self, event):
        showImgsinfo(event, self.state)
        print("selectMainImg state")

    def on_enter_selectStyleImg(self, event):
        showImgsinfo(event, self.state)
        print("selectStyleImg state")



    def menu(self, event):
        if isinstance(event, MessageEvent):
            if event.message.type == "text":
                return event.message.text == "menu"
        return False

    def back(self, event):
        if isinstance(event, MessageEvent):
            if event.message.type == "text":
                return event.message.text == "back"
        return False

    def manage(self, event):
        return event.message.text == "manage"

    def transfer(self, event):
        return event.message.text == "transfer"

    def upload(self, event):
        return event.message.text == "upload"

    # def delete(self, event):
    #     return event.message.text == "delete"

    def selectMain(self, event):
        return event.message.text == "selectMain" or event.message.text == "choose"

    def selectStyle(self, event):
        return event.message.text == "selectStyle" or event.message.text == "choose"

    def delete(self, event):
        # print("delete called")
        if isinstance(event, PostbackEvent):
            # print("test\n\n\n")
            filename = event.postback.data
            if filename in os.listdir(os.path.join("static", event.source.user_id)):
                os.remove(os.path.join("static", event.source.user_id, filename))
                return True
            # else:
            #     send_text_message(event.reply_token, event.postback.data)
            #     return True
        if isinstance(event, MessageEvent):
            return event.message.text == "delete"
        return False

    def uploadImgs(self, event):
        print("uploadImgs called")
        if isinstance(event, MessageEvent):
            if event.message.type == "image":
                print("uploading image!!!")
                path = os.path.join("static", event.source.user_id)
                # if not os.path.exists(path):
                #     os.mkdir(path)
                image_name = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(4))
                image_content = line_bot_api.get_message_content(event.message.id)
                image_name = image_name.upper() +'.jpg'

                path = os.path.join(path, image_name)
                with open(path, 'wb') as fd:
                    for chunk in image_content.iter_content():
                        fd.write(chunk)
                return True
            if event.message.text == "view":
                return True
        return False

    def Start_Transfer(self, event):
        print("Start_Transfer called")
        if isinstance(event, MessageEvent):
            if event.message.text == "Start_Transfer":
                if event.source.user_id in contentImgs.keys() and event.source.user_id in styleImgs.keys() and contentImgs[event.source.user_id] and styleImgs[event.source.user_id]:
                    path = os.path.join("static", event.source.user_id)
                    print("start transfering")
                    for contentImg in contentImgs[event.source.user_id]:
                        for styleImg in styleImgs[event.source.user_id]:
                            img = Transfer(os.path.join(path, contentImg), os.path.join(path, styleImg))
                            img.save(os.path.join("static", event.source.user_id, "sty" + contentImg))
                    contentImgs[event.source.user_id].clear()
                    styleImgs[event.source.user_id].clear()
                    print("finished transfering!!")
                    return True
        return False

    def reset(self, event):
        if isinstance(event, MessageEvent):
            if event.message.text == "reset" and event.source.user_id in contentImgs.keys() and event.source.user_id in styleImgs.keys():
                contentImgs[event.source.user_id].clear()
                styleImgs[event.source.user_id].clear()
                return True
        return False



    # def is_going_to_management(self, event):
    #     text = event["message"]
    #     return text.lower() == "go to management"

    # def is_going_to_upload(self, event):
    #     text = event["message"]
    #     return text.lower() == "go to upload"

    # def on_enter_management(self, event):
    #     print("I'm entering management")

    #     # reply_token = event.reply_token
    #     # send_text_message(reply_token, "Trigger management")
    #     self.go_back(event)

    # def on_exit_management(self, event):
    #     print("Leaving management")

    # def on_enter_upload(self, event):
    #     print("I'm entering upload")

    #     # reply_token = event.reply_token
    #     # send_text_message(reply_token, "Trigger upload")
    #     self.go_back(event)

    # def on_enter_menu(self, event):
    # 	print("enter menu state")

    # def on_exit_menu(self, event):
    # 	print("Leaving menu state")

    # def on_exit_upload(self, event):
    #     print("Leaving upload")







# machine.advance({"message":"go to upload"})
# print(machine.state)
# machine.get_graph().draw("fsm.jpg", prog="dot", format="jpg")