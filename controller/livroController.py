from model.livro import Livro

class LivroController:
    @staticmethod
    def inserir_livro(nome, autor, resumo):
        Livro.create(
            nome=nome,
            autor=autor,
            resumo = resumo,
        )

    
    def listar_livros(self):
        return Livro.select()


    def buscar_por_titulo(nome):
        return Livro.get_or_none(Livro.nome == nome)

    
    def atualizar_genero(nome, novo_genero):
        livro = Livro.get_or_none(Livro.nome == nome)
        if livro:
            livro.genero = novo_genero
            livro.save()

    
    def deletar_por_titulo(nome):
        livro = Livro.get_or_none(Livro.nome == nome)
        if livro:
            livro.delete_instance()
