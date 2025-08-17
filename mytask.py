# mytask.py

from flask import Flask, request, render_template

import sqlalchemy as sql
from sqlalchemy import create_engine, MetaData, Table, select

import db

dbi = None

app = Flask(__name__)

data = (
    dict(name='factory1'),
    dict(name='factory2'),
    dict(name='factory3'),
)

@app.route('/task/', methods=['GET'])
def template():
    return render_template('mytable.html', items=data)

@app.route('/resp/', methods=['GET'])
def template_resp():
    return render_template('resp.html')

@app.route('/get/', methods=['GET'])
def template_get():
    make = request.args.get('make')
    model = request.args.get('model')
    if make and model:
        return render_template('getout.html', make=make, model=model)
    return render_template('get.html')

@app.route('/factories/', methods=['GET'])
def factories():
    data = []
    with dbi.engine.connect() as connection:
        result = connection.execute(select(dbi.factories_table))
        for row in result:
          data.append({'name': row[1]})
    return render_template('factories.html', items=data)

if __name__ == '__main__':
    dbi = db.Db('sqlite:///work.db')

    l = []
    with dbi.engine.connect() as connection:
        result = connection.execute(select(dbi.factories_table))
        for row in result:
            print(row)
            print(row[0], row[1])
            l.append({'name': row[1]})
        
 

    '''select_all_query = sql.select([factories_table])
    select_all_results = conn.execute(select_all_query)
    print(select_all_results.fetchall())'''

    app.run(host='127.0.0.1', port='8000')