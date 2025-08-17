import sqlalchemy as sql
from sqlalchemy import create_engine, MetaData, Table, select

class Db:
  def __init__(self, path):
    self.engine = sql.create_engine(path)
    self.conn = self.engine.connect()
    self.metadata = MetaData()
    self.factories_table = Table("factories", self.metadata, autoload_with=self.engine)
    self.sites_table = Table("sites", self.metadata, autoload_with=self.engine)
    self.equipment_table = Table("equipment", self.metadata, autoload_with=self.engine)
    self.sites_equipment_table = Table("sites_equipment", self.metadata, autoload_with=self.engine)
