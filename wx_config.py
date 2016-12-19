# -*- coding: UTF-8 -*-
import time
import random
import string
import hashlib
import requests

class Sign:
    ''' ʵ������ʼֵ '''
    def __init__(self, appid, appsecret, url):
        self.access_token = self.get_access_token(appid, appsecret)
        self.jsapi_ticket = self.get_ticket(self.access_token)
        self.ret = {
            'nonceStr': self.__create_nonce_str(),
            'jsapi_ticket': self.jsapi_ticket,
            'timestamp': self.__create_timestamp(),
            'url': url
        }

    ''' ��ȡ����ַ��� '''
    def __create_nonce_str(self):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))

    ''' ��ȡʱ��� '''
    def __create_timestamp(self):
        return int(time.time())

    ''' ��ȡaccess_token '''
    def get_access_token(self, appid, appsecret):
        url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}'.format(appid, appsecret)
        r = requests.get(url)
        data = r.json()
        access_token = data.get('access_token')
        return access_token

    ''' ��ȡjsapi_ticket '''
    def get_ticket(self, access_token, type="jsapi"):
        url = 'https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token={}&type={}'.format(access_token, type)
        r = requests.get(url)
        data = r.json()
        ticket = data.get('ticket')
        return ticket

    ''' ��ȡsignature '''
    def sign(self):
        string = '&'.join(['%s=%s' % (key.lower(), self.ret[key]) for key in sorted(self.ret)])
        # print string
        self.ret['signature'] = hashlib.sha1(string).hexdigest()
        return self.ret

if __name__ == '__main__':
    appid, appsecret = 'wx641c38dc8b432148', '18d64c141276a60f17db6c462edf822e'
    url = 'https://www.baidu.com/'
    sign = Sign(appid, appsecret, url)
    print '���ʱ���: ', sign.ret.get('timestamp')
    print '����ַ���: ', sign.ret.get('nonceStr')
    print 'URL: ', sign.ret.get('url')
    print 'access_token: ', sign.access_token
    print 'jsapi_ticket: ', sign.jsapi_ticket
    # ����signaturn����
    sign.sign()
    print 'ǩ����', sign.ret.get('signature')
