from model db import BaseModel
from peewee import charField, IntegerField, ForeignKeyField

class livro(BaseModel):
    id = IntegerField(primary_key=True)
    titulo = charField()
    autor = charField()
    data_lancamento = charField()
    editora = charField()
    genero = charField()