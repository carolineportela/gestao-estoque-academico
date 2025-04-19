import tkinter as tk
from tkinter import messagebox
from main.bd import conectar 
from main.dashboard import abrir_dashboard  
import bcrypt

def verificar_login(nome_usuario, senha):
    try:
        conn = conectar()
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT u.id, u.nome_usuario, u.senha, t.descricao AS perfil
            FROM TBL_USUARIO u
            JOIN TBL_TIPO_USUARIO t ON u.id_tipo_usuario = t.id
            WHERE u.nome_usuario = %s
        """
        cursor.execute(query, (nome_usuario,))
        usuario = cursor.fetchone()
        conn.close()

        if usuario and bcrypt.checkpw(senha.encode('utf-8'), usuario["senha"].encode('utf-8')):
            return usuario
    except Exception as e:
        messagebox.showerror("Erro de conexão", f"Ocorreu um erro ao conectar ao banco: {e}")
    return None

def abrir_login():
    def realizar_login():
        usuario = verificar_login(entry_usuario.get(), entry_senha.get())
        if usuario:
            messagebox.showinfo("Login realizado", f"Bem-vindo, {usuario['nome_usuario']} ({usuario['perfil']})")
            janela.destroy()
            abrir_dashboard(usuario)
        else:
            messagebox.showerror("Erro de login", "Usuário ou senha inválidos.")

    janela = tk.Tk()
    janela.title("Login - Controle de Estoque")
    janela.geometry("420x300")
    janela.configure(bg="#F9F9F9")
    janela.resizable(False, False)

    janela.update_idletasks()
    largura = janela.winfo_width()
    altura = janela.winfo_height()
    x = (janela.winfo_screenwidth() // 2) - (largura // 2)
    y = (janela.winfo_screenheight() // 2) - (altura // 2)
    janela.geometry(f"+{x}+{y}")

    fonte_titulo = ("Segoe UI", 16, "bold")
    fonte_padrao = ("Segoe UI", 12)

    frame = tk.Frame(janela, bg="#FFFFFF", padx=30, pady=30)
    frame.pack(expand=True)

    lbl_titulo = tk.Label(frame, text="🔐 Acesso ao Sistema", font=fonte_titulo, bg="#FFFFFF", fg="#333")
    lbl_titulo.pack(pady=(0, 20))

    lbl_usuario = tk.Label(frame, text="Usuário:", font=fonte_padrao, bg="#FFFFFF", anchor="w")
    lbl_usuario.pack(fill="x")
    entry_usuario = tk.Entry(frame, font=fonte_padrao, width=30)
    entry_usuario.pack(pady=(0, 10))

    lbl_senha = tk.Label(frame, text="Senha:", font=fonte_padrao, bg="#FFFFFF", anchor="w")
    lbl_senha.pack(fill="x")
    entry_senha = tk.Entry(frame, show="*", font=fonte_padrao, width=30)
    entry_senha.pack(pady=(0, 20))

    btn_login = tk.Button(
        frame,
        text="Entrar",
        font=fonte_padrao,
        bg="#4CAF50",
        fg="white",
        activebackground="#45A049",
        relief="flat",
        padx=10,
        pady=6,
        width=25,
        command=realizar_login
    )
    btn_login.pack()

    janela.mainloop()
