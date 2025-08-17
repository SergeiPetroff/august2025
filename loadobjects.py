from sqlalchemy import select, distinct

import db

def loadobjects(tableName, relative, level, startObject, dbi):
  if tableName == 'Factory':
    if relative == 'child':
      if level not in (0, 1):
        return None
      elif level == 0:
        query = select(dbi.sites_table).where(dbi.sites_table.columns.factoryId==startObject['id'])
        select_all_results = dbi.conn.execute(query)
        return select_all_results.fetchall() 
      else:
        query = select(dbi.equipment_table).distinct().select_from(dbi.sites_equipment_table)
        query = query.join(dbi.equipment_table, dbi.sites_equipment_table.columns.equipmentId == dbi.equipment_table.columns.id)
        query = query.join(dbi.sites_table, dbi.sites_equipment_table.columns.siteId == dbi.sites_table.columns.id)
        query = query.where(dbi.sites_table.columns.factoryId==startObject['id'])
        # print(query)
        select_all_results = dbi.conn.execute(query)
        return select_all_results.fetchall() 
    else:
      return None
  elif tableName == 'Site':
    if level != 0:
      return None
    if relative == 'child':
        query = select(dbi.equipment_table).distinct().select_from(dbi.sites_equipment_table)
        query = query.join(dbi.equipment_table, dbi.sites_equipment_table.columns.equipmentId == dbi.equipment_table.columns.id)       
        query = query.join(dbi.sites_table, dbi.sites_equipment_table.columns.siteId == dbi.sites_table.columns.id)
        query = query.where(dbi.sites_table.columns.id==startObject['id'])
        # print(query)
        select_all_results = dbi.conn.execute(query)
        return select_all_results.fetchall() 
    elif relative == 'parent':
        query = select(dbi.factories_table).where(dbi.factories_table.columns.id==startObject['factoryId'])
        select_all_results = dbi.conn.execute(query)
        return select_all_results.fetchall()     
    else:
      return None
  elif tableName == 'Equipment':
    if relative == 'parent':
      if level not in (0, 1):
        return None
      elif level == 0:
        query = select(dbi.sites_table).distinct().select_from(dbi.sites_equipment_table)
        query = query.join(dbi.equipment_table, dbi.sites_equipment_table.columns.equipmentId == dbi.equipment_table.columns.id)       
        query = query.join(dbi.sites_table, dbi.sites_equipment_table.columns.siteId == dbi.sites_table.columns.id)
        query = query.where(dbi.equipment_table.columns.id==startObject['id'])
        # print(query)
        select_all_results = dbi.conn.execute(query)
        return select_all_results.fetchall() 
      else:
        query = select(dbi.factories_table).distinct().select_from(dbi.sites_equipment_table)
        query = query.join(dbi.factories_table, dbi.factories_table.columns.id == dbi.sites_table.columns.factoryId)
        query = query.join(dbi.sites_table, dbi.sites_equipment_table.columns.siteId == dbi.sites_table.columns.id)
        query = query.join(dbi.equipment_table, dbi.sites_equipment_table.columns.equipmentId == dbi.equipment_table.columns.id)
        query = query.where(dbi.equipment_table.columns.id==startObject['id'])
        # print(query)
        select_all_results = dbi.conn.execute(query)
        return select_all_results.fetchall() 
    else:
      return None
  else:
    return None

def test_LoadObjects():
  dbi = db.Db('sqlite:///work.db')  
  res = loadobjects('Factory', 'child', 1, {'id':1, 'name': 'factory1'}, dbi)
  res1 = loadobjects('Equipment', 'parent', 0, {'id':1, 'name': 'equipment1'}, dbi)
  res2 = loadobjects('Equipment', 'parent', 0, {'id':2, 'name': 'equipment2'}, dbi)
  res3 = loadobjects('Equipment', 'parent', 1, {'id':2, 'name': 'equipment2'}, dbi)
  res4 = loadobjects('Site', 'parent', 0, {'id':1, 'factoryId': 1, 'name': 'site1'}, dbi)
  res5 = loadobjects('Site', 'child', 0, {'id':2, 'factoryId': 1, 'name': 'site2'}, dbi)
  return res, res1, res2, res3, res4, res5

print(test_LoadObjects())
