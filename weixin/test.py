from wechat_sdk import WechatBasic,WechatConf
from wechat_sdk.exceptions import ParseError
from wechat_sdk.messages import TextMessage, VoiceMessage, ImageMessage, VideoMessage, LinkMessage, LocationMessage,EventMessage,ShortVideoMessage
from untitled.settings import WECHAT_TOKEN, WEIXIN_APPID, WEIXIN_APPSECRET
import random

conf=WechatConf(
token=WECHAT_TOKEN,
appid=WEIXIN_APPID,
appsecret=WEIXIN_APPSECRET,
encrypt_mode='normal',
encoding_ase_key='1pParL1h55XglOTuNjo2PQtFIRDdjHJMoP8wzTMet9S'
)
#
wechat_instance = WechatBasic(conf=conf)
url='http://138.19.95.53/weixin/test/'
menu = {
    'button': [
        {
            'type': 'click',
            'name': '个人目录',
            'key': 'V1001_TODAY_MUSIC'
        },
        {
            'type': 'click',
            'name': '信息查询',
            'key': 'V1001_TODAY_SINGER',
            'sub_button': [
            {
                'type': 'click',
                'name': '当日图表数据',
                'key': 'V1001_TODAY_PLOT'
            },
            {
                'type': 'click',
                'name': '本周图表数据',
                'key': 'V1001_WEEK_PLOT'
            },
            {
                'type': 'click',
                'name': '本月图表数据',
                'key': 'V1001_MONTH_PLOT'
            }
    ]
},
{
    'type': 'click',
    'name': '关于我们',
    'key':'V1001_GOOD'
    # 'sub_button': [
    #     {
    #         'type': 'view',
    #         'name': '搜索',
    #         'url': 'http://www.soso.com/'
    #     },
    #     {
    #         'type': 'view',
    #         'name': '视频',
    #         'url': 'http://v.qq.com/'
    #     },
    #     {
    #         'type': 'click',
    #         'name': '赞一下我们',
    #         'key': 'V1001_GOOD'
    #     }
    # ]
}
]
}
def create_menu(menu):
    wechat_instance.create_menu(menu)

import matplotlib.pyplot as plt

def test_draw():
    x=[13.6, 13.683333333333334, 14.516666666666667, 14.833333333333334]
    y=[14, 12, 20, 13]
    plt.xlim([0, 24])
    plt.ylim([-10, 40])
    plt.subplot(211)
    plt.plot(x,y)

    plt.subplot(212)
    plt.plot(x,y)
    plt.show()
    # plt.plot(x, y)
    # plt.savefig('./plot/test.jpg')

test_draw()
# create_menu(menu)
# test_draw()
# with open('./plot/test.jpg','rb') as f:
#     print(wechat_instance.upload_media('image', f,extension='jpg'))