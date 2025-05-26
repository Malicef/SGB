from .administradorController import adiministradorController


class loginadm():
    
    
    def adm_nome(self, nome):
        adm = adiministradorController()
        
        resultado = adm.buscar_por_nome(nome)

        return resultado
            
    def adm_senha(self, senha):
        adm = adiministradorController()
        
        resultado = adm.buscar_por_senha(senha)

            
        return resultado