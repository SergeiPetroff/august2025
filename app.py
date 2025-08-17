# Файл app.py

from flask import Flask, request

app = Flask(__name__)

'''@app.route('/')
def sample():
    return 'Был получен GET-запрос!!!'''

@app.route('/', methods=['GET'])
def sample():
    return 'Был получен GET-запрос.'

@app.route('/say/<phrase>', methods=['GET'])
def say(phrase):
    return f'Была получена фраза {phrase}'

@app.route('/sum/<int:number>', methods=['GET'])
def sum_numbers(number):
    return f'Результат сложения 5 и {number} = {5+number}'

# from flask import request

@app.route('/calc/', methods=['GET', 'POST'])
def calc():
    if request.method == 'POST':
        a = int(request.form['a'])
        b = int(request.form['b'])
        result = a + b
        return f'{a} + {b} = {result}'
    return f'Был получен {request.method} запрос.'

if __name__ == '__main__':
    app.run(host='127.0.0.1', port='8000')