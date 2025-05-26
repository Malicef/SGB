# from model.livro import Livro
from model.acervo import Acervo


class BibliotecaController:
    def __init__(self):
        self.acervo = Acervo()  
    
    def executar(self):
        while True:
            op = input("0-sair\n1-criar livro\n2-listar livro\n").strip()
            if not op.isdigit():
                print("Digite uma opção válida.")
                continue
            op = int(op)
            
            if op == 1:
                self.criar_livro()
            
            elif op == 2:
                self.listar_livros()            
            
            elif op == 0:
                print("saindo")
                break
            else:
                print("Opção inválida")
      
    def criar_livro(self, nome, autor, resumo):
        nome = input("Digite o nome do livro: ").strip()
        if not nome:
            print("Erro: nome do livro não pode ser vazio.")
            return False

        autor = input("Digite autor do livro: ").strip()
        resumo = input("Digite resumo: ").strip()

       

        self.acervo.criar_livro(self, nome, autor, resumo)
        print("Livro criado com sucesso!")
        return True
  
    
    def listar_livros(self):
        return self.acervo.listar_livros()


