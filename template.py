# Файл app2.py

from flask import Flask, request, render_template

app = Flask(__name__)

'''@app.route('/')
def sample():
    return 'Был получен GET-запрос!!!'''

# from flask import render_template

data = (
    dict(name='Python', released='20.01.1991'),
    dict(name='Java', released='23.06.1995'),
    dict(name='GO', released='10.11.2009'),
)

@app.route('/template/', methods=['GET'])
def template():
    return render_template('table.html', items=data)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port='8000')