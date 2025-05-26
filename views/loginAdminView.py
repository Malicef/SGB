import tkinter as tk
from tkinter import messagebox
from views.adminView import Admin
from controller.loginadm import loginadm  

class LoginAdminView:
    def __init__(self, root):
        self.root = root
        self.root.title("Login do Administrador")
        self.root.state('zoomed')

        self.login_controller = loginadm()

        
        container = tk.Frame(root, bg="#f0f0f0")
        container.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(container, text="Login", bg="#f0f0f0", font=("Arial", 20)).grid(row=0, column=1, sticky="e", pady=10, padx=100)
        
        tk.Label(container, text="Usuário:", bg="#f0f0f0", font=("Arial", 14)).grid(row=1, column=0, sticky="e", pady=10, padx=10)
        self.username_entry = tk.Entry(container, font=("Arial", 14))
        self.username_entry.grid(row=1, column=1, pady=10)

        
        tk.Label(container, text="Senha:", bg="#f0f0f0", font=("Arial", 14)).grid(row=2, column=0, sticky="e", pady=10, padx=10)
        self.password_entry = tk.Entry(container, show="*", font=("Arial", 14))
        self.password_entry.grid(row=2, column=1, pady=10)

        
        tk.Button(container, text="Entrar", font=("Arial", 14), command=self.verificar_login).grid(row=3, column=0, columnspan=2, pady=20)

    def verificar_login(self):
        nome = self.username_entry.get().strip()
        senha = self.password_entry.get().strip()

        adm_nome = self.login_controller.adm_nome(nome)
        adm_senha = self.login_controller.adm_senha(senha)

        
        if adm_nome and adm_senha and adm_nome.id == adm_senha.id:
            self.root.destroy()
            nova_janela = tk.Tk()
            app = Admin(nova_janela)
            nova_janela.mainloop()
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos.")

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginAdminView(root)
    root.mainloop()
