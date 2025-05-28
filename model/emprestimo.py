from peewee import CharField, IntegerField, DateField, ForeignKeyField, BooleanField
from db.db import BaseModel 
from model.livro import Livro
from model.usuario import Usuario

class Emprestimo(BaseModel):
    id = IntegerField(primary_key=True)
    idUsuario = ForeignKeyField(Usuario, backref='emprestimos')
    idLivro = ForeignKeyField(Livro, backref='emprestimos')
    dataEmprestimo = DateField()
    dataDevolucaoPrevista = DateField()
    dataDevolucaoReal = DateField(null=True, default=None)
    devolvido = BooleanField(default=False)
    status = CharField(default="pendente")