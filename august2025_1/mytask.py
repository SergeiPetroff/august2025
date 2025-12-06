# mytask.py

from flask import Flask, request, render_template, redirect, flash

import sqlalchemy as sql
from sqlalchemy import create_engine, MetaData, Table, select

from sqlalchemy.exc import SQLAlchemyError, IntegrityError, NoResultFound

import db

from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from typing import List

from sqlalchemy import Column
from sqlalchemy import Table


# declarative base class
class Base(DeclarativeBase):
    pass

sites_equipment_table = Table(
    "sites_equipment",
    Base.metadata,
    Column("siteId", ForeignKey("sites.id"), primary_key=True),
    Column("equipmentId", ForeignKey("equipment.id"), primary_key=True),
)

class Factory(Base):
    __tablename__ = "factories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    sites: Mapped[List["Site"]] = relationship(back_populates="factory")

class Site(Base):
    __tablename__ = "sites"

    id: Mapped[int] = mapped_column(primary_key=True) 
    name: Mapped[str]
    factoryId: Mapped[int] = mapped_column(ForeignKey("factories.id"))
    factory: Mapped["Factory"] = relationship(back_populates="sites")
    equipment: Mapped[List["Equipment"]] = relationship(
        secondary=sites_equipment_table, back_populates="sites"        
    )

class Equipment(Base):
    __tablename__ = "equipment"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    sites: Mapped[List["Site"]] = relationship(
        secondary=sites_equipment_table, back_populates="equipment" 
    )

dbi = None

app = Flask(__name__)
app.secret_key = 'your_secret_key' # Required for flashing

@app.route('/factories/', methods=['GET'])
def factories():
    data = []
    with Session(dbi.engine) as session:
        data = session.query(Factory).all()
        return render_template('factories.html', items=data)

@app.route('/factories/show', methods=['GET'])
def factories_show():
    id = request.args.get('id')
    factory = None
    with Session(dbi.engine) as session:
        factory = session.get(Factory, id)
        if not factory:
            return redirect('/factories')
        return render_template('factory_show.html', factory=factory)

@app.route('/factories/create/', methods=['POST'])
def factories_create():
    if request.method == 'POST':
        # Retrieve data for each row/column based on the 'name' attributes
        factory_name = request.form.get('factory_name')
        factory = Factory(name=factory_name)
        with Session(dbi.engine) as session:
            session.add(factory)
            session.commit()
    return redirect('/factories')

@app.route('/factories/delete/', methods=['POST'])
def factories_delete():
    if request.method == 'POST':
        # Retrieve data for each row/column based on the 'name' attributes
        factory_name = request.form.get('factory_name')
        with Session(dbi.engine) as session:
            factories = session.query(Factory).where(Factory.name==factory_name).all()
            try:
                for factory in factories:
                    session.delete(factory)
                session.commit()
            except IntegrityError as e:
                flash('Ошибка удаления фабрики: удалите сначала её цеха.', 'info')
    return redirect('/factories')

@app.route('/factories/deleteById/', methods=['POST'])
def factories_delete_by_id():
    if request.method == 'POST':
        # Retrieve data for each row/column based on the 'name' attributes
        factory_id = request.form.get('factory_id')
        with Session(dbi.engine) as session:
            factory = session.get(Factory, factory_id)
            if not factory:
                flash(("Фабрики не существует!"))
            else:
                try:
                    session.delete(factory)
                    session.commit()
                except IntegrityError as e:
                    flash('Ошибка удаления фабрики: удалите сначала её цеха.', 'info')
    return redirect('/factories')

@app.route('/sites/', methods=['GET'])
def sites():
    data = []
    with Session(dbi.engine) as session:
        data = session.query(Site).all()
        return render_template('sites.html', sites=data)
    
@app.route('/sites/show', methods=['GET'])
def sites_show():
    id = request.args.get('id')
    site = None
    with Session(dbi.engine) as session:
        site = session.get(Site, id)
        data = session.query(Equipment).all()
        if not site:
            return redirect('/sites')
        return render_template('site_show.html', site=site, equipment_all=data)

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

