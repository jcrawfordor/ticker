from peewee import *
db = SqliteDatabase('lists.db')

class BaseModel(Model):
    class Meta:
        database = db

class List(BaseModel):
    name = TextField()

class Item(BaseModel):
    list = ForeignKeyField(List, backref='items')
    name = TextField()
