from __future__ import unicode_literals


from wechat_sdk import WechatBasic,WechatConf
from untitled.settings import WECHAT_TOKEN, WEIXIN_APPID, WEIXIN_APPSECRET


menu={"button":[
  {   "name":"个人菜单",
       "sub_button":[
  {
    "type": "click",
    "name": "个人信息",
    "key": "V1001_SELF"
  },
  {
    "type": "click",
    "name": "设备绑定",
    "key": "V1001_BIND"
  },
  {
    "type": "click",
    "name": "设备删除",
    "key": "V1001_DELETE"
  },
  {
    "type": "click",
    "name": "设备更换",
    "key": "V1001_CHANGE"
  }
]
},
{
  "name": "查询目录",
  "sub_button": [
    {
      "type": "click",
      "name": "日图表数据",
      "key": "V1001_TODAY_PLOT"
    },
    {
      "type": "click",
      "name": "周图表数据",
      "key": "V1001_WEEK_PLOT"
    },
    {
      "type": "click",
      "name": "月图表数据",
      "key": "V1001_MONTH_PLOT"
    }]
},
{
  "name": "控制目录",
  "sub_button": [
    {
      "type": "click",
      "name": "控制—1",
      "key": "V1001_CON1"
    },
    {
      "type": "click",
      "name": "控制—2",
      "key": "V1001_CON2"
    },
    {
      "type": "click",
      "name": "控制—3",
      "key": "V1001_CON3"
    },
{
  "type": "click",
  "name": "关于我们",
  "key": "V1001_GOOD"
}
]
}
]
}





conf=WechatConf(
  token=WECHAT_TOKEN,
  appid=WEIXIN_APPID,
  appsecret=WEIXIN_APPSECRET,
  encrypt_mode='normal',
  encoding_ase_key='1pParL1h55XglOTuNjo2PQtFIRDdjHJMoP8wzTMet9S'
)
#
wechat_instance = WechatBasic(conf=conf)


wechat_instance.create_menu(menu_data=menu)