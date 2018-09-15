#!/usr/bin/python
# -*- coding: UTF-8 -*-

from __future__ import unicode_literals

import datetime

import requests
import feedparser
from flask import Flask,render_template,request,make_response

app = Flask(__name__)


def rss_feed(publication):
    RSS_FEED ={
"zhihu": "https://www.zhihu.com/rss",
"songshuhui": "http://songshuhui.net/feed",
"ifeng": "http://news.ifeng.com/rss/index.xml",
"guojixinwen":"http://news.qq.com/newsgj/rss_newswj.xml",
"guoneixinwen":"http://news.qq.com/newsgn/rss_newsgn.xml",
"lishi":"http://news.qq.com/histor/rss_history.xml",
}
    #print('publication is',publication)
    #print(type(publication))
    if str(publication) in RSS_FEED.keys():

        return RSS_FEED[publication]
    else:
        return RSS_FEED["songshuhui"]



DEFAULTS = {
'city': '北京',
'publication': 'guojixinwen',
}

WEATHERS = {
"北京": 101010100,
            "上海": 101020100,
            "广州": 101280101,
            "深圳": 101280601,
}


def get_value_with_fallback(key,*args,**kwargs):
    if request.args.get(key):
        return request.args.get(key)
    if request.cookies.get(key):
        #print('request.cookies')
        #print(request.cookies)
        #{'Pycharm-bdfc5fce': '44e1e6e2-1007-463a-9c3d-891072768e2e', 'session': 'eyJfcGVybWFuZW50Ijp0cnVlLCJ1c2VyX2lkIjpudWxsfQ.Dn3_kQ.Z__XTqr0WsANIF21pwva2qpNHyo', 'city': '广州', 'publication': 'guoneixinwen'}
        #print('key')
        #print(key)  #city
        return request.cookies.get(key)
    #else:
        #return DEFAULTS[key]
    return DEFAULTS[key]

def get_news(publication):
    # feedparser解析RSS
    #print('RSS_FEED is',RSS_FEED[publication])
    #if RSS_FEED[publication] is not None:
    #feed = feedparser.parse(RSS_FEED[publication])
    feed = feedparser.parse(rss_feed(publication))
    print ("feed['entries']is",feed['entries'])
    return feed['entries']
    #else:
        #return feedparser.parse(RSS_FEED['guojixinwen'])

    #print ('feed is',feed)
    #return feed['entries']

def get_weather(city):
    code = WEATHERS.get(city,101010100)
    url = "http://www.weather.com.cn/data/sk/{0}.html".format(code)

    r =requests.get(url)
    r.encoding = 'utf-8'

    data = r.json()['weatherinfo']
    return dict(city=data['city'],temperature=data['temp'],
                description=data['WD'])

@app.route('/')
def home():
    publication = get_value_with_fallback('publication')
    print ('publication is',publication)
    city = get_value_with_fallback('city')

    weather = get_weather(city)
    articles = get_news(publication)
    print ('articles is',articles)

    response = make_response(render_template('home.html',articles=articles,
                                             weather=weather))
    expires = datetime.datetime.now() + datetime.timedelta(days=365)
    print ('expires')
    print (expires)
    #2019-09-15 12:46:40.261721
    response.set_cookie('publication', publication, expires=expires)
    response.set_cookie('city', city, expires=expires)

    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)