@app.route('/sites/createN/', methods=['POST'])
def sites_createN():
    if request.method == 'POST':
        # Retrieve data for each row/column based on the 'name' attributes
        site_name = request.form.get('site_name')
        factory_id = request.form.get('factory_id')
        with dbi.engine.connect() as connection:
            result = connection.execute(select(dbi.factories_table).where(dbi.factories_table.columns.id==factory_id))
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
    
@app.route('/sites/deleteById/', methods=['POST'])
def sites_delete_by_id():
    if request.method == 'POST':
        # Retrieve data for each row/column based on the 'name' attributes
        site_id = request.form.get('site_id')
        with Session(dbi.engine) as session:
            site = session.get(Site, site_id)
            if not site:
                flash(("Участок не существует!"))
            else:
                try:
                    session.delete(site)
                    session.commit()
                except IntegrityError as e:
                    flash('Ошибка удаления цеха: удалите сначала его оборудование.', 'info')
    return redirect('/sites')

@app.route('/equipment/', methods=['GET'])
def equipment():
    data = []
    with Session(dbi.engine) as session:
        data = session.query(Equipment).all()
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

@app.route('/equipment/deleteById/', methods=['POST'])
def equipment_delete_by_id():
    if request.method == 'POST':
        # Retrieve data for each row/column based on the 'name' attributes
        equipment_id = request.form.get('equipment_id')
        with Session(dbi.engine) as session:
            equipment = session.get(Equipment, equipment_id)
            if not equipment:
                flash(("Оборудование не существует!"))
            else:
                try:
                    session.delete(equipment)
                    session.commit()
                except IntegrityError as e:
                    flash('Ошибка удаления оборудования: удалите сначала его размещение в цехе.', 'info')
    return redirect('/equipment')

@app.route('/placements/create/', methods=['POST'])
def placement_create():
    if request.method == 'POST':
        # Retrieve data for each row/column based on the 'name' attributes
        site_id = request.form.get('site_id')
        equipment_id = request.form.get('equipment_id')
        with Session(dbi.engine) as session:
            site = session.get(Site, site_id)
            equipment = session.get(Equipment, equipment_id)
            site.equipment.append(equipment)
            session.commit()
    return redirect('/sites')

@app.route('/placements/create_batch/', methods=['POST'])
def placement_create_batch():
    if request.method == 'POST':
        # Retrieve data for each row/column based on the 'name' attributes
        site_id = request.form.get('site_id')
        equipment_ids = request.form.getlist('equipment_id')
        with Session(dbi.engine) as session:
            site = session.get(Site, site_id)
            for equipment_id in equipment_ids:
                equipment = session.get(Equipment, equipment_id)
                if not (equipment in site.equipment):
                    site.equipment.append(equipment)
            session.commit()
    return redirect('/sites/show?id='+site_id)

@app.route('/placements/delete/', methods=['POST'])
def placement_delete():
    if request.method == 'POST':
        # Retrieve data for each row/column based on the 'name' attributes
        site_id = request.form.get('site_id')
        equipment_id = request.form.get('equipment_id')
        with Session(dbi.engine) as session:
            site = session.get(Site, site_id)
            equipment = session.get(Equipment, equipment_id)
            site.equipment.remove(equipment)
            session.add(site)
            session.commit()
    return redirect('/sites')

@app.route('/equipment/show', methods=['GET'])
def equipment_show():
    id = request.args.get('id')
    equipment = None
    with Session(dbi.engine) as session:
        equipment = session.get(Equipment, id)
        if not equipment:
            return redirect('/equipment')
        return render_template('equipment_show.html', equipment=equipment)
    
@app.route('/sites/add_equipment', methods=['GET'])
def add_equipment():
    id = request.args.get('id')
    site = None
    with Session(dbi.engine) as session:
        site = session.get(Site, id)
        data = session.query(Equipment).all()
        if not site:
            return redirect('/sites')
        return render_template('add_equipment.html', site=site, equipment_all=data)

if __name__ == '__main__':
    dbi = db.Db('sqlite:///work.db')

    '''select_all_query = sql.select([factories_table])
    select_all_results = conn.execute(select_all_query)
    print(select_all_results.fetchall())'''

    app.run(host='127.0.0.1', port='8000')