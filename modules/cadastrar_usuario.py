import tkinter as tk
from tkinter import ttk, messagebox
from main.bd import conectar  # ✅ Import corrigido
import bcrypt

def abrir_tela_cadastro_usuario():
    def cadastrar():
        nome = entry_usuario.get().strip()
        senha = entry_senha.get().strip()
        tipo = combo_tipo.get().strip()

        if not nome or not senha or not tipo:
            messagebox.showwarning("Campos obrigatórios", "Preencha todos os campos.")
            return

        if nome.isdigit():
            messagebox.showwarning("Nome inválido", "O nome de usuário não pode conter apenas números.")
            return

        if len(senha) < 4:
            messagebox.showwarning("Senha fraca", "A senha deve ter pelo menos 4 caracteres.")
            return

        try:
            conn = conectar()
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM TBL_USUARIO WHERE nome_usuario = %s", (nome,))
            if cursor.fetchone()[0] > 0:
                messagebox.showerror("Erro", "Nome de usuário já existe.")
                conn.close()
                return

            cursor.execute("SELECT id FROM TBL_TIPO_USUARIO WHERE descricao = %s", (tipo.lower(),))
            tipo_id = cursor.fetchone()[0]

            senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())

            cursor.execute("""
                INSERT INTO TBL_USUARIO (nome_usuario, senha, id_tipo_usuario)
                VALUES (%s, %s, %s)
            """, (nome, senha_hash, tipo_id))
            conn.commit()
            conn.close()

            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
            janela.destroy()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao cadastrar usuário: {e}")

    janela = tk.Toplevel()
    janela.title("Cadastrar Novo Usuário")
    janela.geometry("450x350")
    janela.configure(bg="#F9F9F9")
    janela.resizable(False, False)

    janela.update_idletasks()
    largura = janela.winfo_width()
    altura = janela.winfo_height()
    x = (janela.winfo_screenwidth() // 2) - (largura // 2)
    y = (janela.winfo_screenheight() // 2) - (altura // 2)
    janela.geometry(f"+{x}+{y}")

    fonte_titulo = ("Segoe UI", 15, "bold")
    fonte_padrao = ("Segoe UI", 12)

    frame = tk.Frame(janela, bg="#FFFFFF", padx=30, pady=30)
    frame.pack(expand=True)

    lbl_titulo = tk.Label(frame, text="👤 Cadastro de Usuário", font=fonte_titulo, bg="#FFFFFF", fg="#333")
    lbl_titulo.pack(pady=(0, 20))

    tk.Label(frame, text="Nome de Usuário:", font=fonte_padrao, bg="#FFFFFF", anchor="w").pack(fill="x")
    entry_usuario = tk.Entry(frame, font=fonte_padrao, width=30)
    entry_usuario.pack(pady=(0, 10))

    tk.Label(frame, text="Senha:", font=fonte_padrao, bg="#FFFFFF", anchor="w").pack(fill="x")
    entry_senha = tk.Entry(frame, show="*", font=fonte_padrao, width=30)
    entry_senha.pack(pady=(0, 10))

    tk.Label(frame, text="Tipo de Usuário:", font=fonte_padrao, bg="#FFFFFF", anchor="w").pack(fill="x")
    combo_tipo = ttk.Combobox(frame, font=fonte_padrao, values=["administrador", "comum"], state="readonly", width=28)
    combo_tipo.pack(pady=(0, 20))

    btn_cadastrar = tk.Button(
        frame,
        text="Cadastrar",
        font=fonte_padrao,
        bg="#4CAF50",
        fg="white",
        activebackground="#45A049",
        relief="flat",
        padx=10,
        pady=6,
        width=25,
        command=cadastrar
    )
    btn_cadastrar.pack()

