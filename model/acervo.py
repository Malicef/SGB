from .livro import Livro
from controller.livroController import LivroController
# from livro import Livro
from controller.livroController import LivroController

class Acervo:
    
    def criar_livro(self, nome, autor, resumo):
        l = LivroController()
        l.inserir_livro(nome, autor, resumo)
        return True

    def listar_livros(self):
        dao = LivroController()
        return dao.listar_livros()