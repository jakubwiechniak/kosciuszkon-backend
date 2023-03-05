import os
import urllib
from sqlalchemy import create_engine, create_mock_engine
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # ...
    # ssl_args = {'ssl_ca': 'DigiCertGlobalRootCA.crt.pem'}
    # engine = create_engine("mysql+pymysql://kantyna:Admin123@kosciuszkon.mysql.database.azure.com:3306/kosciuszkon",
    #                     connect_args=ssl_args)
    # print(engine.url)
    # SQLALCHEMY_DATABASE_URI = engine.url
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://kantyna:Admin123@kosciuszkon.mysql.database.azure.com:3306/kosciuszkon'
    SQLALCHEMY_TRACK_MODIFICATIONS = False