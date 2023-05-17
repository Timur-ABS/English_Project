# db_instance.py

from .db import Database
from .config import db_config

db_connection = Database(host=db_config['host'],
                         port=db_config['port'],
                         user=db_config['user'],
                         password=db_config['password'],
                         db=db_config['db']
                         )
