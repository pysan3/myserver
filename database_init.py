import os
from glob import glob
from datetime import datetime

import apps.app as backapp
from apps.database import Base, engine, Session, Users

def create_new_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

def init_db():
    backapp.signup({
        'user_name': 'master',
        'user_password': 'password'
    })
    backapp.create_todoList(1, 'ASAP', '')
    backapp.create_todoList(1, 'ASAP', 'here we go')
    backapp.create_todoList(1, 'not for now', '')
    backapp.create_todoList(1, 'not for now', 'you are doing all right')
    backapp.create_todoList(1, 'not for now', 'keep it going!')

if __name__ == '__main__':
    create_new_database()
    init_db()