from peewee import CharField, IntegerField
from db.db import BaseModel 

class Usuario(BaseModel):
    id = IntegerField(primary_key = True)
    nome = CharField()
    cpf = CharField()
    senha = CharField()