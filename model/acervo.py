from .livro import Livro
from .livroDao import LivroDAO

class Acervo:
    
    def criar_livro(self, nome, autor, resumo):
        l = LivroDAO()
        l.inserir_livro(nome, autor, resumo)

    def listar_livros(self):
        dao = LivroDAO()
        livros = dao.listar_livros()  
        for livro in livros:
            livro.exibir()
