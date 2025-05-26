# from model.livro import Livro
from model.acervo import Acervo
from controller.administradorController import adiministradorController
from controller.loginadm import loginadm


class BibliotecaController:
    def __init__(self):
        self.acervo = Acervo()
        
    
    def executar(self):
        # self.criar_adm()
        self.login()
        
        
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
                
                
    def login(self):
        while True:
            self.log = loginadm()
            self.nome = input("nome:")
            self.senha = input("senha:")
            
            self.i = self.log.adm_nome(self.nome)
            self.j = self.log.adm_senha(self.senha)
            
            
            if self.i==None or self.j==None :
                print("nome ou senha não existe")
                continue
            else:
                break
            
            
        
    def criar_adm(self):
        self.adm = adiministradorController()
        
        self.nome =input("digite nome:")
        self.senha = input("digite senha:")
        self.cpf = input("digite cpf:")
        
        self.adm.criar_adm(self.nome,self.cpf, self.senha)
        
      
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


