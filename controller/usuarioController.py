from model.usuario import Usuario
from peewee import DoesNotExist

class UsuarioController:

    @staticmethod
    def cadastarUsuario(nome, cpf, senha):
        return Usuario.create(nome=nome, cpf=cpf, senha=senha)

    @staticmethod
    def autenticarUsuario(cpf, senha):
        try:
            usuario = Usuario.get(Usuario.cpf == cpf, Usuario.senha == senha)

            return True, usuario
        except DoesNotExist:
            return None, False


