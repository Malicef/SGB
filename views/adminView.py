import tkinter as tk
from tkinter import messagebox, ttk
from controller.bibliotecaController import BibliotecaController
from model.acervo import Acervo
from controller.emprestimoController import EmprestimoController
from datetime import datetime


class Admin:
    def __init__(self, root):
        self.root = root
        self.controller = BibliotecaController()
        self.ctrl = Acervo()
        self.window()
        self.sidebar()
        self.main_area()
        self.init_frames()
        self.show_content("listar_livros")

    def window(self):
        self.root.title("Bruninho Livros")
        self.root.state('zoomed')
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

    def sidebar(self):
        sidebar = tk.Frame(self.root, width=300, bg="#f0f0f0", bd=2, relief='ridge')
        sidebar.grid(row=0, column=0, sticky='ns')
        sidebar.grid_propagate(False)

        tk.Label(sidebar, text="Bruninho dos\nLivros", font=("Arial", 24), bg="#f0f0f0").pack(pady=30)

        menu = [
            ("📚 Listar Livros", "listar_livros"),
            ("📖 Criar Livro", "criar_livros"),
            ("🗑️ Deletar Livro", "deletar_livros"),
            ("📒 Emprestar Livro", "emprestar_livro")
        ]

        for text, command in menu:
            btn = tk.Button(
                sidebar, text=text, font=("Arial", 12), bg="#ffffff", anchor='w', padx=20, pady=10,
                relief='flat', command=lambda c=command: self.show_content(c)
            )
            btn.pack(fill='x', padx=10, pady=5)


    def main_area(self):
        self.main_content = tk.Frame(self.root, bg='white')
        self.main_content.grid(row=0, column=1, sticky='nsew')
        self.main_content.grid_rowconfigure(0, weight=1)
        self.main_content.grid_columnconfigure(0, weight=1)


    def init_frames(self):
        self.frames = {}
        self.frames["listar_livros"] = self.create_listar_livros_frame()
        self.frames["criar_livros"] = self.create_criar_livros_frame()
        self.frames["deletar_livros"] = self.create_deletar_livros_frame() #-> opcao deletar livro
        # self.frames["emprestar_livro"] = self.create_emprestar_livro_frame()


    # Deletar livro 
    def create_deletar_livros_frame(self):
        frame = tk.Frame(self.main_content, bg='white', padx=20, pady=20)

        tk.Label(frame, text="Informe o título do livro:", bg='white').pack(anchor='w')
        self.deletar_entry = tk.Entry(frame)
        self.deletar_entry.pack(fill='x')

        tk.Button(frame, text="Deletar Livro", command=self.deletar_livro).pack(pady=15)

        return frame

    # def create_emprestar_livro_frame(self):
    #     frame = tk.Frame(self.main_content, bg='white', padx=20, pady=20)

    #     tk.Label(frame, text="Nome do Livro:", bg='white').pack(anchor='w')
    #     self.nome_livro_entry = tk.Entry(frame)
    #     self.nome_livro_entry.pack(fill='x')

    #     tk.Label(frame, text="CPF do Usuário:", bg='white').pack(anchor='w', pady=(10, 0))
    #     self.cpf_usuario_entry = tk.Entry(frame)
    #     self.cpf_usuario_entry.pack(fill='x')

    #     tk.Label(frame, text="Data do Empréstimo (AAAA-MM-DD):", bg='white').pack(anchor='w', pady=(10, 0))
    #     self.data_emprestimo_entry = tk.Entry(frame)
    #     self.data_emprestimo_entry.pack(fill='x')

    #     tk.Label(frame, text="Data Prevista de Devolução (AAAA-MM-DD):", bg='white').pack(anchor='w', pady=(10, 0))
    #     self.data_prevista_entry = tk.Entry(frame)
    #     self.data_prevista_entry.pack(fill='x')

    #     tk.Button(frame, text="Confirmar Empréstimo", command=self.confirmar_emprestimo).pack(pady=15)

    #     return frame


    # def confirmar_emprestimo(self):
    #     try:
    #         nome_livro = self.nome_livro_entry.get().strip()
    #         cpf_usuario = self.cpf_usuario_entry.get().strip()
    #         data_emprestimo = datetime.strptime(self.data_emprestimo_entry.get(), "%Y-%m-%d").date()
    #         data_prevista = datetime.strptime(self.data_prevista_entry.get(), "%Y-%m-%d").date()

    #         if not nome_livro or not cpf_usuario:
    #             messagebox.showwarning("Campos obrigatórios", "Preencha o nome do livro e o CPF do usuário.")
    #             return

    #         resultado = EmprestimoController.emprestar_por_nome_e_cpf(
    #             nome_livro, cpf_usuario, data_emprestimo, data_prevista
    #         )

    #         if resultado:
    #             messagebox.showinfo("Sucesso", "Empréstimo registrado com sucesso!")
    #             self.nome_livro_entry.delete(0, 'end')
    #             self.cpf_usuario_entry.delete(0, 'end')
    #             self.data_emprestimo_entry.delete(0, 'end')
    #             self.data_prevista_entry.delete(0, 'end')
    #         else:
    #             messagebox.showerror("Erro", "Erro ao registrar empréstimo. Verifique os dados.")
    #     except Exception as e:
    #         messagebox.showerror("Erro", f"Entrada inválida: {e}")



    def deletar_livro(self):
        nome = self.deletar_entry.get().strip()
        if not nome:
            messagebox.showwarning("Atenção", "Digite o nome do livro.")
            return

        try:
            from controller.livroController import LivroController
            lc = LivroController()
            sucesso = lc.deletar_por_titulo(nome)
            if sucesso:
                messagebox.showinfo("Sucesso", f"Livro '{nome}' deletado com sucesso.")
                self.deletar_entry.delete(0, 'end')
                self.show_content("listar_livros")
            else:
                messagebox.showerror("Erro", f"O livro '{nome}' não foi encontrado.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao deletar: {e}")

    
    def create_listar_livros_frame(self):
        frame = tk.Frame(self.main_content, bg='white')
        tree = ttk.Treeview(frame, columns=("Nome", "Autor", "Resumo"), show='headings')

        for col in ("Nome", "Autor", "Resumo"):
            tree.heading(col, text=col)
            tree.column(col, width=200)

        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        self.tree = tree
        return frame

    def create_criar_livros_frame(self):
        frame = tk.Frame(self.main_content, bg='white', padx=20, pady=20)

        tk.Label(frame, text="Nome do Livro:", bg='white').pack(anchor='w')
        self.nome_entry = tk.Entry(frame)
        self.nome_entry.pack(fill='x')

        tk.Label(frame, text="Autor:", bg='white').pack(anchor='w', pady=(10, 0))
        self.autor_entry = tk.Entry(frame)
        self.autor_entry.pack(fill='x')

        tk.Label(frame, text="Resumo:", bg='white').pack(anchor='w', pady=(10, 0))
        self.resumo_entry = tk.Text(frame, height=5)
        self.resumo_entry.pack(fill='x')

        tk.Button(frame, text="Criar Livro", command=self.criar_livro).pack(pady=15)

        return frame


    def show_content(self, name):
        for f in self.frames.values():
            f.grid_forget()
        frame = self.frames.get(name)
        if name == "listar_livros":
            self.update_listar_livros()
        frame.grid(row=0, column=0, sticky='nsew')


    def criar_livro(self):
        nome = self.nome_entry.get().strip()
        autor = self.autor_entry.get().strip()
        resumo = self.resumo_entry.get("1.0", "end").strip()

        if not nome or not autor or not resumo:
            messagebox.showwarning("Campos obrigatórios", "Por favor, preencha todos os campos antes de continuar.")
            return

        resultado = self.ctrl.criar_livro(nome, autor, resumo)

        if resultado is True:
            messagebox.showinfo("Sucesso", "Livro criado com sucesso!")
            self.nome_entry.delete(0, 'end')
            self.autor_entry.delete(0, 'end')
            self.resumo_entry.delete("1.0", 'end')
            self.show_content("listar_livros")
        else:
            messagebox.showerror("Erro", "Erro ao criar livro. Verifique os dados.")


    def update_listar_livros(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        livros = self.controller.listar_livros()
        if livros:
            for livro in livros:
                self.tree.insert('', 'end', values=(livro.nome, livro.autor, livro.resumo))


if __name__ == "__main__":
    root = tk.Tk()
    app = Admin(root)
    root.mainloop()