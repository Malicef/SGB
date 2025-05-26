import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))  # Adiciona a raiz ao PATH


from controller.bibliotecaController import BibliotecaController
from db.db import db
from model.livro import Livro

def main():
    db.connect()
    db.create_tables([Livro])

    try:
        controller = BibliotecaController()
        controller.executar()
    finally:
        db.close()
        
if __name__ == "__main__":
    main()
