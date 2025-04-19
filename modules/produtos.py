import tkinter as tk
from tkinter import messagebox
from main.bd import conectar  # ✅ Import corrigido

def abrir_tela_cadastro_produto():
    def cadastrar():
        nome = entry_nome.get().strip()
        quantidade = entry_quantidade.get().strip()
        quantidade_minima = entry_minima.get().strip()

        if not nome or not quantidade or not quantidade_minima:
            messagebox.showwarning("Campos obrigatórios", "Preencha todos os campos.")
            return

        if nome.isdigit():
            messagebox.showwarning("Nome inválido", "O nome do produto não pode conter apenas números.")
            return

        if not quantidade.isdigit() or not quantidade_minima.isdigit():
            messagebox.showwarning("Valor inválido", "Quantidade e quantidade mínima devem conter apenas números.")
            return

        if int(quantidade) < 0 or int(quantidade_minima) < 0:
            messagebox.showwarning("Valor inválido", "Os valores devem ser positivos.")
            return

        try:
            conn = conectar()
            cursor = conn.cursor()
            query = """
                INSERT INTO TBL_PRODUTO (nome, quantidade, quantidade_minima)
                VALUES (%s, %s, %s)
            """
            cursor.execute(query, (nome, int(quantidade), int(quantidade_minima)))
            conn.commit()
            conn.close()

            messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")
            janela.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao cadastrar produto: {e}")

    janela = tk.Toplevel()
    janela.title("Cadastrar Produto")
    janela.geometry("450x340")
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

    frame = tk.Frame(janela, padx=30, pady=30, bg="#FFFFFF")
    frame.pack(expand=True)

    lbl_titulo = tk.Label(frame, text="📦 Cadastrar Produto", font=fonte_titulo, bg="#FFFFFF", fg="#333")
    lbl_titulo.pack(pady=(0, 20))

    tk.Label(frame, text="Nome do Produto:", font=fonte_padrao, bg="#FFFFFF", anchor="w").pack(fill="x")
    entry_nome = tk.Entry(frame, font=fonte_padrao, width=35)
    entry_nome.pack(pady=(0, 10))

    tk.Label(frame, text="Quantidade Inicial:", font=fonte_padrao, bg="#FFFFFF", anchor="w").pack(fill="x")
    entry_quantidade = tk.Entry(frame, font=fonte_padrao, width=35)
    entry_quantidade.pack(pady=(0, 10))

    tk.Label(frame, text="Quantidade Mínima:", font=fonte_padrao, bg="#FFFFFF", anchor="w").pack(fill="x")
    entry_minima = tk.Entry(frame, font=fonte_padrao, width=35)
    entry_minima.pack(pady=(0, 20))

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
        width=30,
        command=cadastrar
    )
    btn_cadastrar.pack()

