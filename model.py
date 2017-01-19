# coding: UTF-8
import web
import web.db
import sae.const
from random import randint

db = web.database(
    dbn='mysql',
    host=sae.const.MYSQL_HOST,
    port=int(sae.const.MYSQL_PORT),
    user=sae.const.MYSQL_USER,
    passwd=sae.const.MYSQL_PASS,
    db=sae.const.MYSQL_DB
)
 
def gen_checkcode():
    return str(randint(100, 999))
    
    
def wuru(username, product_details):
    #New Product
    #Return product id
    product_id = db.insert('shareit', product_details = product_details, product_owner = username, product_user = username, checkcode_user = 'NA_NA')
    return str(product_id)

def wuruid(username, product_id):
    #Old Product
    #Return checkcode for wuchu guy to confirm
    checkcode = gen_checkcode()
    db.update('shareit', where = 'product_id = $pro_id', vars = dict(pro_id = product_id), checkcode_user = checkcode + '_' + username )
    return checkcode

def wuchu(username, product_id, checkcode):
    #Check checkcode, and if ok, update the product information
    results = db.select('shareit', what = 'product_user, checkcode_user, product_details', where = 'product_id = $pro_id', vars = dict(pro_id = product_id)).list()[0]
    real_checkcode_username = results.checkcode_user
    original_user = results.product_user
   
    #raise NameError(real_checkcode_username)
    real_checkcode, wuru_username = str(real_checkcode_username).split('_', 1)
    
    if real_checkcode != checkcode or original_user != username:
        #Validation fail
        raise NameError(real_checkcode)
    else:
        db.update('shareit', where = 'product_id = $pro_id', vars = dict(pro_id = product_id), product_user = wuru_username, checkcode_user = 'NA_NA')
        return results.product_details
        
    

def suibiankankan(username):
    #Generate username related products. If none, return 5 random products
    owner_products = db.select('shareit', what = 'product_id, product_details', where = 'product_owner = $usrname', vars = dict(usrname = username)).list()
    user_products = db.select('shareit', what = 'product_id, product_details', where = 'product_user = $usrname', vars = dict(usrname = username)).list()
    strtmp = ''
    if len(owner_products) == 0 and len(user_products) == 0:
        #No user-related info, just randomly select 5 product details to show
        strtmp = u'随机展示5个产品：'
        random_products = db.select('shareit', what = 'product_details', limit = 5).list()
        for product in random_products:
            strtmp = strtmp + product.product_details + u';'
        return strtmp.strip(';')
    else:
        strtmp = u'你有所有权的产品:'
        for product in owner_products:
            strtmp = strtmp + u' [' + str(product.product_id) + u']' + product.product_details + u';'
        strtmp = strtmp.strip(';')
        strtmp = strtmp + u' \n你有使用权的产品:'
        for product in user_products:
            strtmp = strtmp + u' [' + str(product.product_id) + u']' + product.product_details + u';'
        return strtmp.strip(';')
        
    

