import tkinter as tk
from tkinter import ttk, messagebox
from main.bd import conectar 

def abrir_tela_visualizar_produtos():
    def carregar_produtos(filtro=""):
        try:
            tree.delete(*tree.get_children())

            conn = conectar()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT nome, quantidade, quantidade_minima FROM TBL_PRODUTO")
            produtos = cursor.fetchall()
            conn.close()

            alertas = 0
            for prod in produtos:
                if filtro.lower() in prod["nome"].lower():
                    cor = "red" if prod["quantidade"] < prod["quantidade_minima"] else "black"
                    if cor == "red":
                        alertas += 1
                    tree.insert("", "end", values=(prod["nome"], prod["quantidade"], prod["quantidade_minima"]), tags=(cor,))

            texto_alerta = f"⚠️ Produtos abaixo do mínimo: {alertas}" if alertas > 0 else "✅ Nenhum produto abaixo do mínimo"
            lbl_alerta.config(text=texto_alerta, fg="red" if alertas > 0 else "green")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar produtos: {e}")

    def aplicar_filtro():
        filtro = entry_busca.get().strip()
        carregar_produtos(filtro)

    janela = tk.Toplevel()
    janela.title("Visualizar Produtos")
    janela.geometry("600x460")
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

    frame = tk.Frame(janela, padx=30, pady=20, bg="#FFFFFF")
    frame.pack(expand=True, fill="both")

    lbl_titulo = tk.Label(frame, text="📊 Lista de Produtos", font=fonte_titulo, bg="#FFFFFF", fg="#333")
    lbl_titulo.pack(pady=(0, 10))

    filtro_frame = tk.Frame(frame, bg="#FFFFFF")
    filtro_frame.pack(pady=(0, 10))

    entry_busca = tk.Entry(filtro_frame, font=fonte_padrao, width=30)
    entry_busca.pack(side="left", padx=(0, 10))

    btn_buscar = tk.Button(
        filtro_frame,
        text="Buscar",
        font=fonte_padrao,
        bg="#4CAF50",
        fg="white",
        activebackground="#45A049",
        relief="flat",
        padx=10,
        command=aplicar_filtro
    )
    btn_buscar.pack(side="left")

    lbl_alerta = tk.Label(frame, text="", font=fonte_padrao, bg="#FFFFFF")
    lbl_alerta.pack(pady=(0, 10))

    colunas = ("nome", "quantidade", "quantidade_minima")
    tree = ttk.Treeview(frame, columns=colunas, show="headings", height=12)

    tree.heading("nome", text="Produto")
    tree.heading("quantidade", text="Qtd Atual")
    tree.heading("quantidade_minima", text="Qtd Mínima")

    tree.column("nome", width=240)
    tree.column("quantidade", width=120, anchor="center")
    tree.column("quantidade_minima", width=120, anchor="center")

    tree.tag_configure("red", foreground="red")
    tree.tag_configure("black", foreground="black")

    tree.pack(padx=10, pady=10, fill="x")

    carregar_produtos()
