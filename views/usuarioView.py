import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from controller.bibliotecaController import BibliotecaController

class UsuarioView:
    def __init__(self, root, usuario):
        self.root = root
        self.usuario = usuario
        self.controller = BibliotecaController()
        self.window()
        self.sidebar()
        self.main_area()
        self.init_frames()
        self.show_content("ver_livros")

    def window(self):
        nome = self.usuario.nome if self.usuario else "Usuário"
        self.root.title(f"Área do Usuário - {nome}")
        self.root.title("Área do Usuário - Bruninho Livros")
        self.root.state('zoomed')
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

    def sidebar(self):
        sidebar = tk.Frame(self.root, width=300, bg="#f0f0f0", bd=2, relief='ridge')
        sidebar.grid(row=0, column=0, sticky='ns')
        sidebar.grid_propagate(False)

        tk.Label(sidebar, text="Bruninho dos\nLivros", font=("Arial", 24), bg="#f0f0f0").pack(pady=30, padx=50)

        menu = [
            ("📚 Ver Livros", "ver_livros"),
            ("📒 Livros Emprestados", "livros_emprestados"),
            ("📝 Solicitar Empréstimo", "solicitar_emprestimo"),  # Futuro
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
        self.frames["ver_livros"] = self.create_ver_livros_frame()
        self.frames["solicitar_emprestimo"] = self.create_solicitar_emprestimo_frame()
        self.frames["livros_emprestados"] = self.create_livros_emprestados_frame() 

    def show_content(self, name):
        for f in self.frames.values():
            f.grid_forget()

        frame = self.frames.get(name)

        if name == "ver_livros":
            self.update_livros()
        elif name == "livros_emprestados":
            self.update_livros_emprestados()  

        frame.grid(row=0, column=0, sticky='nsew')


    def update_livros_emprestados(self):
        for item in self.tree_emprestados.get_children():
            self.tree_emprestados.delete(item)

        emprestimos = self.controller.listar_emprestimos_usuario(self.usuario)

        print(f"[DEBUG] {len(emprestimos)} empréstimos encontrados")

        for emp in emprestimos:
            print(f"[DEBUG] Inserindo: {emp.idLivro.nome}")
            self.tree_emprestados.insert(
                '', 'end',
                values=(
                    emp.idLivro.nome,
                    emp.dataEmprestimo.strftime('%d/%m/%Y'),
                    emp.dataDevolucaoPrevista.strftime('%d/%m/%Y'),
                    emp.status
                )
            )




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

        return frame


    def create_solicitar_emprestimo_frame(self):
        frame = tk.Frame(self.main_content, bg='white', padx=20, pady=20)

        tk.Label(frame, text="Solicitar Empréstimo de Livro", font=("Arial", 16), bg='white').pack(anchor='w', pady=(0, 10))

        tk.Label(frame, text="Título do Livro:", bg='white').pack(anchor='w')
        self.titulo_entry = tk.Entry(frame)
        self.titulo_entry.pack(fill='x')

        tk.Button(frame, text="Solicitar", command=self.solicitar_emprestimo).pack(pady=15)

        return frame


    def atualizar_livros_para_solicitar(self):
        livros = self.controller.listar_livros_disponiveis_para_emprestimo()
        nomes_livros = [livro.nome for livro in livros]
        self.livros_disponiveis['values'] = nomes_livros
    

    def solicitar_emprestimo(self):
        titulo = self.titulo_entry.get().strip()
        if not titulo:
            messagebox.showwarning("Atenção", "Digite o título do livro.")
            return

        try:
            self.controller.solicitar_emprestimo(self.usuario, titulo)
            messagebox.showinfo("Solicitação Enviada", f"Sua solicitação para o livro '{titulo}' foi enviada e está pendente de aprovação.")
            self.titulo_entry.delete(0, 'end')
        except ValueError as e:
            messagebox.showerror("Erro", str(e))


    
    def create_ver_livros_frame(self):
        frame = tk.Frame(self.main_content, bg='white', padx=20, pady=20)

        tk.Label(frame, text="📖 Livros Disponíveis", font=("Arial", 16), bg='white').pack(anchor='w', pady=(0, 10))

        columns = ("Nome", "Autor", "Resumo")
        self.tree = ttk.Treeview(frame, columns=columns, show='headings')

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=200, anchor='center')

        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        return frame 


    def update_livros(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        livros = self.controller.listar_livros()
        for livro in livros:
            self.tree.insert('', 'end', values=(livro.nome, livro.autor, livro.resumo))


if __name__ == "__main__":
    root = tk.Tk()
    app = UsuarioView(root)
    root.mainloop()
