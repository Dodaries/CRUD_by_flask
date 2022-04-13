from multiprocessing import context
from flask import Flask, request, redirect

app = Flask(__name__)

nextId = 1
topics = [
    # {'id':1, 'title':'HTML', 'body':'HTML is ...'},
    # {'id':2, 'title':'CSS', 'body':'CSS is ...'},
    # {'id':3, 'title':'JS', 'body':'JS is ...'}
]

def template(contents, content, id=None):
    contextUI = ''
    if id != None:
        contextUI =f'''
            <li><a href="/update/{id}/">update</a></li>
            <li><form action="/delete/{id}/" method="POST"><input type="submit" value="delete"></form></li>
        '''
    return f'''<!doctype html>
    <html>
        <body>
            <h1><a href="/">WEB</a></h1>
            <ol>
                {contents}
            </ol>
            {content}
            <ul>
                <li><a href="/create">create</a></li>
                {contextUI}
            </ul>
        </body>
    </html>
    '''

def getContents():
    litags = ''
    for topic in topics:
        litags = litags + f'<li><a href="/read/{topic["id"]}/">{topic["title"]}</a></li>'
    return litags

@app.route('/')
def index():
    return template(getContents(), '<h2>Wellcome</h2>Hello, Web')

@app.route('/read/<int:id>/')
def read(id):
    title = ''
    body = ''
    for topic in topics:
        if id == topic['id']:
            title = topic['title']
            body = topic['body']
            break
    return template(getContents(), f'<h2>{title}</h2>{body}', id)

@app.route('/create/', methods=['GET', 'POST'])
def create():
    # print(request.method)
    if request.method == 'GET':
        content = '''
            <form action="/create/" method="POST">
                <p><input type="text" name="title" placeholder="title"></p>
                <p><textarea name="body" placeholder="body"></textarea></p>
                <p><input type="submit" value="create"></p>
            </form>
        '''
        return template(getContents(), content)
    elif request.method == 'POST':
        global nextId
        title = request.form['title']
        body = request.form['body']
        newtopic = {'id': nextId, 'title': title, 'body': body}
        topics.append(newtopic)
        url = '/read/'+str(nextId)+'/'
        nextId = nextId + 1
        return redirect(url)
    

@app.route('/update/<int:id>/', methods=['GET', 'POST'])
def update(id):
    # print(request.method)
    if request.method == 'GET':
        title = ''
        body = ''
        for topic in topics:
            if id == topic['id']:
                title = topic['title']
                body = topic['body']
                break
        content = f'''
            <form action="/update/{id}/" method="POST">
                <p><input type="text" name="title" placeholder="title" value="{title}"></p>
                <p><textarea name="body" placeholder="body">{body}</textarea></p>
                <p><input type="submit" value="update"></p>
            </form>
        '''
        return template(getContents(), content)

    elif request.method == 'POST':
        global nextId
        title = request.form['title']
        body = request.form['body']

        for topic in topics:
            if id == topic['id']:
                topic['title'] = title
                topic['body'] = body
                break
        url = '/read/'+str(id)+'/'

        return redirect(url)
    

@app.route('/delete/<int:id>/', methods=['POST'])
def delete(id):
    for topic in topics:
        if id == topic['id']:
            topics.remove(topic)
            break
    return redirect('/')

app.run(port=5000,debug=True)