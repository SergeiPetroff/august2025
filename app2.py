# Файл app2.py

from flask import Flask, request

app = Flask(__name__)

'''@app.route('/')
def sample():
    return 'Был получен GET-запрос!!!'''

data = (
    dict(name='Python', released='20.01.1991'),
    dict(name='Java', released='23.06.1995'),
    dict(name='GO', released='10.11.2009'),
)

@app.route('/table/', methods=['GET'])
def table():
    start = '<html><body><table border=3>'
    caption = '<caption>Языки программирования</caption>'
    header = '<tr><th>Название</th><th>Первый релиз</th></tr>'
    end = '</table></body></html>'
    tr_list = list()
    for item in data:
        tr_list.append(
            f'<tr><td>{item["name"]}</td><td>{item["released"]}</td></tr>'
        )
    content = ''.join(tr_list)
    html_response = ''.join((start, caption, header, content, end))
    return html_response.format(request.method)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port='8000')