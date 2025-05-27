from model.emprestimo import Emprestimo
from peewee import DoesNotExist

class EmprestimoController:

    @staticmethod
    def emprestarLivro(self, idLivro, idUsuario, dataEmprestimo, dataDevolucaoPrevista):
        try:
            emprestimo = Emprestimo.create(idLivro=idLivro, idUsuario=idUsuario, dataEmprestimo=dataEmprestimo, dataDevolucaoPrevista=dataDevolucaoPrevista, devolvido=False)
            return emprestimo
        except Exception as e:
            print('Erro ao emprestar livro: ', e)
            return None
    
    @staticmethod
    def devolucaoLivro(self, idEmprestimo, dataDevolucaoReal):
        try: 
            emprestado = Emprestimo.get((Emprestimo.id == idEmprestimo) & (Emprestimo.devolvido == False))
            emprestado.dataDevolucaoReal = dataDevolucaoReal
            emprestado.devolvido = True

            atrasado = dataDevolucaoReal > emprestado.dataDevolucaoPrevista
            emprestado.save()

            return {
                "emprestimo": emprestado,
                "atrasado": atrasado,
                "dias_atraso": (dataDevolucaoReal - emprestado.dataDevolucaoPrevista).days if atrasado else 0
            }

        except DoesNotExist:
            print("Empréstimo não encontrado.")
            return None
        except Exception as e:
            print("Erro ao devolver livro:", e)
            return None

