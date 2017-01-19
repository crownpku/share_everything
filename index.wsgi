# coding: UTF-8
import sae
#sae.add_vendor_dir('vendor')
from wxtest import app 
#flask
application = sae.create_wsgi_app(app)
