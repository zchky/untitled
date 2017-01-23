# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
# from zinnia.models.entry import Entry

from wechat_sdk import WechatBasic,WechatConf
from wechat_sdk.exceptions import ParseError
from wechat_sdk.messages import TextMessage, VoiceMessage, ImageMessage, VideoMessage, LinkMessage, LocationMessage,EventMessage,ShortVideoMessage
from untitled.settings import WECHAT_TOKEN, WEIXIN_APPID, WEIXIN_APPSECRET
from . import info
from . import functions


# wechat_instance = WechatBasic(
# token=WECHAT_TOKEN,
# appid=WEIXIN_APPID,
# appsecret=WEIXIN_APPSECRET
# )

conf=WechatConf(
token=WECHAT_TOKEN,
appid=WEIXIN_APPID,
appsecret=WEIXIN_APPSECRET,
encrypt_mode='normal',
encoding_ase_key='1pParL1h55XglOTuNjo2PQtFIRDdjHJMoP8wzTMet9S'
)
#
wechat_instance = WechatBasic(conf=conf)


@csrf_exempt
def wechat(request):
    # if request.method == 'GET':
        # 检验合法性
    # 从 request 中提取基本信息 (signature, timestamp, nonce, xml)
    signature = request.GET.get('signature')
    timestamp = request.GET.get('timestamp')
    nonce = request.GET.get('nonce')

    print(wechat_instance.check_signature(signature=signature, timestamp=timestamp, nonce=nonce))
    if not wechat_instance.check_signature(
            signature=signature, timestamp=timestamp, nonce=nonce):
        return HttpResponseBadRequest('Verify Failed')
    else:
        if  request.method == 'GET':
            response = request.GET.get('echostr', 'error')
        else:
            try:
                wechat_instance.parse_data(request.body)
                # print(wechat_instance.parse_data(request.body))
                message = wechat_instance.get_message()
                # print(message)
                if isinstance(message, TextMessage):
                    reply_text=functions.textswitch(message)
                    response = wechat_instance.response_text(content=reply_text)
                elif isinstance(message, VoiceMessage):
                    reply_text = 'voice'
                elif isinstance(message, ImageMessage):
                    reply_text = 'image'
                elif isinstance(message, LinkMessage):
                    reply_text = 'link'
                elif isinstance(message, LocationMessage):
                    reply_text = 'location'
                elif isinstance(message, VideoMessage):
                    reply_text = 'video'
                elif isinstance(message, ShortVideoMessage):
                    reply_text = 'shortvideo'
                elif isinstance(message, EventMessage):
                    if message.type == 'subscribe':
                        reply_text = info.message_subscribe
                    elif message.type == 'click':
                        response=functions.draw_plot(message.key,wechat_instance)
                        # response=wechat_instance.response_image(media_id=media_id)
                else:
                    reply_text = 'other'
                    response = wechat_instance.response_text(content=reply_text)
            except ParseError:
                return HttpResponseBadRequest('Invalid XML Data')
        # kk=HttpResponse(response, content_type="application/xml")
        # print(type(kk))
        return HttpResponse(response, content_type="application/xml")

# 解析本次请求的 XML 数据
#
# wechat_instance.create_menu(menu)