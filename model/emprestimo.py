from peewee import CharField, IntegerField, DateField, ForeignKeyField, BooleanField
from db.db import BaseModel 
from model.livro import Livro
from model.usuario import Usuario

class Emprestimo(BaseModel):
    STATUS_PENDENTE = 'pendente'
    STATUS_APROVADO = 'aprovado'
    STATUS_NEGADO = 'negado'
    STATUS_DEVOLVIDO = 'devolvido'

    id = IntegerField(primary_key=True)
    idLivro = ForeignKeyField(Livro)
    idUsuario = ForeignKeyField(Usuario)
    dataEmprestimo = DateField()
    dataDevolucaoPrevista = DateField()
    dataDevolucaoReal = DateField()
    status = CharField(default=STATUS_PENDENTE)
