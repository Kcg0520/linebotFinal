from flask import Flask, request, abort
from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
    TemplateMessage,
    ConfirmTemplate,
    ButtonsTemplate,
    CarouselTemplate,
    CarouselColumn,
    ImageCarouselTemplate,
    ImageCarouselColumn,
    MessageAction,
    URIAction,
    PostbackAction,
    DatetimePickerAction,
    CameraAction,
    CameraRollAction,
    LocationAction
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,PostbackEvent,
    FollowEvent,PostbackContent
)
import myfitnesspal
import matplotlib.pyplot as plt
app = Flask(__name__)
caltotal=[]
proteintoal=[]
fattotal=[]
carbstotal=[]
sodiumtotal=[]
sugartotal=[]
basicinfo=[]
configuration = Configuration(access_token='LVxXjG26WuhUSgarsuaJBzFw0TJoTJGxtM6IIL8YRC2DlYaz1Cb0QXGtBKfVKdkzyUx86bYPlM4pkYrz5vRpVrYHLD77e5et0kQ7xszaptKHWykCOWEHZdUu9XWnOlc4BwEQI94egYUXEm9T9/HQYAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('886804d12908edd8cff134dc251d1b88')
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'
#初次使用者
@handler.add(FollowEvent)
def handle_follow(event):
    print('這裡是營養小幫手!第一次使用者請先輸入您的身高、體重、年齡及性別，以便我們提供您更適合的飲食建議。') 
@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        text=event.message.text
        if event.message.text == '性別':
            buttons_template = ButtonsTemplate(
                title='請選擇您的生理性別',
                text='性別選擇',
                actions=[
                    PostbackAction(label='男', data='gender=male'),
                    PostbackAction(label='女', data='gender=female')
                ])
            template_message = TemplateMessage(
                alt_text='Postback Sample',
                template=buttons_template
            )
            # 回覆訊息
            text_message=TextMessage(text='請接續輸入您的身高(需函我的身高此關鍵字)')
            messages_all=[template_message,text_message]
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=messages_all
                )
            )
            
        elif '身高' in event.message.text:
            height=''.join(i for i in event.message.text if i.isdigit())
            text_message=TextMessage(text='請接續輸入您的體重(需函我的體重此關鍵字)')
            height_message=TextMessage(text='您的身高為'+height+'cm')
            messages_all=[height_message,text_message]
            basicinfo.append(height)
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=messages_all
                )
            )
            
        elif '體重' in event.message.text:
            weight=''.join(i for i in event.message.text if i.isdigit())
            text_message=TextMessage(text='請接續輸入您的年紀(需函我的年紀此關鍵字)')
            weight_message=TextMessage(text='您的體重為'+weight+'kg')
            messages_all=[weight_message,text_message]
            basicinfo.append(weight)
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=messages_all
                )
            )
            
        elif '年紀' in event.message.text or '年齡' in event.message.text or '歲' in event.message.text:
            age=''.join(i for i in event.message.text if i.isdigit())
            age_message=TextMessage(text='您的年齡為'+age+'歲')
            text_message=TextMessage(text='輸入成功!如需查詢飲食建議請輸入"餐點登錄"')
            messages_all=[age_message,text_message]
            basicinfo.append(age)
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=messages_all
            
                )
            )
        #加入預先的設定標準
        # Buttons Template
        elif '餐點登錄' in text:
            url = request.url_root + 'static/Logo.jpg'
            url = url.replace("http", "https")
            app.logger.info("url=" + url)
            buttons_template = ButtonsTemplate(
                thumbnail_image_url=url,
                title='餐點登錄',
                text='詳細說明',
                actions=[
                    # URIAction(label='連結', uri='https://www.facebook.com/NTUEBIGDATAEDU'),
                    # PostbackAction(label='回傳值', data='ping', displayText='傳了'),
                    # MessageAction(label='傳"哈囉"', text='哈囉'),
                    # DatetimePickerAction(label="選擇時間", data="時間", mode="datetime"),
                    PostbackAction(label='早餐',data='breakfast',),
                    PostbackAction(label='午餐',data='lunch',text='請輸入午餐品項，請開頭輸入我的午餐:作為提示語，午餐可依序描述名稱、品牌'),
                    PostbackAction(label='晚餐',data='dinner',text='請輸入晚餐品項，請開頭輸入我的晚餐:作為提示語，晚餐可依序描述名稱、品牌'),
                    PostbackAction(label='點心',data='snack',text='請輸入點心品項，請開頭輸入我的點心:作為提示語，點心可依序描述名稱、品牌')
                ]
            )
            template_message = TemplateMessage(
                alt_text="This is a buttons template",
                template=buttons_template
            )
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[template_message]
                )
            )

            
       
        elif '早餐' in event.message.text:
            breakfast = text.replace('早餐', '').strip()
            client = myfitnesspal.Client()
            food_items = client.get_food_search_results(breakfast)
            try:
                cals=str(food_items[0].calories)
            except KeyError:
                cals='NA'
            try:    
                protein=str(food_items[0].protein)
            except KeyError:
                protein='NA'
            try:
                fat=str(food_items[0].fat)
            except KeyError:
                fat='NA'
            try:
                carbs=str(food_items[0].carbohydrates)
            except KeyError:
                carbs='NA'
            try:
                sodium=str(food_items[0].sodium)
            except KeyError:
                sodium='NA'
            try:
                sugar=str(food_items[0].sugar)
            except KeyError:
                sugar='NA'
            caltotal.append(cals)
            proteintoal.append(protein)
            fattotal.append(fat)
            carbstotal.append(carbs)
            sodiumtotal.append(sodium)
            sugartotal.append(sugar)
            
            text_message=TextMessage(text='您的早餐為'+breakfast+'\n，營養成分如下:\n熱量:'+cals+'大卡\n蛋白質:'+protein+'g\n脂肪:'+fat+'g\n碳水化合物:'+carbs+'g\n鈉:'+sodium+'mg\n糖:'+sugar+'g')
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[text_message]
                    ))
        elif '午餐' in event.message.text:
            breakfast = text.replace('午餐', '').strip()
            client = myfitnesspal.Client()
            food_items = client.get_food_search_results(breakfast)
            try:
                cals=str(food_items[0].calories)
            except KeyError:
                cals='NA'
            try:    
                protein=str(food_items[0].protein)
            except KeyError:
                protein='NA'
            try:
                fat=str(food_items[0].fat)
            except KeyError:
                fat='NA'
            try:
                carbs=str(food_items[0].carbohydrates)
            except KeyError:
                carbs='NA'
            try:
                sodium=str(food_items[0].sodium)
            except KeyError:
                sodium='NA'
            try:
                sugar=str(food_items[0].sugar)
            except KeyError:
                sugar='NA'
            caltotal.append(cals)
            proteintoal.append(protein)
            fattotal.append(fat)
            carbstotal.append(carbs)
            sodiumtotal.append(sodium)
            sugartotal.append(sugar)
            text_message=TextMessage(text='您的午餐為'+breakfast+'\n，營養成分如下:\n熱量:'+cals+'大卡\n蛋白質:'+protein+'g\n脂肪:'+fat+'g\n碳水化合物:'+carbs+'g\n鈉:'+sodium+'mg\n糖:'+sugar+'g')
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[text_message]
                    ))
        elif '晚餐' in event.message.text:
            breakfast = text.replace('早餐', '').strip()
            client = myfitnesspal.Client()
            food_items = client.get_food_search_results(breakfast)
            try:
                cals=str(food_items[0].calories)
            except KeyError:
                cals='NA'
            try:    
                protein=str(food_items[0].protein)
            except KeyError:
                protein='NA'
            try:
                fat=str(food_items[0].fat)
            except KeyError:
                fat='NA'
            try:
                carbs=str(food_items[0].carbohydrates)
            except KeyError:
                carbs='NA'
            try:
                sodium=str(food_items[0].sodium)
            except KeyError:
                sodium='NA'
            try:
                sugar=str(food_items[0].sugar)
            except KeyError:
                sugar='NA'
            caltotal.append(cals)
            proteintoal.append(protein)
            fattotal.append(fat)
            carbstotal.append(carbs)
            sodiumtotal.append(sodium)
            sugartotal.append(sugar)
            text_message=TextMessage(text='您的晚餐為'+breakfast+'\n，營養成分如下:\n熱量:'+cals+'大卡\n蛋白質:'+protein+'g\n脂肪:'+fat+'g\n碳水化合物:'+carbs+'g\n鈉:'+sodium+'mg\n糖:'+sugar+'g')
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[text_message]
                    ))
        elif '點心' in event.message.text:
            breakfast = text.replace('點心', '').strip()
            client = myfitnesspal.Client()
            food_items = client.get_food_search_results(breakfast)
            try:
                cals=str(food_items[0].calories)
            except KeyError:
                cals='NA'
            try:    
                protein=str(food_items[0].protein)
            except KeyError:
                protein='NA'
            try:
                fat=str(food_items[0].fat)
            except KeyError:
                fat='NA'
            try:
                carbs=str(food_items[0].carbohydrates)
            except KeyError:
                carbs='NA'
            try:
                sodium=str(food_items[0].sodium)
            except KeyError:
                sodium='NA'
            try:
                sugar=str(food_items[0].sugar)
            except KeyError:
                sugar='NA'
            caltotal.append(cals)
            proteintoal.append(protein)
            fattotal.append(fat)
            carbstotal.append(carbs)
            sodiumtotal.append(sodium)
            sugartotal.append(sugar)
            text_message=TextMessage(text='點心'+breakfast+'\n，營養成分如下:\n熱量:'+cals+'大卡\n蛋白質:'+protein+'g\n脂肪:'+fat+'g\n碳水化合物:'+carbs+'g\n鈉:'+sodium+'mg\n糖:'+sugar+'g')
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[text_message]
                    ))
        elif '今日總量' in event.message.text:
            totalcal=[]
            for i in caltotal:
                if i=='NA':
                    caltotal.remove(i)
                else:
                    i=float(i)
                    totalcal.append(i)
            for i in proteintoal:
                if i=='NA':
                    proteintoal.remove(i)
                else:
                    i=float(i)
                    proteintoal.append(i)
            for i in fattotal:
                if i=='NA':
                    fattotal.remove(i)
                else:
                    i=float(i)
                    fattotal.append(i)
            for i in carbstotal:
                if i=='NA':
                    carbstotal.remove(i)
                else:
                    i=float(i)
                    carbstotal.append(i)
            for i in sodiumtotal:
                if i=='NA':
                    sodiumtotal.remove(i)
                else:
                    i=float(i)
                    sodiumtotal.append(i)
            for i in sugartotal:
                if i=='NA':
                    sugartotal.remove(i)
                else:
                    i=float(i)
                    sugartotal.append(i)
            totalcal=str(sum(totalcal))
            totalprotein=str(sum(proteintoal))
            totalfat=str(sum(fattotal))
            totalcarbs=str(sum(carbstotal))
            totalsodium=str(sum(sodiumtotal))
            totalsugar=str(sum(sugartotal))
            text_message=TextMessage(text='您今日的總熱量為'+totalcal+'大卡\n總蛋白質為'+totalprotein+'g\n總脂肪為'+totalfat+'g\n總碳水化合物為'+totalcarbs+'g\n總鈉為'+totalsodium+'mg\n總糖分為'+totalsugar+'g')
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[text_message]
                    )) 
      
    
                    
