# -*- encoding: utf-8 -*-  
  
import urllib  
import urllib2  
from urllib import urlencode  
import json  
import sys  
reload(sys)  
sys.setdefaultencoding('UTF-8')  
  
appid = 'xxxx'  
secret = '000000'  
gettoken = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=' + appid + '&secret=' + secret  
f = urllib2.urlopen( gettoken )  
stringjson = f.read()   
access_token = json.loads(stringjson)['access_token']  
  
#print access_token  
  
posturl = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=" + access_token  


#未认证的订阅号并不能实现下面的功能，而个人订阅号又不能被认证。。。 
menu = '''''{ 
     "button":[ 
 
      { 
           "name":"万物共享", 
           "sub_button": 
           [{ 
               "type":"click", 
               "name":"物入", 
               "key":"wuru" 
            }, 
            { 
               "type":"click", 
               "name":"物出", 
               "key":"wuchu" 
            }, 
            { 
               "type":"click", 
               "name":"随便看看", 
               "key":"sbkk" 
            }, 
            { 
               "type":"click", 
               "name":"这是什么?", 
               "key":"zssm" 
            }
            ] 
       }] 
 }'''  
  
request = urllib2.urlopen(posturl, menu.encode('utf-8') )  
print request.read()  

