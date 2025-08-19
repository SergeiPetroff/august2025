# mytask.py

from flask import Flask, request, render_template, redirect, flash

import sqlalchemy as sql
from sqlalchemy import create_engine, MetaData, Table, select

from sqlalchemy.exc import SQLAlchemyError, IntegrityError, NoResultFound

import db

dbi = None

app = Flask(__name__)
app.secret_key = 'your_secret_key' # Required for flashing

@app.route('/factories/', methods=['GET', 'POST'])
def factories():
    data = []
    with dbi.engine.connect() as connection:
        result = connection.execute(select(dbi.factories_table))
        for row in result:
          data.append(dict(id = row[0], name = row[1]))
    return render_template('factories.html', items=data)

@app.route('/factories/create/', methods=['POST'])
def factories_create():
    if request.method == 'POST':
        # Retrieve data for each row/column based on the 'name' attributes
        factory_name = request.form.get('factory_name')
        with dbi.engine.connect() as connection:
            insertion_query = dbi.factories_table.insert().values({'name': factory_name})
            connection.execute(insertion_query)
            connection.commit()
    return redirect('/factories')

@app.route('/factories/delete/', methods=['POST'])
def factories_delete():
    if request.method == 'POST':
        # Retrieve data for each row/column based on the 'name' attributes
        factory_name = request.form.get('factory_name')
        with dbi.engine.connect() as connection:
            # delete_query = sql.delete(dbi.factories_table).where(dbi.factories_table.columns.id==factory_id)
            delete_query = sql.delete(dbi.factories_table).where(dbi.factories_table.columns.name==factory_name)
            print(delete_query)
            try:
                connection.execute(delete_query)
                connection.commit()
            except IntegrityError as e:
                flash('Ошибка удаления фабрики: удалите сначала её цеха.', 'info')
    return redirect('/factories')


@app.route('/sites/', methods=['GET', 'POST'])
def sites():
    data = []
    with dbi.engine.connect() as connection:
        result = connection.execute(select(dbi.sites_table))
        for row in result:
          data.append(dict(id = row[0], siteId = row[1], name = row[2]))
    return render_template('sites.html', items=data)

@app.route('/sites/create/', methods=['POST'])
def sites_create():
    if request.method == 'POST':
        # Retrieve data for each row/column based on the 'name' attributes
        site_name = request.form.get('site_name')
        factory_name = request.form.get('factory_name')
        with dbi.engine.connect() as connection:
            result = connection.execute(select(dbi.factories_table).where(dbi.factories_table.columns.name==factory_name))
            factory_id = result.__next__()[0]
            insertion_query = dbi.sites_table.insert().values({'name': site_name, 'factoryId': factory_id})
            connection.execute(insertion_query)
            connection.commit()
    return redirect('/sites')

@app.route('/sites/delete/', methods=['POST'])
def sites_delete():
    if request.method == 'POST':
        # Retrieve data for each row/column based on the 'name' attributes
        site_name = request.form.get('site_name')
        factory_name = request.form.get('factory_name')
        with dbi.engine.connect() as connection:
            result = connection.execute(select(dbi.factories_table).where(dbi.factories_table.columns.name==factory_name))
            factory_id = result.__next__()[0]
            delete_query = sql.delete(dbi.sites_table).where(dbi.sites_table.columns.name==site_name, dbi.sites_table.columns.factoryId==factory_id)
            print(delete_query)
            try:
                connection.execute(delete_query)
                connection.commit()
            except IntegrityError as e:
                flash('Ошибка удаления участка: удалите сначала его оборудование.', 'info')
        return redirect('/sites')

@app.route('/equipment/', methods=['GET', 'POST'])
def equipment():
    data = []
    with dbi.engine.connect() as connection:
        result = connection.execute(select(dbi.equipment_table))
        for row in result:
          data.append(dict(id = row[0], name = row[1]))
    return render_template('equipment.html', items=data)