@handler.add(PostbackEvent)
def handle_postback(event):
    with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
        
            if event.postback.data == 'breakfast':
                text_message=TextMessage(text='請輸入早餐品項，請開頭輸入我的早餐:作為提示語，早餐可依序描述名稱、品牌')
                line_bot_api.reply_message(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[text_message]
                    )
                )
            if event.postback.data == 'lunch':
                text_message=TextMessage(text='請輸入午餐品項，請開頭輸入我的午餐:作為提示語，午餐可依序描述名稱、品牌')
                line_bot_api.reply_message(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[text_message]
                    )
                )
            if event.postback.data == 'dinner':
                text_message=TextMessage(text='請輸入晚餐品項，請開頭輸入我的晚餐:作為提示語，晚餐可依序描述名稱、品牌')
                line_bot_api.reply_message(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[text_message]
                    )
                )
            if event.postback.data == 'snack':
                text_message=TextMessage(text='請輸入點心品項，請開頭輸入我的點心:作為提示語，點心可依序描述名稱、品牌')
                line_bot_api.reply_message(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[text_message]
                    )
                )
            if event.postback.data == 'gender=male':
                standardcal=10*float(basicinfo[0])+6.25*float(basicinfo[1])-5*(basicinfo[2])+5  
            if event.postback.data == 'gender=female':
                standardcal=10*float(basicinfo[0])+6.25*float(basicinfo[1])-5*(basicinfo[2])-161
            standardprotein=0.8*float(basicinfo[1])
            standardfat=0.3*standardcal/9
            standardcarbs=(standardcal-standardprotein*4-standardfat*9)/4
            
                
        
# 用於存儲用戶資料的全域字典







        

       
if __name__ == "__main__":
    app.run()