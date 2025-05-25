from datatime import datatime, timedelta
from model.emprestado import Emprestimo
from model.usuario import Usuario
from peewee import DoesNotExist

class EmprestimoController:

    @staticmethod
    def criarEmprestimo(idLivro, idUsuario, dataEmprestimo, dataDevolucaoPrevista):
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

    @staticmethod
    def pedirEmprestimo(id_usuario, id_livro):
        try:
            usuario = Usuario.get_by_id(id_usuario)
            emprestimo = Emprestimo.create(
                livro.id_livro,
                usuario=usuario,
                data_solicitacao=datetime.now(),
                status = Emprestimo.STATUS_PENDENTE
            )

            return {
                "sucesso": True,
                "emprestimo": emprestimo,
                "mensage": "Solicitação de empréstimo criada com sucesso, aguarde aprovação."
            }
        except DoesNotExist:
            return {"success": False, "message": "Usuário ou livro não encontrado."}
        except Exception as e:
            return {"success": False, "message": f"Erro ao solicitar empréstimo: {str(e)}"}







