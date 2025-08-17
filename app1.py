# Файл app1.py

from flask import Flask, request

app = Flask(__name__)

'''@app.route('/')
def sample():
    return 'Был получен GET-запрос!!!'''

@app.route('/html/', methods=['GET'])
def html():
    html_response = '<html><body>Был получен <p>{}</p> запрос.</body></html>'
    return html_response.format(request.method)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port='8000')