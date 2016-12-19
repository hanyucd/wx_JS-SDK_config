# -*- coding: UTF-8 -*-
import time
import random
import string
import hashlib
import requests

class Sign:
    ''' 实例化初始值 '''
    def __init__(self, appid, appsecret, url):
        self.access_token = self.get_access_token(appid, appsecret)
        self.jsapi_ticket = self.get_ticket(self.access_token)
        self.ret = {
            'nonceStr': self.__create_nonce_str(),
            'jsapi_ticket': self.jsapi_ticket,
            'timestamp': self.__create_timestamp(),
            'url': url
        }

    ''' 获取随机字符串 '''
    def __create_nonce_str(self):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))

    ''' 获取时间戳 '''
    def __create_timestamp(self):
        return int(time.time())

    ''' 获取access_token '''
    def get_access_token(self, appid, appsecret):
        url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}'.format(appid, appsecret)
        r = requests.get(url)
        data = r.json()
        access_token = data.get('access_token')
        return access_token

    ''' 获取jsapi_ticket '''
    def get_ticket(self, access_token, type="jsapi"):
        url = 'https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token={}&type={}'.format(access_token, type)
        r = requests.get(url)
        data = r.json()
        ticket = data.get('ticket')
        return ticket

    ''' 获取signature '''
    def sign(self):
        string = '&'.join(['%s=%s' % (key.lower(), self.ret[key]) for key in sorted(self.ret)])
        # print string
        self.ret['signature'] = hashlib.sha1(string).hexdigest()
        return self.ret

if __name__ == '__main__':
    appid, appsecret = 'wx641c38dc8b432148', '18d64c141276a60f17db6c462edf822e'
    url = 'https://www.baidu.com/'
    sign = Sign(appid, appsecret, url)
    print '随机时间戳: ', sign.ret.get('timestamp')
    print '随机字符串: ', sign.ret.get('nonceStr')
    print 'URL: ', sign.ret.get('url')
    print 'access_token: ', sign.access_token
    print 'jsapi_ticket: ', sign.jsapi_ticket
    # 调用signaturn函数
    sign.sign()
    print '签名：', sign.ret.get('signature')
