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

from untitled.settings import WECHAT_TOKEN, WEIXIN_APPID, WEIXIN_APPSECRET,BASE_DIR
from weixin.models import data,user,device,UserAndDevice
from weixin.wechat import info
# from weixin.models import DoesNotExist
import numpy as np
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

# create_menu(info_draw.menu)

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

def save_data(message,bind_num):
    tem=random.randint(0,20)
    hum=random.randint(0,20)
    somke_num = float(random.randint(0, 100)) / float(100)
    gas_num = float(random.randint(0, 100)) / float(100)
    data.objects.create(user=str(message.source),temperature=tem,humidity=hum,gas=gas_num,somke=somke_num)
    print(data.objects.all())

def save_device(message,bind_num):
    if device.objects.filter(device_id=bind_num):
        new_user=user.objects.get_or_create(user=str(message.source))
        the_user=user.objects.get(user=message.source)
        device_id=device.objects.get(device_id=bind_num)
        UserAndDevice.objects.create(UAD_user=the_user,UAD_device_id=device_id)
        return "绑定成功"
    else:
        return "绑定失败"

def delete_device(message,delete_num):
    # if device.objects.filter(device_id=bind_num)
     if UserAndDevice.objects.filter(UAD_user__user=message.source,UAD_device_id__device_id=delete_num):
        the_user=user.objects.get(user=str(message.source))
        device_id=device.objects.get(device_id=delete_num)
        UserAndDevice.objects.get(UAD_user=the_user,UAD_device_id=device_id).delete()
        if UserAndDevice.objects.filter(UAD_user=the_user):
            pass
        else:
            the_user.delete()
        return "删除成功"
     else:
        return "删除失败"


def textswitch(message):
    # try:
    #     com = re.compile(r'^(.*)-(.*)')
    #     bind = com.match(message.content).groups()
    # except AttributeError as e:
    #     print('error:',e)
    #     bind=[1,2]
    # try:
    # r = user.objects.get(user=message.source).data_set.all().values()

    reply_text = "尊敬的用户您好"
    if message.content=='save':
        print(message.source)
        print(message.id)
        reply_text=reply_text+"save ok"
    # elif bind[0]=='bind':
    elif message.content[0:4]=='bind':
        # bind_num=bind[1]
        bind_str=message.content[5:]
        reply_text=save_device(message,bind_str)
    elif message.content[0:6]=='delete':
        delete_str=message.content[7:]
        print(delete_str)
        reply_text=delete_device(message,delete_str)
    elif message.content == '0':
        reply_text = info.message_reply_0_test
    elif message.content in ['1','2','3','4']:
        try:
            if user.objects.filter(user=message.source):
                result=[]
                unit=[]
                dev = UserAndDevice.objects.filter(UAD_user__user=message.source)
                for i in dev:
                    dev_id = i.UAD_device_id.device_id
                    try:
                        text = device.objects.filter(device_id=dev_id).first().data_set.order_by(
                            '-data').first()
                        unit=[dev_id,text.data.strftime("%B %d,%Y"),text.temperature,text.humidity,text.smoke,text.gas ]
                        result.append(unit)
                    except BaseException as e:
                        print('error',e)
                if message.content=='1':
                     for i in result:
                        reply_text=reply_text+"设备%s:当前时间%s,气温为%s。 "%(i[0],i[1],i[2])
                elif message.content=='2':
                    for i in result:
                        reply_text = reply_text + "设备%s:当前时间%s,湿度为%s。 " % (i[0], i[1], i[3])
                elif message.content=='3':
                    for i in result:
                        reply_text = reply_text + "设备%s:当前时间%s,烟雾浓度为%s。 " % (i[0], i[1], i[4])
                elif message.content=='4':
                    for i in result:
                        reply_text = reply_text + "设备%s:当前时间%s,可燃气体浓度为%s。 " % (i[0], i[1], i[5])
            else:
                reply_text=reply_text+"用户不存在"
        except ex.ObjectDoesNotExist as e:
            e=' Error: '+str(e)
            reply_text=reply_text+e
            print('error',e)
    return  reply_text

