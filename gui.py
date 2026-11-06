import customtkinter as ctk
from tkinter import messagebox
from database import EstoqueDB
from auth import AuthSystem

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class LoginWindow(ctk.CTk):
    def __init__(self, on_success):
        super().__init__()
        self.auth = AuthSystem()
        self.on_success = on_success
        self.title("Login - StockMaster Pro")
        self.geometry("400x300")
        
        frame = ctk.CTkFrame(self)
        frame.pack(pady=40, padx=40, fill="both", expand=True)
        ctk.CTkLabel(frame, text="Acesso ao Sistema", font=("Arial", 20, "bold")).pack(pady=20)
        self.u = ctk.CTkEntry(frame, placeholder_text="Operador")
        self.u.pack(pady=10)
        self.p = ctk.CTkEntry(frame, placeholder_text="Senha", show="*")
        self.p.pack(pady=10)
        ctk.CTkButton(frame, text="Entrar", command=self.login).pack(pady=20)

    def login(self):
        user = self.u.get()
        senha = self.p.get()
        sucesso, nivel = self.auth.validar_login(user, senha)
        if sucesso:
            self.withdraw() # Esconde a janela
            self.on_success(user, nivel)
            self.after(100, self.destroy) # Destrói após abrir o app
        else:
            messagebox.showerror("Erro", "Dados inválidos!")

