from controller.bibliotecaController import BibliotecaControllerr
from db.db import db
from model.livro import Livro
from model.administrador import administrador

def main():
    db.connect()
    db.create_tables([Livro])
    db.create_tables([administrador])

    try:
        controller = BibliotecaControllerr()
        controller.executar()
    finally:
        db.close()
        
if __name__ == "__main__":
    main()