@app.route('/equipment/create/', methods=['POST'])
def equipment_create():
    if request.method == 'POST':
        # Retrieve data for each row/column based on the 'name' attributes
        equipment_name = request.form.get('equipment_name')
        with dbi.engine.connect() as connection:
            insertion_query = dbi.equipment_table.insert().values({'name': equipment_name})
            connection.execute(insertion_query)
            connection.commit()
    return redirect('/equipment')

@app.route('/equipment/delete/', methods=['POST'])
def equipment_delete():
    if request.method == 'POST':
        # Retrieve data for each row/column based on the 'name' attributes
        equipment_name = request.form.get('equipment_name')
        with dbi.engine.connect() as connection:
            # delete_query = sql.delete(dbi.factories_table).where(dbi.factories_table.columns.id==factory_id)
            delete_query = sql.delete(dbi.equipment_table).where(dbi.equipment_table.columns.name==equipment_name)
            print(delete_query)
            try:
                connection.execute(delete_query)
                connection.commit()
            except IntegrityError as e:
                flash('Ошибка удаления оборудования: удалите сначала его размещение в цехе.', 'info')
    return redirect('/equipment')

@app.route('/placements/', methods=['GET', 'POST'])
def placements():
    data = []
    '''with dbi.engine.connect() as connection:
        result = connection.execute(select(dbi.factories_table))
        for row in result:
          data.append(dict(id = row[0], name = row[1]))'''
    return render_template('placements.html', items=data)

@app.route('/placements/create/', methods=['POST'])
def placement_create():
    if request.method == 'POST':
        # Retrieve data for each row/column based on the 'name' attributes
        factory_name = request.form.get('factory_name')
        site_name = request.form.get('site_name')
        equipment_name = request.form.get('equipment_name')
        with dbi.engine.connect() as connection:
            result1 = connection.execute(select(dbi.factories_table).where(dbi.factories_table.columns.name==factory_name))
            factory_id = result1.__next__()[0]
            result2 = connection.execute(select(dbi.sites_table).where(dbi.sites_table.columns.name==site_name, dbi.sites_table.columns.factoryId==factory_id))
            site_id = result2.__next__()[0]
            result3 = connection.execute(select(dbi.equipment_table).where(dbi.equipment_table.columns.name==equipment_name))
            equipment_id = result3.__next__()[0]
            print(factory_id, site_id, equipment_id)

            insertion_query = dbi.sites_equipment_table.insert().values({'siteId': site_id, 'equipmentId': equipment_id})

            connection.execute(insertion_query)
            connection.commit()
    return redirect('/placements')

@app.route('/placements/delete/', methods=['POST'])
def placement_delete():
    if request.method == 'POST':
        # Retrieve data for each row/column based on the 'name' attributes
        factory_name = request.form.get('factory_name')
        site_name = request.form.get('site_name')
        equipment_name = request.form.get('equipment_name')
        with dbi.engine.connect() as connection:
            result1 = connection.execute(select(dbi.factories_table).where(dbi.factories_table.columns.name==factory_name))
            factory_id = result1.__next__()[0]
            result2 = connection.execute(select(dbi.sites_table).where(dbi.sites_table.columns.name==site_name, dbi.sites_table.columns.factoryId==factory_id))
            site_id = result2.__next__()[0]
            result3 = connection.execute(select(dbi.equipment_table).where(dbi.equipment_table.columns.name==equipment_name))
            equipment_id = result3.__next__()[0]
            print(factory_id, site_id, equipment_id)
            delete_query = sql.delete(dbi.sites_equipment_table).where(dbi.sites_equipment_table.columns.siteId==site_id, dbi.sites_equipment_table.columns.equipmentId==equipment_id)
            print(delete_query)
            try:
                connection.execute(delete_query)
                connection.commit()
            except IntegrityError as e:
                flash('Ошибка удаления размещения: такого нет', 'info')
    return redirect('/placements')


if __name__ == '__main__':
    dbi = db.Db('sqlite:///work.db')

    '''select_all_query = sql.select([factories_table])
    select_all_results = conn.execute(select_all_query)
    print(select_all_results.fetchall())'''

    app.run(host='127.0.0.1', port='8000')