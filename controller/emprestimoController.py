from model.emprestado import Emprestimo
from peewee import DoesNotExist

class EmprestimoController:

    @staticmethod
    def emprestarLivro(idLivro, idUsuario, dataEmprestimo, dataDevolucaoPrevista):
        try:
            Emprestimo.create(idLivro=idLivro, idUsuario=idUsuario, dataEmprestimo=dataEmprestimo, dataDevolucaoPrevista=dataDevolucaoPrevista, devolvido=False)
            return Emprestimo
        except Exception as e:
            return None
    
    @staticmethod
    def devolucaoLivro(idEmprestimo, dataDevolucaoReal):
        try: 
            emprestado = Emprestimo.get((Emprestimo.id == idEmprestimo) & (Emprestimo.devolvido == False))
            emprestado.dataDevolucaoReal = dataDevolucaoReal
            emprestado.devolvido = True

            atrasado = dataDevolucaoReal > emprestado.dataDevolucaoPrevista
            emprestado.save()

            return {
                "emprestimo": emprestimo,
                "atrasado": atrasado,
                "dias_atraso": (dataDevolucaoReal - emprestimo.dataDevolucaoPrevista).days if atrasado else 0
            }

        except DoesNotExist:
            return None
        except Exception:
            return None





