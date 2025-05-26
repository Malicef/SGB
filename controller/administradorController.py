from model.administrador import administrador

class adiministradorController:
    
    def criar_adm(self, nome, cpf, senha):
        administrador.create(
            nome=nome,
            cpf=cpf,
            senha=senha
        )
        
    def buscar_por_nome(self, nome):
        return administrador.get_or_none(administrador.nome == nome)  
    
    
    def buscar_por_senha(self, senha):
        return administrador.get_or_none(administrador.senha == senha)  