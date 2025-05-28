import tkinter as tk
from tkinter import messagebox, ttk
from model.emprestimo import Emprestimo
from controller.bibliotecaController import BibliotecaController
from model.acervo import Acervo
from controller.emprestimoController import EmprestimoController
from datetime import date, datetime


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
        self.verificar_solicitacoes_pendentes()


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
            ("📒 Emprestar Livro", "solicitacoes_emprestimo"),
            ("📕 Livros Emprestados", "livros_emprestados")
        ]

        
        for text, command in menu:
            btn = tk.Button(
                sidebar, text=text, font=("Arial", 12), bg="#ffffff", anchor='w', padx=20, pady=10,
                relief='flat', command=lambda c=command: self.show_content(c)
            )
            btn.pack(fill='x', padx=10, pady=5)

            if command == "emprestar_livro":
                self.btn_emprestar = btn


    def main_area(self):
        self.main_content = tk.Frame(self.root, bg='white')
        self.main_content.grid(row=0, column=1, sticky='nsew')
        self.main_content.grid_rowconfigure(0, weight=1)
        self.main_content.grid_columnconfigure(0, weight=1)


    def init_frames(self):
        self.frames = {}
        self.frames["listar_livros"] = self.create_listar_livros_frame()
        self.frames["criar_livros"] = self.create_criar_livros_frame()
        self.frames["deletar_livros"] = self.create_deletar_livros_frame() 
        self.frames["solicitacoes_emprestimo"] = self.create_solicitacoes_emprestimo_frame()
        self.frames["livros_emprestados"] = self.create_livros_emprestados_frame()


    def create_solicitacoes_emprestimo_frame(self):
        frame = tk.Frame(self.main_content, bg='white', padx=20, pady=20)

        tk.Label(frame, text="Solicitações Pendentes de Empréstimo", font=("Arial", 16), bg='white').pack(anchor='w', pady=(0,10))

        columns = ("ID", "Livro", "Usuário", "Ações")
        self.tree_solicitacoes = ttk.Treeview(frame, columns=columns[:-1], show='headings')
        for col in columns[:-1]:
            self.tree_solicitacoes.heading(col, text=col)
            self.tree_solicitacoes.column(col, width=150)

        self.tree_solicitacoes.pack(fill='both', expand=True)

        btn_frame = tk.Frame(frame, bg='white')
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Aceitar", command=self.aceitar_solicitacao).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Recusar", command=self.recusar_solicitacao).pack(side='left', padx=5)

        self.update_solicitacoes()

        return frame

    def create_livros_emprestados_frame(self):
        frame = tk.Frame(self.main_content, bg='white', padx=20, pady=20)

        columns = ("ID", "Livro", "Usuário", "Data Empréstimo", "Data Devolução Prevista", "Status")
        
        self.tree_emprestados = ttk.Treeview(frame, columns=columns, show='headings')
        for col in columns:
            self.tree_emprestados.heading(col, text=col)
            self.tree_emprestados.column(col, width=120, anchor='center')

        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=self.tree_emprestados.yview)
        self.tree_emprestados.configure(yscrollcommand=scrollbar.set)

        self.tree_emprestados.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        devolver_btn = tk.Button(frame, text="Devolver Livro", command=self.devolver_livro_selecionado)
        devolver_btn.pack(pady=10)

        return frame


    def update_livros_emprestados(self):
    # Limpa a treeview
        for item in self.tree_emprestados.get_children():
            self.tree_emprestados.delete(item)

        emprestimos = Emprestimo.select().where(
            (Emprestimo.status == "aceito") & 
            (Emprestimo.devolvido == False)
        )

        for emp in emprestimos:
            self.tree_emprestados.insert(
                '', 'end',
                values=(
                    emp.id,
                    emp.idLivro.nome,
                    emp.idUsuario.nome,
                    emp.dataEmprestimo.strftime("%d/%m/%Y"),
                    emp.dataDevolucaoPrevista.strftime("%d/%m/%Y"),
                    "Sim" if emp.devolvido else "Não"
                )
            )




    def devolver_livro_selecionado(self):
        selected = self.tree_emprestados.selection()
        if not selected:
            messagebox.showwarning("Atenção", "Selecione um empréstimo para devolver.")
            return

        item_data = self.tree_emprestados.item(selected[0])
        if item_data['values'][5] == "Sim":  # Verifica coluna "Devolvido"
            messagebox.showwarning("Aviso", "Este livro já foi devolvido.")
            return

        emprestimo_id = int(self.tree_emprestados.item(selected[0])['values'][0])
        
        try:
            resultado = EmprestimoController.devolucaoLivro(
                idEmprestimo=emprestimo_id,
                dataDevolucaoReal=date.today()
            )
            
            if resultado:
                if resultado['atrasado']:
                    msg = f"Livro devolvido com sucesso! (Atraso: {resultado['dias_atraso']} dias)"
                else:
                    msg = "Livro devolvido com sucesso dentro do prazo!"
                
                messagebox.showinfo("Sucesso", msg)
                self.update_livros_emprestados()
            else:
                messagebox.showerror("Erro", "Não foi possível processar a devolução")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao devolver o livro: {e}")

    def show_content(self, name):
        print(f"Mostrando frame: {name}")
        for f in self.frames.values():
            f.grid_forget()
        frame = self.frames.get(name)
        
        if name == "listar_livros":
            self.update_listar_livros()
        elif name == "livros_emprestados":
            self.update_livros_emprestados()
        elif name == "solicitacoes_emprestimo":
            self.update_solicitacoes()
        
        frame.grid(row=0, column=0, sticky='nsew')




    def verificar_solicitacoes_pendentes(self):
        from model.emprestimo import Emprestimo
        pendentes = Emprestimo.select().where(Emprestimo.status == "pendente")
        if pendentes.exists():
            self.btn_emprestar.configure(bg="#FFD700")  # Amarelo
        else:
            self.btn_emprestar.configure(bg="#FFFFFF")  # Branco padrão


    def update_solicitacoes(self):
        for item in self.tree_solicitacoes.get_children():
            self.tree_solicitacoes.delete(item)

        solicitacoes = Emprestimo.select().where(Emprestimo.status == "pendente")
        for sol in solicitacoes:
            self.tree_solicitacoes.insert('', 'end', iid=sol.id, values=(sol.id, sol.idLivro.nome, sol.idUsuario.nome))

    def aceitar_solicitacao(self):
        selected = self.tree_solicitacoes.selection()
        if not selected:
            messagebox.showwarning("Atenção", "Selecione uma solicitação para aceitar.")
            return

        idEmprestimo = int(selected[0])
      
        from datetime import date, timedelta
        dataDevolucaoPrevista = date.today() + timedelta(days=7)

        sucesso = EmprestimoController.aceitar_emprestimo(idEmprestimo, dataDevolucaoPrevista)
        if sucesso:
            messagebox.showinfo("Sucesso", "Empréstimo aceito.")
            self.update_solicitacoes()
            self.show_content("listar_livros")  
        else:
            messagebox.showerror("Erro", "Falha ao aceitar empréstimo.")
        
        self.verificar_solicitacoes_pendentes()


    def recusar_solicitacao(self):
        selected = self.tree_solicitacoes.selection()
        if not selected:
            messagebox.showwarning("Atenção", "Selecione uma solicitação para recusar.")
            return

        idEmprestimo = int(selected[0])
        sucesso = EmprestimoController.recusar_emprestimo(idEmprestimo)
        if sucesso:
            messagebox.showinfo("Sucesso", "Empréstimo recusado.")
            self.update_solicitacoes()
        else:
            messagebox.showerror("Erro", "Falha ao recusar empréstimo.")
        
        self.verificar_solicitacoes_pendentes()

    
    # Deletar livro 
    def create_deletar_livros_frame(self):
        frame = tk.Frame(self.main_content, bg='white', padx=20, pady=20)

        tk.Label(frame, text="Informe o título do livro:", bg='white').pack(anchor='w')
        self.deletar_entry = tk.Entry(frame)
        self.deletar_entry.pack(fill='x')

        tk.Button(frame, text="Deletar Livro", command=self.deletar_livro).pack(pady=15)

        return frame



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