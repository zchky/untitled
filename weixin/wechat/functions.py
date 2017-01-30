# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import django.core.exceptions as ex

import datetime
import json
import os
import random
from urllib.request import urlopen
import re

import matplotlib.pyplot as plt
from wechat_sdk import WechatBasic,WechatConf

from untitled.settings import WECHAT_TOKEN, WEIXIN_APPID, WEIXIN_APPSECRET
from weixin.models import test_data,test_user,test_device
from weixin.wechat import info
# from weixin.models import DoesNotExist

conf=WechatConf(
token=WECHAT_TOKEN,
appid=WEIXIN_APPID,
appsecret=WEIXIN_APPSECRET,
encrypt_mode='normal',
encoding_ase_key='1pParL1h55XglOTuNjo2PQtFIRDdjHJMoP8wzTMet9S'
)
#
wechat_instance = WechatBasic(conf=conf)

wait_list=[]

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

def save_test_data(message,bind_num):
    tem=random.randint(0,20)
    hum=random.randint(0,20)
    somke_num = float(random.randint(0, 100)) / float(100)
    gas_num = float(random.randint(0, 100)) / float(100)
    test_data.objects.create(user=str(message.source),temperature=tem,humidity=hum,gas=gas_num,somke=somke_num)
    print(test_data.objects.all())

def save_test_user(message,bind_num):
    if test_device.objects.filter(device_id=bind_num):
        device_id=test_device(device_id=bind_num)
        test_user.objects.create(user=str(message.source),user_device_id=device_id)
        return "save successfully"
    else:
        return "save failed,device id doesnot exist"


def textswitch(message):
    reply_text = "尊敬的用户您好"
    try:
        com = re.compile(r'^(.*)-(.*)')
        bind = com.match(message.content).groups()
    except AttributeError as e:
        print('error:',e)
        bind=[1,2]
    # try:
    # r = test_user.objects.get(user=message.source).test_data_set.all().values()
    if message.content == '0':
        reply_text = info.message_reply_0_test
    try:
        if message.content=='1':
             # text=test_data.objects.filter(user=message.source,data__lt=datetime.datetime.now()).order_by('-data').values()[0]
            device = test_user.objects.filter(user=message.source)
            for i in device:
                dev=i.user_device_id.first().device_id
                text = test_user.objects.filter(user=message.source,user_device_id=dev).first().test_data_set.order_by('-data').first()
                print(text)
                reply_text=reply_text+"设备%s:当前时间%s,气温为%s。 "%(dev,text.data.strftime("%B %d,%Y"),text.temperature)
        elif message.content=='2':
            r = test_user.objects.get(user=message.source).test_data_set.all().values()
            for text in r:
                reply_text = reply_text + "设备%s:当前时间%s,湿度为%s。 " % (
                text['data_device_id_id'], text['data'].strftime("%B %d,%Y"), text['humidity'])
        elif message.content=='3':
            r = test_user.objects.get(user=message.source).test_data_set.all().values()
            for text in r:
                reply_text = reply_text + "设备%s:当前时间%s,烟雾浓度为%s。 " % (
                    text['data_device_id_id'], text['data'].strftime("%B %d,%Y"), text['smoke'])
        elif message.content=='4':
            r = test_user.objects.get(user=message.source).test_data_set.all().values()
            for text in r:
                reply_text = reply_text + "设备%s:当前时间%s,可燃气体浓度为%s。 " % (
                    text['data_device_id_id'], text['data'].strftime("%B %d,%Y"), text['gas'])
    except ex.ObjectDoesNotExist as e:
        e=' Error: '+str(e)
        reply_text=reply_text+e
        print('error',e)
    if message.content=='save':
        # save_test_data(message)
        # reply_text= "save ok"
        print(message.source)
        print(message.id)
        reply_text=reply_text+"save ok"
    elif bind[0]=='bind':
        bind_num=bind[1]
        reply_text=save_test_user(message,bind_num)
    return  reply_text

def draw_plot(keys,wechat):
    if keys=='V1001_TODAY_PLOT':
        info=test_data.objects.filter(data__lt=datetime.datetime.now(),data__gt=datetime.datetime.combine(datetime.date.today(),datetime.time(0,0,0,0)))
        y=[int(num['temperature']) for num in info.values()]
        x=[(time['data'].time().hour+time['data'].time().minute/60) for time in info.values()]
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

    elif keys=='V1001_TODAY_MUSIC':
        reply_text=info.message_reply_bind
        return wechat.response_text(content=reply_text)