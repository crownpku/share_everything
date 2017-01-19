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
    db.update('shareit', where = 'product_id = $pro_id', vars = dict(pro_id = product_id), checkcode_user = checkcode + ' ' + username )
    return checkcode

def wuchu(username, product_id, checkcode):
    #Check checkcode, and if ok, update the product information
    real_checkcode_username = db.select('shareit', what = 'checkcode_user', where = 'product_id = $pro_id', vars = dict(pro_id = product_id))
    real_checkcode_username = str(list(real_checkcode_username)[0])
    original_user = db.select('shareit', what = 'product_user', where = 'product_id = $pro_id', vars = dict(pro_id = product_id))
    original_user = str(list(original_user)[0])
    real_checkcode, wuru_username = str(real_checkcode_username).split(' ', 1)
    
    if real_checkcode != checkcode or original_user != username:
        #Validation fail
        raise
    else:
        db.update('shareit', where = 'product_id = $pro_id', vars = dict(pro_id = product_id), product_user = wuru_username, checkcode_user = 'NA_NA')
        return 1
        
    

def suibiankankan(username):
    #Generate username related products. If none, return 5 random products
    owner_products = db.select('shareit', what = ['product_id', 'product_details'], where = 'product_owner = $usrname', vars = dic(usrname = username))
    user_products = db.select('shareit', what = ['product_id', 'product_details'], where = 'product_user = $usrname', vars = dic(usrname = username))
    strtmp = ''
    if len(owner_products) == 0 and len(user_products) == 0:
        #No user-related info, just randomly select 5 product details to show
        strtmp = '随机展示5个产品：'
        random_products = db.select('shareit', what = 'product_details', limit = 5)
        for product in random_products:
            strtmp = strtmp + product + ';'
        return strtmp.strip(';')
    else:
        strtmp = '你有所有权的产品：'
        for product in owner_products:
            strtmp = strtmp + '[' + product[0] + ']' + product[1] + ';'
        strtmp = strtmp.strip(';')
        strtmp = strtmp + ' || 你有使用权的产品：'
        for product in user_products:
            strtmp = strtmp + '[' + product[0] + ']' + product[1] + ';'
        return strtmp.strip(';')
        
    


