from .livro import Livro
from controller.livroController import LivroController

class Acervo:
    
    def criar_livro(self, nome, autor, resumo):
        l = LivroController()
        l.inserir_livro(nome, autor, resumo)

    def listar_livros(self):
        dao = LivroController()
        livros = dao.listar_livros()  
        for livro in livros:
            livro.exibir()
    