def draw_plot(keys,wechat):
    reply_text = "尊敬的用户您好"
    if keys=='V1001_GOOD':
        reply_text="宇宙无敌超级组合，啦啦啦啦啦"
        return wechat.response_text(content=reply_text)

    elif keys=='V1001_BIND':
        reply_text=info.message_reply_bind
        return wechat.response_text(content=reply_text)
    elif keys=='V1001_SELF':
        reply_text=info.message_reply_building
        return wechat.response_text(content=reply_text)
    elif keys=='V1001_DELETE':
        reply_text=info.message_reply_delete
        return wechat.response_text(content=reply_text)
    elif keys=='V1001_CHANGE':
        reply_text=info.message_reply_building
        return  wechat.response_text(content=reply_text)

    elif keys in ['V1001_CON1','V1001_CON2','V1001_CON3']:
        reply_text=info.message_reply_building
        return wechat.response_text(content=reply_text)

    elif user.objects.filter(user=wechat.message.source):
        y = [[],[],[],[],[]]
        x = []
        # print(wechat.message.source)
        dev = UserAndDevice.objects.filter(UAD_user__user=wechat.message.source)
        print(dev)
        diff_one=datetime.datetime.combine(datetime.date.today(),datetime.time(0,0,0,0))
        diff_seven=datetime.datetime.today()-datetime.timedelta(days=7)
        diff_thirty=datetime.datetime.today()-datetime.timedelta(days=30)
        diff_time=[diff_one,diff_seven,diff_thirty]
        for i in dev:
            dev_id = i.UAD_device_id.device_id
            count=None
            if keys=='V1001_TODAY_PLOT':
                count=0
                info_draw=data.objects.filter(data_device_id__device_id=dev_id,data__lt=datetime.datetime.now(),data__gt=diff_time[count]).order_by('-data')
                x_one=[(time['data'].time().hour+time['data'].time().minute/60) for time in info_draw.values()]

            elif keys=='V1001_WEEK_PLOT':
                count=1
                info_draw=data.objects.filter(data_device_id__device_id=dev_id,data__lt=datetime.datetime.now(),data__gt=diff_time[count]).order_by('-data')
                print(info_draw.values())
                # x_one = [(time['data'].date().day + time['data'].time().hour / 24) for time in info_draw.values()]
                # x_one = [value - min(x_one) for value in x_one]
                x_one=[(time['data']-diff_seven) for time in info_draw.values()]
                x_one=[value.total_seconds()/86400 for value in x_one]

            elif keys == 'V1001_MONTH_PLOT':
                count=2
                info_draw=data.objects.filter(data_device_id__device_id=dev_id,data__lt=datetime.datetime.now(),data__gt=diff_time[count]).order_by('-data')
                # x_one = [(time['data'].date().day + time['data'].time().hour / 24) for time in info_draw.values()]
                # x_one = [value - min(x_one) for value in x_one]
                x_one=[(time['data']-diff_thirty) for time in info_draw.values()]
                x_one=[value.total_seconds()/86400 for value in x_one]

            # print(count)
            if count in [0,1,2]:
                # print("ok")
                info_draw=data.objects.filter(data_device_id__device_id=dev_id,data__lt=datetime.datetime.now(),data__gt=diff_time[count]).order_by('-data')
                # print(info_draw.values())
                y_tem=[int(num['temperature']) for num in info_draw.values()]
                y_hum=[int(num['humidity']) for num in info_draw.values()]
                y_smo=[int(num['smoke']) for num in info_draw.values()]
                y_gas=[int(num['gas']) for num in info_draw.values()]
                y[0].append(y_tem)
                y[1].append(y_hum)
                y[2].append(y_smo)
                y[3].append(y_gas)
                x.append(x_one)
                print(y)
                print(x)

        for i in range(4):
            y_plot = np.array(y[i])
            y_plot = y_plot.transpose()
            y[i]=y_plot
        x_plot = np.array(x)
        x_plot = x_plot.transpose()
        x= x_plot
        # for i in dev:
        #     dev_id = i.user_device_id.device_id
        #     try:
        #         text = device.objects.filter(user=message.source, user_device_id=dev_id).first().data_set.order_by(
        #             '-data').first()
        #         unit = [dev, text.data.strftime("%B %d,%Y"), text.temperature, text.humidity, text.smoke, text.gas]
        #         result.append(unit)
        #     except BaseException as e:
        #         print('error', e)
        if keys=='V1001_TODAY_PLOT':
            # info_draw=data.objects.filter(data__lt=datetime.datetime.now(),data__gt=datetime.datetime.combine(datetime.date.today(),datetime.time(0,0,0,0)))
            #
            # y=[int(num['temperature']) for num in info_draw.values()]
            # x=[(time['data'].time().hour+time['data'].time().minute/60) for time in info_draw.values()]
            plt.subplot(221)
            plt.title("Today's Temperature ")
            plt.xlabel('time/hr')
            plt.ylabel('temperature/degree')
            plt.xlim([0,24])
            plt.ylim([-10,40])
            plt.grid(True)

            plt.plot(x,y[0],'-')

            # y = [int(num['humidity']) for num in info_draw.values()]
            # x = [(time['data'].time().hour + time['data'].time().minute / 60) for time in info_draw.values()]
            plt.subplot(222)
            plt.title("Today's humidity ")
            plt.xlabel('time/hr')
            plt.ylabel('humidity/%')
            plt.xlim([0,24])
            plt.ylim([-10,40])
            plt.grid(True)
            plt.plot(x,y[1],'-')

            plt.subplot(223)
            plt.title("Today's smoke ")
            plt.xlabel('time/hr')
            plt.ylabel('percentage/%')
            plt.xlim([0,24])
            plt.ylim([0,100])
            plt.grid(True)
            plt.plot(x,y[2],'-')

            plt.subplot(224)
            plt.title("Today's gas ")
            plt.xlabel('time/hr')
            plt.ylabel('percentage/%')
            plt.xlim([0,24])
            plt.ylim([0,100])
            plt.grid(True)
            plt.plot(x,y[3],'-')

            plt.suptitle("this is a test", fontsize=28)
            plt.subplots_adjust(top=0.85, bottom=0.08, left=0.10, right=0.95, hspace=0.7,
                                wspace=0.35)
            plt.savefig('./weixin/plot/test.jpg')
            plt.clf()

            test=os.path.join(BASE_DIR,'weixin/plot/test.jpg')
            test=os.path.abspath('.')
            test=os.path.join(test,'weixin/plot/test.jpg')
            print(test)
            with open('./weixin/plot/test.jpg','rb') as f:
                media_id=wechat_instance.upload_media('image',f,extension='jpg')
                print(media_id)
            os.remove('./weixin/plot/test.jpg')
            return wechat.response_image(media_id=media_id['media_id'])

        elif keys=='V1001_WEEK_PLOT':
            # info_draw=data.objects.filter(data__lt=datetime.datetime.now(),data__gt=datetime.datetime(datetime.date.today().year,datetime.date.today().month,datetime.date.today().day-7,0,0,0,0))
            # y=[int(num['temperature']) for num in info_draw.values()]
            # x=[(time['data'].date().day+time['data'].time().hour/24) for time in info_draw.values()]
            # x=[value-min(x) for value in x]
            plt.subplot(221)
            plt.title("Week's Temperature ")
            plt.xlabel('time/day')
            plt.ylabel('temperature/degree')
            plt.xlim([0,7])
            plt.ylim([-10,40])
            plt.grid(True)
            plt.plot(x,y[0],'-')

            # y = [int(num['humidity']) for num in info_draw.values()]
            # x = [(time['data'].date().day + time['data'].time().hour / 24) for time in info_draw.values()]
            # x = [value - min(x) for value in x]
            plt.subplot(222)
            plt.title("Week's humidity ")
            plt.xlabel('time/day')
            plt.ylabel('humidity/%')
            plt.xlim([0, 7])
            plt.ylim([-10, 40])
            plt.grid(True)
            plt.plot(x, y[1], '-')

            plt.subplot(223)
            plt.title("Week's Temperature ")
            plt.xlabel('time/day')
            plt.ylabel('temperature/degree')
            plt.xlim([0,7])
            plt.ylim([-10,40])
            plt.grid(True)
            plt.plot(x,y[2],'-')

            plt.subplot(224)
            plt.title("Week's Temperature ")
            plt.xlabel('time/day')
            plt.ylabel('temperature/degree')
            plt.xlim([0,7])
            plt.ylim([-10,40])
            plt.grid(True)
            plt.plot(x,y[3],'-')

            plt.suptitle("this is a test", fontsize=28)
            plt.subplots_adjust(top=0.85, bottom=0.08, left=0.10, right=0.95, hspace=0.7,
                                wspace=0.35)

            plt.savefig('./weixin/plot/test.jpg')
            plt.clf()
            with open('./weixin/plot/test.jpg','rb') as f:
                media_id=wechat_instance.upload_media('image',f,extension='jpg')
                print(media_id)
            os.remove('./weixin/plot/test.jpg')
            return wechat.response_image(media_id=media_id['media_id'])

        elif keys=='V1001_MONTH_PLOT':
            # info_draw=data.objects.filter(data__lt=datetime.datetime.now(),data__gt=datetime.datetime(datetime.date.today().year,datetime.date.today().month,1,0,0,0,0))
            # y=[int(num['temperature']) for num in info_draw.values()]
            # x=[(time['data'].date().day+time['data'].time().hour/24) for time in info_draw.values()]
            # x=[value-min(x) for value in x]
            plt.subplot(221)
            plt.title("Month's Temperature ")
            plt.xlabel('time/day')
            plt.ylabel('temperature/degree')
            plt.xlim([0,31])
            plt.ylim([-10,40])
            plt.grid(True)
            plt.plot(x,y[0],'-')

            # y = [int(num['humidity']) for num in info_draw.values()]
            # x = [(time['data'].date().day + time['data'].time().hour / 24) for time in info_draw.values()]
            # x = [value - min(x) for value in x]
            plt.subplot(222)
            plt.title("Month's humidity ")
            plt.xlabel('time/day')
            plt.ylabel('humidity/%')
            plt.xlim([0, 31])
            plt.ylim([-10, 40])
            plt.grid(True)
            plt.plot(x, y[1], '-')

            plt.subplot(223)
            plt.title("Month's humidity ")
            plt.xlabel('time/day')
            plt.ylabel('humidity/%')
            plt.xlim([0, 31])
            plt.ylim([-10, 40])
            plt.grid(True)
            plt.plot(x, y[2], '-')

            plt.subplot(224)
            plt.title("Month's humidity ")
            plt.xlabel('time/day')
            plt.ylabel('humidity/%')
            plt.xlim([0, 31])
            plt.ylim([-10, 40])
            plt.grid(True)
            plt.plot(x, y[3], '-')

            plt.suptitle("this is a test", fontsize=28)
            plt.subplots_adjust(top=0.85, bottom=0.08, left=0.10, right=0.95, hspace=0.7,
                                wspace=0.35)

            plt.savefig('./weixin/plot/test.jpg')
            plt.clf()
            with open('./weixin/plot/test.jpg','rb') as f:
                media_id=wechat_instance.upload_media('image',f,extension='jpg')
                print(media_id)
            # wechat_instance.response_image(media_id=media_id)
            os.remove('./weixin/plot/test.jpg')
            return wechat.response_image(media_id=media_id['media_id'])

    else:
        reply_text=info.message_reply_no_user
        return wechat.response_text(content=reply_text)
