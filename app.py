# coding: utf-8

from flask import Flask, render_template, request, redirect, session, g
import redis

app = Flask(__name__)
app.secret_key = 'dfjkvKDOc<nnKJCndsc231r3r../dciasd'


@app.before_request
def before_request():
    g.r = redis.StrictRedis()


@app.route('/')
def index():
    message = session.pop('message', '')
    names = g.r.keys('phonebook:*')
    contacts = [(name[10:], g.r.get(name)) for name in names]
    return render_template('index.html', message=message, contacts=contacts)


# @app.route('/')
@app.route('/<name>')
def nindex(name='Anonymous'):
    return render_template('index.html', name=name)


@app.route('/add', methods=['GET', 'POST'])
def add():
    name = phone = ''
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        if name and phone:
            # add to db
            g.r.set('phonebook:' + name, phone)
            session['message'] = 'Contact added'
            return redirect('/')
    return render_template('add.html', name=name, phone=phone)


@app.route('/alter', methods=('POST',))
def alter():
    if 'del' in request.form:
        return redirect('/del?id=' + request.form['id'])
    elif 'upd' in request.form:
        print "upd"
    else:
        print "123"
    return request.form['id']


@app.route('/del', methods={'GET', 'POST'})
def delnum():
    if request.method == 'POST':
        if 'yes' in request.form:
            g.r.delete('phonebook:' + request.form['name'])
            session['message'] = 'Contact deleted'
        return redirect('/')
    return render_template('delete.html', name=request.args["id"])

if __name__ == '__main__':
    app.run(debug=True)


