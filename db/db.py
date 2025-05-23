from peewee import SqliteDatabase

db = SqliteDatabase('database.db')

class BaseModel(Model):
    class Meta:
        database = sqlite_db

db = sqlite_db