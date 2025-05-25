from peewee import CharField, IntegerField
from db.db import BaseModel 
# from model.livro import Livro

class Usuario(BaseModel):
    id = IntegerField(primary_key = True)
    nome = CharField
    cpf = CharField
    senha = CharField