from peewee import CharField, IntegerField
from db.db import BaseModel 
from peewee import  IntegerField
# from model.livro import Livro

class administrador(BaseModel):
    id = IntegerField(primary_key = True)
    nome = CharField()
    cpf = CharField()
    senha = CharField()