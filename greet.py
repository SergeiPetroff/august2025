from flask import Flask, request

app = Flask(__name__)

@app.route('/search')
def search():
    # Получаем значение параметра 'query'
    search_query = request.args.get('query')

    # Получаем значение параметра 'page'
    page_num = request.args.get('page')

    # Используем .get() для безопасного доступа, если параметр может отсутствовать
    # Например, можно использовать пустую строку по умолчанию:
    # username = request.args.get('username', '')

    if search_query:
        return f"Поисковый запрос: {search_query}, страница: {page_num}"
    else:
        return "Пожалуйста, введите поисковый запрос."

if __name__ == '__main__':
    app.run(host='127.0.0.1', port='8000')