import tkinter as tk
from tkinter import messagebox
from views.usuarioView import UsuarioView  
from controller.usuarioController import UsuarioController  

class LoginUsuarioView:
    def __init__(self, root):
        self.root = root
        self.root.title("Login do Usuário")
        self.root.state('zoomed')
        self.login_controller = UsuarioController()

        container = tk.Frame(root, bg="#f0f0f0")
        container.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(container, text="Login do Usuário", bg="#f0f0f0", font=("Arial", 20)).grid(row=0, column=1, pady=10, padx=100)

        tk.Label(container, text="Nome:", bg="#f0f0f0", font=("Arial", 14)).grid(row=1, column=0, sticky="e", pady=10, padx=10)
        self.nome_entry = tk.Entry(container, font=("Arial", 14))
        self.nome_entry.grid(row=1, column=1, pady=10)

        tk.Label(container, text="Senha:", bg="#f0f0f0", font=("Arial", 14)).grid(row=2, column=0, sticky="e", pady=10, padx=10)
        self.password_entry = tk.Entry(container, show="*", font=("Arial", 14))
        self.password_entry.grid(row=2, column=1, pady=10)

        tk.Button(container, text="Entrar", font=("Arial", 14), command=self.verificar_login).grid(row=3, column=0, columnspan=2, pady=20)

    def verificar_login(self):
        nome = self.nome_entry.get().strip()
        senha = self.password_entry.get().strip()

        usuario = self.login_controller.autenticar(nome, senha)

        if usuario:
            self.root.destroy()
            nova_janela = tk.Tk()
            app = UsuarioView(nova_janela, usuario)
            nova_janela.mainloop()
        else:
            messagebox.showerror("Erro", "Nome ou senha incorretos.")
