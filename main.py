from controller.bibliotecaController import BibliotecaControllerr
from db.db import db
from model.livro import Livro

def main():
    db.connect()
    db.create_tables([Livro])

    try:
        controller = BibliotecaControllerr()
        controller.executar()
    finally:
        db.close()
        
if __name__ == "__main__":
    main()
