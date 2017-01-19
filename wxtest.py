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
        msgType = xml_rec.find('MsgType').text
        
        
    	toUser= xml_rec.find('ToUserName').text
    	fromUser = xml_rec.find('FromUserName').text
    	reply = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[%s]]></Content><FuncFlag>0</FuncFlag></xml>"
    	reply_news_temp_head = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[news]]></MsgType><ArticleCount>%s</ArticleCount><Articles>"
    	reply_news_temp_body = "<item><Title><![CDATA[%s]]></Title><Description><![CDATA[%s]]></Description><PicUrl><![CDATA[%s]]></PicUrl><Url><![CDATA[%s]]></Url></item>"
    	reply_news_temp_foot = "</Articles></xml>"
    	
        
        if msgType == 'event':
            event = xml_rec.find('Event').text
            return_result = '貌似出错了......'
            if event == 'sbkk':
                return_result = model.suibiankankan(fromUser)
                response = make_response(reply % (fromUser,toUser,str(int(time.time())),return_result))
                response.headers['content_type']='application/xml'
                return response
            elif event == 'wuru':
                return_result = u"如果您是物品所有权人，第一次录入物品，请输入'wuru+物品名称'；\n如果您是借用人，请输入'wuru+物品ID'，物品ID请向原物主查询，成功后请将返回的验证码发给原物主确认。"
                response = make_response(reply % (fromUser,toUser,str(int(time.time())),return_result))
                response.headers['content_type']='application/xml'
                return response 
            elif event == 'wuchu':
                return_result = u"请输入'wuchu+物品ID+验证码'确认，验证码请向新物主查询。"
                response = make_response(reply % (fromUser,toUser,str(int(time.time())),return_result))
                response.headers['content_type']='application/xml'
                return response
            elif event == 'zssm':
                return_result = u"烦请阅读我的历史消息中的第三篇文章，谢谢！"
                response = make_response(reply % (fromUser,toUser,str(int(time.time())),return_result))
                response.headers['content_type']='application/xml'
                return response
    
        if msgType == 'text':   
            #根据msgType来处理信息（text,image...)
            #pass
            content = xml_rec.find('Content').text
            return_result = '貌似出错了......'
            try:
                if content == 'sbkk':
                    return_result = model.suibiankankan(fromUser)
                    response = make_response(reply % (fromUser,toUser,str(int(time.time())),return_result))
                    response.headers['content_type']='application/xml'
                    return response
                elif content == 'wuru':
                    return_result = u"如果您是物品所有权人，第一次录入物品，请输入'wuru+物品名称'；如果您是借用人，请输入'wuru+物品ID'，物品ID请向原物主查询。"
                    response = make_response(reply % (fromUser,toUser,str(int(time.time())),return_result))
                    response.headers['content_type']='application/xml'
                    return response 
                elif content == 'wuchu':
                    return_result = u"请输入'wuchu+物品ID+验证码'确认，验证码请向新物主查询。"
                    response = make_response(reply % (fromUser,toUser,str(int(time.time())),return_result))
                    response.headers['content_type']='application/xml'
                    return response
                content = content.strip().split('+')
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