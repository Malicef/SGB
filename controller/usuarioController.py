from model.usuario import Usuario
from peewee import DoesNotExist

class UsuarioController:

    @staticmethod
    def cadastarUsuario(nome, cpf, senha):
        return Usuario.create(nome=nome, cpf=cpf, senha=senha)

    @staticmethod
    def autenticar(nome, senha):
        try:
            usuario = Usuario.get(Usuario.nome == nome, Usuario.senha == senha)

            return usuario
        except DoesNotExist:
            return None