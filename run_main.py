import responder
import random
import urllib

import apps.app as backapp

api = responder.API(static_dir='./static', templates_dir='./static')
api.add_route('/', static=True, websocket=True)
# backapp.init_server()

@api.route('/api/login')
async def login(req, resp):
    resp.media = backapp.login(await req.media())

@api.route('/api/signup')
async def signup(req, resp):
    resp.media = backapp.signup(await req.media())

@api.route('/api/loggedin')
async def logged_in(req, resp):
    resp.text = 'valid' if backapp.check_login((await req.media())['token']) else 'invalid'

@api.route('/api/loadfile/{project}')
async def load_file(req, resp, *, project):
    user_id = backapp.verify_user((await req.media())['token'])
    if user_id:
        resp.media = dict({'valid': '1', 'user_name': backapp.username(user_id)}, **backapp.load_file(user_id, project))
    else:
        resp.media = {'valid': '0'}

@api.route('/api/userfile/{file_url}')
async def user_file(req, resp, *, file_url):
    user_id = backapp.verify_user((await req.media())['token'])
    if user_id:
        with open(urllib.parse.unquote(file_url), 'r') as f:
            resp.text = f.read()
    else:
        resp.text = ''

@api.route('/api/fileupload/{file_url}')
async def fileupload(req, resp, *, file_url):
    data = await req.media()
    user_id = backapp.verify_user(data['token'])
    if user_id:
        with open(urllib.parse.unquote(file_url), 'w') as f:
            f.write(data['data'])

@api.route('/ws/terminal', websocket=True)
async def ws_terminal(ws):
    await ws.accept()
    data = await ws.receive_json()
    project = data['project']
    user_id = backapp.verify_user(data['token'])
    try:
        while user_id is not False:
            data = await ws.receive_json()
            if user_id != backapp.verify_user(data['token']):
                break
            if len(data['command'].split()) > 0:
                res = backapp.run_command(user_id, project, data['command'].split(), False).stdout
                if res is None:
                    res = ''.encode('utf-8')
                await ws.send_json({'result': res.decode('utf-8')})
    except:
        pass
    await ws.close()

@api.route('/api/loadproject')
async def load_project(req, resp):
    user_id = backapp.verify_user((await req.media())['token'])
    if user_id:
        resp.media = dict({'valid': '1', 'user_name': backapp.username(user_id)}, **backapp.load_project(user_id))
    else:
        resp.media = {'valid': '0'}

@api.route('/api/manageproject/{command}/{name}')
async def manage_project(req, resp, *, command, name):
    user_id = backapp.verify_user((await req.media())['token'])
    name = urllib.parse.unquote(name)
    if user_id:
        if command == 'create':
            backapp.create_project(user_id, name)
        elif command == 'delete':
            backapp.delete_project(user_id, name)

@api.route('/api/kusa')
async def github_kusa(req, resp):
    github_name = backapp.github_user(backapp.verify_user((await req.media())['token']))
    resp.media = {
        'github_name': github_name,
        'garden': backapp.github_kusa(github_name)
    }

@api.route('/api/todolist/{mode}')
async def todoList_handler(req, resp, *, mode):
    data = await req.media()
    user_id = backapp.verify_user(data['token'])
    if mode == 'load':
        resp.media = backapp.load_todoList(user_id)
    elif mode == 'createlist':
        backapp.create_todoList(user_id, data['list_name'], '')
    elif mode == 'createelement':
        backapp.create_todoList(user_id, data['list_name'], data['name'])
    elif mode == 'deletelist':
        backapp.deletelist_todoList(user_id, data['list_name'])
    elif mode == 'doneelement':
        backapp.deleteelement_todoList(user_id, data['list_name'], data['name'], 'done')
    elif mode == 'deleteelement':
        backapp.deleteelement_todoList(user_id, data['list_name'], data['name'], 'delete')

@api.route('/api/random')
def random_number(req, resp):
    resp.media = {'randomNumber': random.randint(1, 100)}

if __name__ == '__main__':
    api.run()