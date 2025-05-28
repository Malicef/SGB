# from model.livro import Livro
from datetime import date, timedelta
from controller.emprestimoController import EmprestimoController
from model.emprestimo import Emprestimo
from model.livro import Livro
from model.acervo import Acervo
from controller.administradorController import adiministradorController
from controller.loginadm import loginadm
from controller.usuarioController import UsuarioController

class BibliotecaController:
    def __init__(self):
        self.acervo = Acervo()
        self.usuario = UsuarioController()
        self.solicitacoes_pendentes = []

    def solicitar_emprestimo(self, usuario, titulo_livro):
        try:
            livro = Livro.get(Livro.nome == titulo_livro)
        except Livro.DoesNotExist:
            raise ValueError("Livro não encontrado.")

        emprestimo_existente = Emprestimo.select().where(
            (Emprestimo.idLivro == livro) &
            (Emprestimo.idUsuario == usuario) &
            (Emprestimo.devolvido == False)
        )

        if emprestimo_existente.exists():
            raise ValueError("Você já possui um empréstimo ativo ou pendente deste livro.")

        Emprestimo.create(
            idLivro=livro,
            idUsuario=usuario,
            dataEmprestimo=date.today(),
            dataDevolucaoPrevista=date.today() + timedelta(days=7),
            dataDevolucaoReal=None,
            devolvido=False,
            status="pendente"
        )
        
        
    def aprovar_emprestimo(self, emprestimo_id):
        emprestimo = Emprestimo.get_by_id(emprestimo_id)
        emprestimo.status = 'aprovado'
        emprestimo.save()

        # Atualiza o livro para indisponível
        emprestimo.idLivro.disponivel = False
        emprestimo.idLivro.save()

    def recusar_emprestimo(self, emprestimo_id):
        emprestimo = Emprestimo.get_by_id(emprestimo_id)
        emprestimo.status = 'recusado'
        emprestimo.save()

    def listar_solicitacoes(self):
        return self.solicitacoes_pendentes
    
    def listar_emprestimos_usuario(self, usuario):
        return (
            Emprestimo
            .select()
            .where(
                (Emprestimo.idUsuario == usuario) & 
                (Emprestimo.status.in_(["aprovado", "aceito"])) &
                (Emprestimo.devolvido == False)
            )
            .order_by(Emprestimo.dataEmprestimo.desc())
        )

    def devolver_livro(self, emprestimo_id):
        emprestimo = Emprestimo.get_by_id(emprestimo_id)
        if emprestimo.devolvido:
            raise ValueError("Este livro já foi devolvido.")

        emprestimo.devolvido = True
        emprestimo.dataDevolucaoReal = date.today()
        emprestimo.save()

        livro = emprestimo.idLivro
        livro.disponivel = True
        livro.save()


    
    def executar(self):
        # self.criar_adm()
        # self.login()
        # self.criar_usuario()
        
        
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
            
            
        
    def criar_usuario(self):
        
        nome =input("digite nome:")
        senha = input("digite senha:")
        cpf = input("digite cpf:")
        
        self.usuario.cadastarUsuario(nome, cpf, senha)
        
        
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


    def listar_livros_disponiveis_para_emprestimo(self):
    # Retorna livros que não estão emprestados (status aceito e não devolvido)
        livros_emprestados = Emprestimo.select().where(
            (Emprestimo.status == "aceito") & (Emprestimo.devolvido == False)
        ).execute()
        ids_emprestados = [e.idLivro.id for e in livros_emprestados]

        livros = Livro.select().where(Livro.id.not_in(ids_emprestados))
        return livros

    def buscar_livro_por_nome(self, nome):
        return Livro.get_or_none(Livro.nome == nome)
