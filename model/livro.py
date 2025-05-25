from peewee import CharField, BooleanField
from db.db import BaseModel 
from peewee import  IntegerField

class Livro(BaseModel):
    id = IntegerField(primary_key=True)
    nome = CharField()
    autor = CharField()
    resumo = CharField()
    emprestado = BooleanField(default=False)

    def exibir(self):
        print(f"{self.nome} - {self.autor}")
