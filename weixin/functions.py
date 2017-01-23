# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt


from wechat_sdk import WechatBasic,WechatConf
from wechat_sdk.exceptions import ParseError
from wechat_sdk.messages import TextMessage, VoiceMessage, ImageMessage, VideoMessage, LinkMessage, LocationMessage,EventMessage,ShortVideoMessage
from untitled.settings import WECHAT_TOKEN, WEIXIN_APPID, WEIXIN_APPSECRET
from weixin.models import test_data
import random

import sys, json
import urllib
from urllib.request import urlopen
import datetime
import matplotlib.pyplot as plt
import os

from . import info



conf=WechatConf(
token=WECHAT_TOKEN,
appid=WEIXIN_APPID,
appsecret=WEIXIN_APPSECRET,
encrypt_mode='normal',
encoding_ase_key='1pParL1h55XglOTuNjo2PQtFIRDdjHJMoP8wzTMet9S'
)
#
wechat_instance = WechatBasic(conf=conf)



def create_menu(menu):
    wechat_instance.create_menu(menu)

# create_menu(info.menu)

def weather_api():
    url = "http://api.openweathermap.org/data/2.5/weather?q=Hongkong&appid=4c2058c8e5c4e94fffc5871bc18098c6"
    # req = urllib.Request(url)
    # req.add_header("apikey", "您自己的apikey")
    resp = urlopen(url).read()
    # content =resp.read()
    # content=str(content)
    content=json.loads(resp.decode('utf-8'))
    # content["weather"]
    message="最低气温:%s,平均气温:%s，最高气温:%s，湿度:%s"%(content['main']['temp_min']-273.15,int(content['main']['temp']-273.15),content['main']['temp_max']-273.15,content['main']['humidity'])
    return str(message)

def save_test_data(message):
    tem=random.randint(0,20)
    hum=random.randint(0,20)
    test_data.objects.create(user=str(message.source),temperature=tem,humidity=hum)
    print(test_data.objects.all())


def textswitch(message):
    if message.content == '1':
        reply_text = info.message_reply_1_test
    elif message.content == '2':
        reply_text = "待开发"
    elif message.content=='3':
        save_test_data(message)
        reply_text= "save ok"
    elif message.content=='4':
         text=test_data.objects.filter(user=message.source,data__lt=datetime.datetime.now()).order_by('-data').values()[0]
         print(text)
         reply_text="尊敬的用户您好,当前时间%s,气温为%s,湿度为%s,"%(text['data'].strftime("%B %d,%Y"),text['temperature'],text['humidity'])
         # test_data.objects.filter(data__lt=datetime.datetime.now()).values()[0]['data'].strftime("%B %d,%Y")
    else:
        reply_text = info.message_subscribe

    return  reply_text

