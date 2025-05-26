# from model.livro import Livro
from model.acervo import Acervo
from controller.administradorController import adiministradorController
from controller.loginadm import loginadm


class BibliotecaController:
    def __init__(self):
        self.acervo = Acervo()
        
    
    def executar(self):
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
            log = loginadm()
            nome = input("nome:")
            senha = input("senha:")
            
            i = log.adm_nome(nome)
            j = log.adm_senha(senha)
            
            
            if i==None or j==None :
                print("nome ou senha não existe")
                continue
            else:
                break
            
            
        
    def criar_adm(self):
        adm = adiministradorController()
        
        nome =input("digite nome:")
        senha = input("digite senha:")
        cpf = input("digite cpf:")
        
        adm.criar_adm(nome,cpf, senha)
        
      
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


