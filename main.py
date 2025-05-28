import sys
from pathlib import Path
import tkinter as tk
sys.path.append(str(Path(__file__).parent))


from controller.bibliotecaController import BibliotecaController
from db.db import db
from model.livro import Livro
from model.administrador import administrador
from model.usuario import Usuario
from model.emprestimo import Emprestimo 
from views.loginUsuarioView import LoginUsuarioView
from views.loginAdminView import LoginAdminView

def main():
    db.connect()
    db.create_tables([Livro])
    db.create_tables([administrador])
    db.create_tables([Usuario])
    db.create_tables([Emprestimo])

    try:
        root = tk.Tk()
        # app = LoginUsuarioView(root)
        app = LoginAdminView(root)
        root.mainloop()
        # controller = BibliotecaController()
        # controller.executar()
    finally:
        db.close()

if __name__ == "__main__":
    main()