class AppEstoque(ctk.CTk):
    def __init__(self, usuario, nivel):
        super().__init__()
        self.usuario_logado = usuario
        self.nivel_usuario = nivel 
        self.db = EstoqueDB()
        self.auth = AuthSystem()
        
        self.title("StockMaster Pro")
        self.geometry("900x600")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- SIDEBAR ---
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        ctk.CTkLabel(self.sidebar, text="📦 StockMaster", font=("Arial", 20, "bold")).pack(pady=20, padx=20)
        
        ctk.CTkButton(self.sidebar, text="Cadastrar", command=self.janela_cadastro).pack(pady=10, padx=20)
        ctk.CTkButton(self.sidebar, text="Movimentar", command=self.janela_movimentacao).pack(pady=10, padx=20)
        ctk.CTkButton(self.sidebar, text="Atualizar", command=self.carregar_dados).pack(pady=10, padx=20)

        self.btn_admin_users = ctk.CTkButton(self.sidebar, text="Gerenciar Usuários", command=self.janela_usuarios)
        self.btn_admin_users.pack(pady=10, padx=20)
        if self.nivel_usuario != "Administrador":
            self.btn_admin_users.configure(state="disabled", fg_color="gray")

        # --- MAIN FRAME ---
        self.main_frame = ctk.CTkScrollableFrame(self, label_text="Inventário de Produtos")
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        
        self.carregar_dados()
        self.agendar_atualizacao() # Inicia o timer de 5 segundos

    def agendar_atualizacao(self):
        self.carregar_dados()
        self.after(5000, self.agendar_atualizacao)

    def carregar_dados(self):
        for w in self.main_frame.winfo_children(): w.destroy()
        prods = self.db.listar_produtos()
        ctk.CTkLabel(self.main_frame, text="SKU | Nome | Categoria | Qtd | Status", font=("Arial", 12, "bold")).pack(pady=5)
        for p in prods:
            frame_item = ctk.CTkFrame(self.main_frame, fg_color="transparent")
            frame_item.pack(fill="x", pady=2)
            cor = "white" if p[4] > p[5] else "#FF6666"
            status = "✅ OK" if p[4] > p[5] else "⚠️ BAIXO"
            ctk.CTkLabel(frame_item, text=f"{p[1]} | {p[2]} | {p[3]} | {p[4]} | {status}", text_color=cor, width=500, anchor="w").pack(side="left", padx=5)
            if self.nivel_usuario == "Administrador":
                ctk.CTkButton(frame_item, text="Excluir", width=60, fg_color="red", command=lambda s=p[1]: self.confirmar_exclusao(s)).pack(side="right", padx=5)

    def confirmar_exclusao(self, sku):
        if messagebox.askyesno("Confirmar", f"Deseja excluir o produto {sku}?"):
            if self.db.deletar_produto(sku):
                messagebox.showinfo("Sucesso", "Excluído!"); self.carregar_//dados()

    def janela_cadastro(self):
        self.win = ctk.CTkToplevel(self)
        self.win.geometry("400x350")
        self.win.attributes("-topmost", True)
        ctk.CTkLabel(self.win, text="Nome:").pack(pady=5)
        self.en = ctk.CTkEntry(self.win); self.en.pack()
        ctk.CTkLabel(self.win, text="Categoria:").pack(pady=5)
        self.ec = ctk.CTkEntry(self.win); self.ec.pack()
        ctk.CTkLabel(self.win, text="Mínimo:").pack(pady=5)
        self.em = ctk.CTkEntry(self.win); self.em.pack()
        ctk.CTkButton(self.win, text="Salvar", command=self.salvar).pack(pady=20)

    def salvar(self):
        try:
            s, res = self.db.adicionar_produto(self.en.get(), self.ec.get(), int(self.em.get()), self.usuario_logado)
            if s: messagebox.showinfo("Sucesso", f"SKU: {res}"); self.win.destroy(); self.carregar_dados()
            else: messagebox.showerror("Erro", res)
        except: messagebox.showerror("Erro", "Valor inválido")

    def janela_movimentacao(self):
        self.win = ctk.CTkToplevel(self)
        self.win.geometry("400x500")
        self.win.attributes("-topmost", True)
        ctk.CTkLabel(self.win, text="Busque o Produto:").pack(pady=5)
        self.ent_sku = ctk.CTkEntry(self.win, width=300); self.ent_sku.pack(pady=5)
        self.ent_sku.bind("<KeyRelease>", self.atualizar_sugestoes)
        self.frame_sug = ctk.CTkFrame(self.win, fg_color="transparent"); self.frame_sug.pack()
        ctk.CTkLabel(self.win, text="Quantidade:").pack(pady=5)
        self.ent_q = ctk.CTkEntry(self.win); self.ent_q.pack()
        ctk.CTkLabel(self.win, text="Usuário:").pack(pady=5)
        self.ent_u = ctk.CTkEntry(self.win); self.ent_u.pack()
        bf = ctk.CTkFrame(self.win); bf.pack(pady=20)
        ctk.CTkButton(bf, text="ENTRADA", fg_color="green", command=lambda: self.processar("ENTRADA")).pack(side="left", padx=10)
        ctk.CTkButton(bf, text="SAÍDA", fg_color="red", command=lambda: self.processar("SAIDA")).pack(side="left", padx=10)

    def atualizar_sugestoes(self, e):
        for w in self.frame_sug.winfo_children(): w.destroy()
        txt = self.ent_sku.get()
        if len(txt) < 2: return
        res = self.db.buscar_produtos_por_texto(txt)
        for s, n in res[:5]:
            ctk.CTkButton(self.frame_sug, text=f"{s} - {n}", fg_color="#3b3b3b", anchor="w", 
                          command=lambda sku=s: self.selecionar(sku)).pack(fill="x", pady=1)

    def selecionar(self, s):
        self.ent_sku.delete(0, 'end'); self.ent_sku.insert(0, s)
        for w in self.frame_sug.winfo_children(): w.destroy()

    def processar(self, t):
        try:
            q = int(self.ent_q.get())
            if q <= 0: return
            s, m = self.db.registrar_movimentacao(self.ent_sku.get(), t, q, self.usuario_logado)
            if s: messagebox.showinfo("Sucesso", m); self.win.destroy(); self.carregar_dados()
            else: messagebox.showerror("Erro", m)
        except: messagebox.showerror("Erro", "Valor inválido")

    def janela_usuarios(self):
        self.win_u = ctk.CTkToplevel(self)
        self.win_u.title("Gerenciar Operadores")
        self.win_u.geometry("400x300")
        self.win_u.attributes("-topmost", True)
        ctk.CTkLabel(self.win_u, text="Novo Usuário:").pack(pady=5)
        self.u_user = ctk.CTkEntry(self.win_u, placeholder_text="Login"); self.u_user.pack()
        self.u_pass = ctk.CTkEntry(self.win_u, placeholder_text="Senha", show="*"); self.u_pass.pack()
        self.u_nivel = ctk.CTkOptionMenu(self.win_u, values=["Operador", "Administrador"])
        self.u_nivel.pack(pady=10)
        ctk.CTkButton(self.win_u, text="Cadastrar Operador", command=self.salvar_usuario).pack(pady=20)

    def salvar_usuario(self):
        if self.auth.adicionar_usuario(self.u_user.get(), self.u_pass.get(), self.u_nivel.get()):
            messagebox.showinfo("Sucesso", "Usuário cadastrado!"); self.win_u.destroy()
        else: messagebox.showerror("Erro", "Usuário já existe!")

if __name__ == "__main__":
    def start(u, n):
        app = AppEstoque(u, n)
        app.mainloop()
    LoginWindow(on_success=start).mainloop()
