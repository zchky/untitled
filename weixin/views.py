# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
# from zinnia.models.entry import Entry

from wechat_sdk import WechatBasic,WechatConf
from wechat_sdk.exceptions import ParseError
from wechat_sdk.messages import TextMessage, VoiceMessage, ImageMessage, VideoMessage, LinkMessage, LocationMessage,EventMessage
from untitled.settings import WECHAT_TOKEN, WEIXIN_APPID, WEIXIN_APPSECRET



# wechat_instance = WechatBasic(
# token=WECHAT_TOKEN,
# appid=WEIXIN_APPID,
# appsecret=WEIXIN_APPSECRET
# )

conf=WechatConf(
token=WECHAT_TOKEN,
appid=WEIXIN_APPID,
appsecret=WEIXIN_APPSECRET
)

wechat_instance=WechatBasic(conf=conf)

@csrf_exempt
def wechat(request):
    # if request.method == 'GET':
        # 检验合法性
    # 从 request 中提取基本信息 (signature, timestamp, nonce, xml)
    signature = request.GET.get('signature')
    timestamp = request.GET.get('timestamp')
    nonce = request.GET.get('nonce')

    if not wechat_instance.check_signature(
            signature=signature, timestamp=timestamp, nonce=nonce):
        return HttpResponseBadRequest('Verify Failed')
    else:
        if request.method == 'GET':
            response = request.GET.get('echostr', 'error')
        else:
            try:
                wechat_instance.parse_data(request.body)
                message = wechat_instance.get_message()
                if isinstance(message, TextMessage):
                    reply_text = '叔叔不约'
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
                elif isinstance(message,EventMessage):
                    if message.type=='subscribe':
                        reply_text="test1"
                else:
                    reply_text = 'other'
                response = wechat_instance.response_text(content=reply_text)
            except ParseError:
                return HttpResponseBadRequest('Invalid XML Data')
        return HttpResponse(response, content_type="application/xml")

# 解析本次请求的 XML 数据
