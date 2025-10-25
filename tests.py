import loadobjects

import db

def test_ok():
  assert True == True

def test_LoadObjects():
  dbi = db.Db('sqlite:///work.db')  
  res = loadobjects.loadobjects('Factory', 'child', 1, {'id':1, 'name': 'factory1'}, dbi)
  res1 = loadobjects.loadobjects('Equipment', 'parent', 0, {'id':1, 'name': 'equipment1'}, dbi)
  res2 = loadobjects.loadobjects('Equipment', 'parent', 0, {'id':2, 'name': 'equipment2'}, dbi)
  res3 = loadobjects.loadobjects('Equipment', 'parent', 1, {'id':2, 'name': 'equipment2'}, dbi)
  res4 = loadobjects.loadobjects('Site', 'parent', 0, {'id':1, 'factoryId': 1, 'name': 'site1'}, dbi)
  res5 = loadobjects.loadobjects('Site', 'child', 0, {'id':2, 'factoryId': 1, 'name': 'site2'}, dbi)
  return res, res1, res2, res3, res4, res5