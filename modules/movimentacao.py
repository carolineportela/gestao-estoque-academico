import tkinter as tk
from tkinter import ttk, messagebox
from main.bd import conectar  # ✅ Import corrigido

def abrir_tela_movimentacao(usuario):
    def carregar_produtos():
        try:
            conn = conectar()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id, nome FROM TBL_PRODUTO")
            produtos = cursor.fetchall()
            conn.close()
            combo_produto['values'] = [f"{p['id']} - {p['nome']}" for p in produtos]
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar produtos: {e}")

    def registrar_movimentacao():
        if not combo_produto.get() or not combo_tipo.get() or not entry_quantidade.get().strip():
            messagebox.showwarning("Campos obrigatórios", "Preencha todos os campos.")
            return

        if not entry_quantidade.get().isdigit():
            messagebox.showwarning("Valor inválido", "A quantidade deve ser um número.")
            return

        quantidade = int(entry_quantidade.get())
        if quantidade <= 0:
            messagebox.showwarning("Valor inválido", "A quantidade deve ser maior que zero.")
            return

        try:
            id_produto = int(combo_produto.get().split(" - ")[0])
            tipo_mov = combo_tipo.get().lower()

            conn = conectar()
            cursor = conn.cursor()

            sinal = "+" if tipo_mov == "entrada" else "-"
            cursor.execute(f"""
                UPDATE TBL_PRODUTO
                SET quantidade = quantidade {sinal} %s
                WHERE id = %s
            """, (quantidade, id_produto))

            cursor.execute("SELECT id FROM TBL_TIPO_MOVIMENTACAO WHERE descricao = %s", (tipo_mov,))
            tipo_id = cursor.fetchone()[0]

            cursor.execute("""
                INSERT INTO TBL_MOVIMENTACAO (quantidade, id_produto, id_usuario, id_tipo_movimentacao)
                VALUES (%s, %s, %s, %s)
            """, (quantidade, id_produto, usuario["id"], tipo_id))

            conn.commit()
            conn.close()

            messagebox.showinfo("Sucesso", f"{tipo_mov.capitalize()} registrada com sucesso!")
            janela.destroy()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao registrar movimentação: {e}")

    janela = tk.Toplevel()
    janela.title("Movimentação de Estoque")
    janela.geometry("450x370")
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

    lbl_titulo = tk.Label(frame, text="🔄 Movimentar Estoque", font=fonte_titulo, bg="#FFFFFF", fg="#333")
    lbl_titulo.pack(pady=(0, 20))

    tk.Label(frame, text="Produto:", font=fonte_padrao, bg="#FFFFFF", anchor="w").pack(fill="x")
    combo_produto = ttk.Combobox(frame, font=fonte_padrao, width=35)
    combo_produto.pack(pady=(0, 10))

    tk.Label(frame, text="Tipo de Movimentação:", font=fonte_padrao, bg="#FFFFFF", anchor="w").pack(fill="x")
    combo_tipo = ttk.Combobox(frame, font=fonte_padrao, values=["Entrada", "Saída"], state="readonly", width=35)
    combo_tipo.pack(pady=(0, 10))

    tk.Label(frame, text="Quantidade:", font=fonte_padrao, bg="#FFFFFF", anchor="w").pack(fill="x")
    entry_quantidade = tk.Entry(frame, font=fonte_padrao, width=38)
    entry_quantidade.pack(pady=(0, 20))
    
    btn_salvar = tk.Button(
        frame,
        text="Registrar",
        font=fonte_padrao,
        bg="#4CAF50",
        fg="white",
        activebackground="#45A049",
        relief="flat",
        padx=10,
        pady=6,
        width=30,
        command=registrar_movimentacao
    )
    btn_salvar.pack()

    carregar_produtos()

