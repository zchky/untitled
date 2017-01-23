from .functions import weather_api

# -*- coding: utf-8 -*-


message_subscribe = "欢迎订阅玄云子物联网平台，本平台现在正处于测试中，输入1：\"查看当前香港天气情况\"，输入2:\"待定\",输入3:\"随机生成数据\"，输入4:\"返回最新数据\",输入其他:\"获得关键词\""
# message_reply_1_test = weather_api()
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
                'url': url+'today_plot'
            },
            {
                'type': 'click',
                'name': '本周图表数据',
                'url': url+'week_plot'
            },
            {
                'type': 'click',
                'name': '本月图表数据',
                'url': url+'month_plot'
            }
    ]
},
{
    'name': '关于我们',
    'sub_button': [
        {
            'type': 'view',
            'name': '搜索',
            'url': 'http://www.soso.com/'
        },
        {
            'type': 'view',
            'name': '视频',
            'url': 'http://v.qq.com/'
        },
        {
            'type': 'click',
            'name': '赞一下我们',
            'key': 'V1001_GOOD'
        }
    ]
}
]
}
