import tkinter as tk
from tkinter import ttk, messagebox
from main.bd import conectar  # ✅ Import corrigido
from datetime import datetime

def abrir_tela_historico_movimentacoes():
    def carregar_historico():
        try:
            conn = conectar()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT 
                    m.quantidade,
                    m.data_movimentacao,
                    p.nome AS produto,
                    t.descricao AS tipo,
                    u.nome_usuario AS usuario
                FROM TBL_MOVIMENTACAO m
                JOIN TBL_PRODUTO p ON p.id = m.id_produto
                JOIN TBL_TIPO_MOVIMENTACAO t ON t.id = m.id_tipo_movimentacao
                JOIN TBL_USUARIO u ON u.id = m.id_usuario
                ORDER BY m.data_movimentacao DESC
            """)
            movimentacoes = cursor.fetchall()
            conn.close()

            for mov in movimentacoes:
                data_formatada = datetime.strptime(str(mov["data_movimentacao"]), "%Y-%m-%d %H:%M:%S")
                data_str = data_formatada.strftime("%d/%m/%Y %H:%M")
                tree.insert("", "end", values=(
                    mov["produto"],
                    mov["tipo"].capitalize(),
                    mov["quantidade"],
                    mov["usuario"],
                    data_str
                ))

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar histórico: {e}")

    janela = tk.Toplevel()
    janela.title("Histórico de Movimentações")
    janela.geometry("720x440")
    janela.configure(bg="#F9F9F9")
    janela.resizable(False, False)

    # Centralizar
    janela.update_idletasks()
    largura = janela.winfo_width()
    altura = janela.winfo_height()
    x = (janela.winfo_screenwidth() // 2) - (largura // 2)
    y = (janela.winfo_screenheight() // 2) - (altura // 2)
    janela.geometry(f"+{x}+{y}")

    fonte_titulo = ("Segoe UI", 15, "bold")
    fonte_padrao = ("Segoe UI", 12)

    frame = tk.Frame(janela, padx=30, pady=20, bg="#FFFFFF")
    frame.pack(expand=True, fill="both")

    lbl_titulo = tk.Label(frame, text="📜 Histórico de Movimentações", font=fonte_titulo, bg="#FFFFFF", fg="#333")
    lbl_titulo.pack(pady=(0, 15))

    colunas = ("produto", "tipo", "quantidade", "usuario", "data")
    tree = ttk.Treeview(frame, columns=colunas, show="headings", height=15)

    tree.heading("produto", text="Produto")
    tree.heading("tipo", text="Tipo")
    tree.heading("quantidade", text="Qtd")
    tree.heading("usuario", text="Usuário")
    tree.heading("data", text="Data")

    tree.column("produto", width=200)
    tree.column("tipo", width=80, anchor="center")
    tree.column("quantidade", width=80, anchor="center")
    tree.column("usuario", width=140, anchor="center")
    tree.column("data", width=150, anchor="center")

    tree.pack(padx=10, pady=10, fill="x")

    carregar_historico()
