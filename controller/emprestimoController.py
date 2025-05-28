from model.emprestimo import Emprestimo
from peewee import DoesNotExist
from datetime import date

class EmprestimoController:

    @staticmethod
    def emprestarLivro(idLivro, idUsuario, dataEmprestimo, dataDevolucaoPrevista):
        try:
            emprestimo = Emprestimo.create(idLivro=idLivro, idUsuario=idUsuario, dataEmprestimo=dataEmprestimo, dataDevolucaoPrevista=dataDevolucaoPrevista, devolvido=False)
            return emprestimo
        except Exception as e:
            print('Erro ao emprestar livro: ', e)
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

    @staticmethod
    def solicitar_emprestimo(idLivro, idUsuario):
        try:
            
            emprestimo = Emprestimo.create(
                idLivro=idLivro,
                idUsuario=idUsuario,
                status="pendente",
                devolvido=False,
                dataEmprestimo=None,
                dataDevolucaoPrevista=None,
                dataDevolucaoReal=None
            )
            return emprestimo
        except Exception as e:
            print(f"Erro ao solicitar empréstimo: {e}")
            return None

    @staticmethod
    def aceitar_emprestimo(idEmprestimo, dataDevolucaoPrevista):
        try:
            emprestimo = Emprestimo.get(Emprestimo.id == idEmprestimo)
            emprestimo.status = "aceito"
            emprestimo.devolvido = False
            emprestimo.dataEmprestimo = date.today()
            emprestimo.dataDevolucaoPrevista = dataDevolucaoPrevista
            emprestimo.save()
            return True
        except Exception as e:
            print(f"Erro ao aceitar empréstimo: {e}")
            return False

    @staticmethod
    def recusar_emprestimo(idEmprestimo):
        try:
            emprestimo = Emprestimo.get(Emprestimo.id == idEmprestimo)
            emprestimo.status = "recusado"
            emprestimo.save()
            return True
        except Exception as e:
            print(f"Erro ao recusar empréstimo: {e}")
            return False

