from .administradorController import adiministradorController


class loginadm():
    
    def adm_nome(self, nome):
        self.adm = adiministradorController()
        
        self.resultado = self.adm.buscar_por_nome(nome)
        return self.resultado
            
    def adm_senha(self, senha):
        self.adm = adiministradorController()
        
        self.resultado = self.adm.buscar_por_senha(senha)
        return self.resultado