def draw_plot(keys,wechat):
    if keys=='V1001_TODAY_PLOT':
        info=test_data.objects.filter(data__lt=datetime.datetime.now(),data__gt=datetime.datetime.combine(datetime.date.today(),datetime.time(0,0,0,0)))
        y=[int(num['temperature']) for num in info.values()]
        x=[(time['data'].time().hour+time['data'].time().minute/60) for time in info.values()]
        print(y)
        print(x)
        # x=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
        plt.subplot(211)
        plt.title("Today's Temperature ")
        plt.xlabel('time/hr')
        plt.ylabel('temperature/degree')
        plt.xlim([0,24])
        plt.ylim([-10,40])
        plt.grid(True)
        plt.plot(x,y,'-')

        y = [int(num['humidity']) for num in info.values()]
        x = [(time['data'].time().hour + time['data'].time().minute / 60) for time in info.values()]
        plt.subplot(212)
        plt.title("Today's humidity ")
        plt.xlabel('time/hr')
        plt.ylabel('humidity/%')
        plt.xlim([0,24])
        plt.ylim([-10,40])
        plt.grid(True)
        plt.plot(x,y,'-')

        plt.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95, hspace=1.0,
                            wspace=0.35)
        plt.savefig('./weixin/plot/test.jpg')
        plt.clf()
        with open('./weixin/plot/test.jpg','rb') as f:
            media_id=wechat_instance.upload_media('image',f,extension='jpg')
            print(media_id)
        os.remove('./weixin/plot/test.jpg')
        return wechat.response_image(media_id=media_id['media_id'])

    elif keys=='V1001_WEEK_PLOT':
        info=test_data.objects.filter(data__lt=datetime.datetime.now(),data__gt=datetime.datetime(datetime.date.today().year,datetime.date.today().month,datetime.date.today().day-7,0,0,0,0))
        y=[int(num['temperature']) for num in info.values()]
        x=[(time['data'].date().day+time['data'].time().hour/24) for time in info.values()]
        x=[value-min(x) for value in x]
        # print(y)
        # print(x)
        # x=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
        plt.subplot(211)
        plt.title("Week's Temperature ")
        plt.xlabel('time/day')
        plt.ylabel('temperature/degree')
        plt.xlim([0,7])
        plt.ylim([-10,40])
        plt.grid(True)
        plt.plot(x,y,'-')

        y = [int(num['humidity']) for num in info.values()]
        x = [(time['data'].date().day + time['data'].time().hour / 24) for time in info.values()]
        x = [value - min(x) for value in x]
        plt.subplot(212)
        plt.title("Week's humidity ")
        plt.xlabel('time/day')
        plt.ylabel('humidity/%')
        plt.xlim([0, 7])
        plt.ylim([-10, 40])
        plt.grid(True)
        plt.plot(x, y, '-')

        plt.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95, hspace=1.0,
                            wspace=0.35)

        plt.savefig('./weixin/plot/test.jpg')
        plt.clf()
        with open('./weixin/plot/test.jpg','rb') as f:
            media_id=wechat_instance.upload_media('image',f,extension='jpg')
            print(media_id)
        os.remove('./weixin/plot/test.jpg')
        return wechat.response_image(media_id=media_id['media_id'])

    elif keys=='V1001_MONTH_PLOT':
        info=test_data.objects.filter(data__lt=datetime.datetime.now(),data__gt=datetime.datetime(datetime.date.today().year,datetime.date.today().month,1,0,0,0,0))
        y=[int(num['temperature']) for num in info.values()]
        x=[(time['data'].date().day+time['data'].time().hour/24) for time in info.values()]
        x=[value-min(x) for value in x]

        # x=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
        plt.subplot(211)
        plt.title("Month's Temperature ")
        plt.xlabel('time/day')
        plt.ylabel('temperature/degree')
        plt.xlim([0,31])
        plt.ylim([-10,40])
        plt.grid(True)
        plt.plot(x,y,'-')

        y = [int(num['humidity']) for num in info.values()]
        x = [(time['data'].date().day + time['data'].time().hour / 24) for time in info.values()]
        x = [value - min(x) for value in x]
        plt.subplot(212)
        plt.title("Month's humidity ")
        plt.xlabel('time/day')
        plt.ylabel('humidity/%')
        plt.xlim([0, 31])
        plt.ylim([-10, 40])
        plt.grid(True)
        plt.plot(x, y, '-')

        plt.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95, hspace=1.0,
                            wspace=0.35)

        plt.savefig('./weixin/plot/test.jpg')
        plt.clf()
        with open('./weixin/plot/test.jpg','rb') as f:
            media_id=wechat_instance.upload_media('image',f,extension='jpg')
            print(media_id)
        # wechat_instance.response_image(media_id=media_id)
        os.remove('./weixin/plot/test.jpg')
        return wechat.response_image(media_id=media_id['media_id'])

    elif keys=='V1001_GOOD':
        reply_text="宇宙无敌超级组合，啦啦啦啦啦"
        return wechat.response_text(content=reply_text)
