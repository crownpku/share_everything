# coding: UTF-8
import hashlib
import time
from flask import Flask, request, make_response, render_template
import xml.etree.ElementTree as ET
import model

app = Flask(__name__)
app.debug = True
#微信验证
@app.route('/', methods=['GET','POST'])
def wechat_auth():
    if request.method == 'GET':
        token = 'weixin'
        query = request.args
        signature = query.get('signature','')
        timestamp = query.get('timestamp', '')
        nonce = query.get('nonce', '')
        echostr = query.get('echostr', '')
        s = [timestamp, nonce, token]
        s.sort()
        s = ''.join(s)
        if (hashlib.sha1(s).hexdigest() == signature):
            response = make_response(echostr)
            response.headers['content-type'] = 'text'
            #response.headers['charset'] = 'utf-8'
            #这步很关键，不然会出错
            return response
    else:  
        ###这里就是处理用户发来的消息了
    	rec = request.stream.read()
    	xml_rec = ET.fromstring(rec)
        content = xml_rec.find('Content').text
    	toUser= xml_rec.find('ToUserName').text
    	fromUser = xml_rec.find('FromUserName').text
    	reply = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[%s]]></Content><FuncFlag>0</FuncFlag></xml>"
    	reply_news_temp_head = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[news]]></MsgType><ArticleCount>%s</ArticleCount><Articles>"
    	reply_news_temp_body = "<item><Title><![CDATA[%s]]></Title><Description><![CDATA[%s]]></Description><PicUrl><![CDATA[%s]]></PicUrl><Url><![CDATA[%s]]></Url></item>"
    	reply_news_temp_foot = "</Articles></xml>"
    	msgType = xml_rec.find('MsgType').text
    	if msgType == 'text':   
            #根据msgType来处理信息（text,image...)
            #pass
            
            content = content.strip().split('+')
            return_result = '貌似出错了......'
            try:
            #if True:
            	#wuru+产品名称
            	if content[0].strip() == 'wuru':
                    product_details = content[1].strip()
                    product_id = model.wuru(fromUser, product_details)
                    return_result = u'您的物品('+product_details+u')的物品ID是:[' + product_id + u'],您可以随时点击"随便看看"查看'
                    response = make_response(reply % (fromUser,toUser,str(int(time.time())),return_result))
                    response.headers['content_type']='application/xml'
                    return response
                #wuruid+产品id
                if content[0].strip() == 'wuruid':
                    product_id = content[1].strip()
                    checkcode = model.wuruid(fromUser, product_id)
                    return_result = u'该物品ID是[' + product_id + u'],验证码是: ' + checkcode + u',请您发给原使用者进行物出确认'
                    response = make_response( reply % (fromUser,toUser,str(int(time.time())),return_result))
                    response.headers['content_type']='application/xml'
                    return response
                #wuchu+产品id+checkcode
                if content[0] == 'wuchu':
                    product_id = content[1].strip()
                    checkcode = content[2].strip()
                    product_details = model.wuchu(fromUser, product_id, checkcode)
                    return_result = u'您的物品('+product_details+u') 物品ID[' + product_id + u']的使用权已经成功给出。'
                    response = make_response( reply % (fromUser,toUser,str(int(time.time())),return_result))
                    response.headers['content_type']='application/xml'
                    return response
            except Exception as e:
                print e
            #    pass
                
                
            response = make_response( reply % (fromUser,toUser,str(int(time.time())),return_result))
            response.headers['content_type']='application/xml'
            return response