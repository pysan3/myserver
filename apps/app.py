import numpy as np
import os
import shutil
from glob import glob
import subprocess
import hashlib
import secrets
from datetime import datetime
import requests
from bs4 import BeautifulSoup

from apps.database import *
from sqlalchemy.sql import exists

def init_server():
    subprocess.run('python database_init.py'.split())
    for d in os.listdir('user_files'):
        if os.path.isdir(f'user_files/{d}') and d != '1':
            os.system(f'rm -rf user_files/{d}')

def login(data):
    session = Session()
    user = session.query(Users).filter_by(user_name=data['user_name']).all()
    session.close()
    user_id = -1
    password = hashlib.sha256(data['user_password'].encode()).hexdigest()
    if len(user) == 1:
        if user[0].user_password == password:
            msg = 'success'
            user_id = user[0].id
        else:
            msg = 'wrong password'
    else:
        msg = 'wrong username'
    return {'isFound': len(user), 'token': new_token(user_id), 'msg': msg}

def signup(data):
    name = data['user_name']
    user_id = -1
    session = Session()
    user = session.query(Users).filter_by(user_name=name).all()
    if len(user) == 0:
        user_id = session.query(Users).count() + 1
        session.add(Users(
            user_name=name,
            user_password=hashlib.sha256(data['user_password'].encode()).hexdigest(),
            created_at=datetime.now().isoformat(' ', 'seconds')
        ))
        session.commit()
        msg = 'succeeded to create an user account'
    else:
        msg = 'already exists'
    session.close()
    return {'isFound': (user_id >= 0) + 0, 'token': new_token(user_id), 'msg': msg}

def check_login(token):
    if token == 'none':
        return False
    session = Session()
    check = session.query(exists().where(TokenTable.token==token))
    session.close()
    return check

def new_token(user_id):
    session = Session()
    token = secrets.token_hex()
    session.add(TokenTable(
        token=token,
        user_id=user_id
    ))
    session.commit()
    session.close()
    return token

def verify_user(token):
    session = Session()
    user_id = session.query(TokenTable).filter_by(token=token).one_or_none()
    session.close()
    if user_id is None:
        return False
    else:
        return int(user_id.user_id)

def load_file(user_id, project):
    path = f'user_files/{user_id}/{project}'
    if not os.path.exists(path):
        os.mkdir(path)
    def file_recursive(path):
        files = []
        for f in os.listdir(path):
            f_path = f'{path}/{f}'
            f_data = {'id': f_path, 'name': f, 'type': 'file', 'show': '1', 'insides': []}
            if os.path.isdir(f_path):
                f_data['type'] = 'dir'
                f_data['insides'].extend(file_recursive(f_path))
            files.append(f_data)
        return files
    return {'comment': file_recursive(path)}

def load_project(user_id):
    path = f'user_files/{user_id}'
    if not os.path.exists(path):
        os.mkdir(path)
    dirs = []
    for d in os.listdir(path):
        d_path = f'{path}/{d}'
        if os.path.isdir(d_path):
            dirs.append({'name': d})
    return {'projects': dirs}

def username(user_id):
    session = Session()
    name = session.query(Users).filter_by(id=user_id).first()
    session.close()
    return name.user_name

def run_command(user_id, project, command, cat):
    in_file = subprocess.PIPE
    out_file = subprocess.PIPE
    project_path = f'user_files/{user_id}/{project}/'
    command_length = len(command)
    for i, c in enumerate(reversed(command), 1):
        index = command_length - i
        if c == '>':
            out_file = open(project_path + command[index + 1], 'w')
            command = command[:index]
        elif c == '>>':
            out_file = open(project_path + command[index + 1], 'a')
            command = command[:index]
        elif c == '<':
            in_file = open(project_path + command[index + 1], 'r')
            command = command[:index]
        elif c == '|':
            in_file = run_command(user_id, project, command[:index], True).stdout
            command = command[index + 1:]
            break
    return subprocess.run(command, cwd=project_path, stdin=in_file, stdout=out_file, stderr=out_file)

def create_project(user_id, name):
    os.mkdir(f'user_files/{user_id}/{name}')

def delete_project(user_id, name):
    shutil.rmtree(f'user_files/{user_id}/{name}')

def github_user(user_id):
    # TODO: here
    return 'pysan3'

def github_kusa(name):
    def color(count):
        colors = ['#ebedf0', '#c6e48b', '#c6e48b', '#c6e48b', '#7bc96f']
        if count <= 4:
            return colors[count]
        else:
            c = Color(colors[4])
            c.darken(count-4)
            return c.return_colorcode()
    return [{
        'date': day['data-date'],
        'day': (datetime.strptime(day['data-date'], '%Y-%m-%d').weekday() + 1) % 7,
        'count': day['data-count'],
        'color': color(int(day['data-count']))
    } for day in BeautifulSoup(
        requests.Session().get(f'https://github.com/users/{name}/contributions').text,
        'html.parser'
    ).find_all('rect', attrs={'class': 'day'})]

class Color:
    def __init__(self, c):
        if isinstance(c, tuple):
            self.color = c
        else:
            self.color = (int(c[1:3],16),int(c[3:5],16),int(c[5:7],16))
    def return_rgb(self):
        return self.color
    def return_colorcode(self):
        return f'#{self.color[0]:02X}{self.color[1]:02X}{self.color[2]:02X}'
    def darken(self, stage):
        for _ in range(int(stage)):
            self.color = tuple(int(c * 0.9) for c in self.color)

def load_todoList(user_id):
    todolist = {}
    session = Session()
    for data in session.query(ToDoList).filter_by(user_id=user_id).all():
        todolist.setdefault(data.list_name, [])
        if len(data.name):
            todolist[data.list_name].append({'name': data.name, 'isDone': data.isDone})
    session.close()
    return todolist

def create_todoList(user_id, list_name, name):
    session = Session()
    session.add(ToDoList(
        user_id=user_id,
        list_name=list_name,
        name=name,
        isDone=False
    ))
    session.commit()
    session.close()