from peewee import CharField, IntegerField, DateField, ForeignKeyField, BooleanField
from db.db import BaseModel 
from model.livro import Livro
from model.usuario import Usuario

class Emprestimo(BaseModel):
    id = IntegerField(primary_key=True)
    idLivro = ForeignKeyField(Livro)
    idUsuario = ForeignKeyField(Usuario)
    dataEmprestimo = DateField()
    dataDevolucaoPrevista = DateField()
    dataDevolucaoReal = DateField()
    devolvido = BooleanField(default=False)
