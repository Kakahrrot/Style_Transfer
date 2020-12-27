from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageMessage, ImageSendMessage, TemplateSendMessage, ButtonsTemplate, MessageTemplateAction, PostbackTemplateAction, ImageCarouselTemplate, ImageCarouselColumn, PostbackEvent
import configparser
from linebot import LineBotApi, WebhookHandler
import os

config = configparser.ConfigParser()
config.read('config.ini')
line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))

domain = 'https://381f20a31e66.ngrok.io/static/'
contentImgs = {}
styleImgs = {}

def send_text_message(reply_token, text):
	line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

def send_image_message(reply_token, filename):
	url = domain + filename
	if filename[:4] == "http":
		url = filename
	line_bot_api.reply_message(
        reply_token,
        ImageSendMessage(original_content_url = url, preview_image_url = url)
    )

def sendMenu(reply_token):
	buttons_template = TemplateSendMessage(
        alt_text='Menu',
        template=ButtonsTemplate(
            title='Menu',
            text='Please choose one of the following modes',
            thumbnail_image_url = domain + 'f.jpeg',
            actions=[
                MessageTemplateAction(
                    label='manage',
                    text='manage'
                ),
                MessageTemplateAction(
                    label='transfer',
                    text='transfer'
                )
            ]
        )
    )
	line_bot_api.reply_message(reply_token, buttons_template)

def sendTransfer(reply_token):
	print("sendTransfer called")
	buttons_template = TemplateSendMessage(
        alt_text='Transfer',
        template=ButtonsTemplate(
            title='Transfer',
            text='Choose one of the following modes\ninput "menu" to go back',
            thumbnail_image_url = domain + 'f.jpeg',
            actions=[
                MessageTemplateAction(
                    label='Choose main Images',
                    text='selectMain'
                ),
                MessageTemplateAction(
                    label='Choose your styles',
                    text='selectStyle'
                ),
                MessageTemplateAction(
                    label='Start Transfer!',
                    text='Start_Transfer'
                ),
                MessageTemplateAction(
                    label='reset',
                    text='reset'
                ),
                # MessageTemplateAction(
                #     label='menu',
                #     text='menu'
                # )
            ]
        )
    )
	line_bot_api.reply_message(reply_token, buttons_template)

def sendManagement(reply_token):
	buttons_template = TemplateSendMessage(
        alt_text='Management',
        template=ButtonsTemplate(
            title='Management',
            text='Upload or Delete',
            thumbnail_image_url = domain + 'f.jpeg',
            actions=[
                MessageTemplateAction(
                    label='upload',
                    text='upload'
                ),
                MessageTemplateAction(
                    label='delete',
                    text='delete'
                ),
                MessageTemplateAction(
                    label='back to menu',
                    text='menu'
                )
            ]
        )
    )
	line_bot_api.reply_message(reply_token, buttons_template)

def deleteImgs(event):
	# print("sendImgsInfo called")
	if isinstance(event, PostbackEvent):
		return
	path = domain + event.source.user_id + "/"
	columns = [ImageCarouselColumn(
                image_url=domain + "f.jpeg",
                action=
					PostbackTemplateAction(
						label="back",
						text='back',
						data='back'
					)
			)]
	for filename in os.listdir(os.path.join("static", event.source.user_id)):
		col = ImageCarouselColumn(
                image_url=path + filename,
                action=
					PostbackTemplateAction(
						label="delete",
						text='delete',
						data=filename
					)
			)
		columns.append(col)
	Image_Carousel = TemplateSendMessage(
        alt_text='ImgsInfo',
        template=ImageCarouselTemplate(
        columns=columns
		)
    )
	
	# Image_Carousel = TemplateSendMessage(
 #        alt_text='ImgsInfo',
 #        template=ImageCarouselTemplate(
 #        columns=[
 #            ImageCarouselColumn(
 #                image_url=path + "IFTM.jpg",
 #                action=
	# 				PostbackTemplateAction(
	# 					label="delete",
	# 					text='delete',
	# 					data=os.path.join("static", event.source.user_id, "IFTM.jpg")
	# 				)
	# 		),
	# 		ImageCarouselColumn(
 #                image_url=path + "OJHS.jpg",
 #                action=
 #                	PostbackTemplateAction(
	#                 	label="delete",
	# 					text='delete',
	# 					data=os.path.join("static", event.source.user_id, "OJHS.jpg")
 #                	)
 #            )
 #        ]
	# 	)
 #    )
	line_bot_api.reply_message(event.reply_token,Image_Carousel)

def showImgsinfo(event, state):
	path = domain + event.source.user_id + "/"
	columns = [ImageCarouselColumn(
                image_url=domain + "f.jpeg",
                action=
					PostbackTemplateAction(
						label="back",
						text='back',
						data='back'
					)
			)]
	for filename in os.listdir(os.path.join("static", event.source.user_id)):
		data = filename
		text = 'choose'
		if state == "uploading":
			text = 'view'
			data = path + filename
		col = ImageCarouselColumn(
                image_url=path + filename,
                action=
					PostbackTemplateAction(
						label=filename,
						text=text,
						data=data
					)
			)
		columns.append(col)
	Image_Carousel = TemplateSendMessage(
        alt_text='ImgsInfo',
        template=ImageCarouselTemplate(
        columns=columns
		)
    )
	
	# Image_Carousel = TemplateSendMessage(
 #        alt_text='ImgsInfo',
 #        template=ImageCarouselTemplate(
 #        columns=[
 #            ImageCarouselColumn(
 #                image_url=path + "IFTM.jpg",
 #                action=
	# 				PostbackTemplateAction(
	# 					label="delete",
	# 					text='delete',
	# 					data=os.path.join("static", event.source.user_id, "IFTM.jpg")
	# 				)
	# 		),
	# 		ImageCarouselColumn(
 #                image_url=path + "OJHS.jpg",
 #                action=
 #                	PostbackTemplateAction(
	#                 	label="delete",
	# 					text='delete',
	# 					data=os.path.join("static", event.source.user_id, "OJHS.jpg")
 #                	)
 #            )
 #        ]
	# 	)
 #    )

	line_bot_api.reply_message(event.reply_token,Image_Carousel)




    # print("uploadImgs called")
    # if event.message.type == "image":
    #     print("uploading image!!!")
    #     path = os.path.join("static", event.source.user_id)
    #     # if not os.path.exists(path):
    #     #     os.mkdir(path)
    #     image_name = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(4))
    #     image_content = line_bot_api.get_message_content(event.message.id)
    #     image_name = image_name.upper() +'.jpg'

    #     path = os.path.join(path, image_name)
    #     with open(path, 'wb') as fd:
    #         for chunk in image_content.iter_content():
    #             fd.write(chunk)
    #     return True

    # if event.message.type == "text":
    #     send_text_message(event.reply_token, "Please upload images")
    #     return "OK"
