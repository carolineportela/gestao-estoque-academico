import tkinter as tk
from tkinter import messagebox
from modules.produtos import abrir_tela_cadastro_produto
from modules.movimentacao import abrir_tela_movimentacao
from modules.visualizar_produtos import abrir_tela_visualizar_produtos
from modules.cadastrar_usuario import abrir_tela_cadastro_usuario
from modules.historico import abrir_tela_historico_movimentacoes
from modules.sobre import abrir_tela_sobre

def abrir_dashboard(usuario):
    janela = tk.Tk()
    janela.title("Menu Principal")
    janela.geometry("500x500")
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

    frame = tk.Frame(janela, padx=30, pady=30, bg="#FFFFFF")
    frame.pack(expand=True)

    lbl_boas_vindas = tk.Label(
        frame,
        text=f"📋 Olá, {usuario['nome_usuario']} ({usuario['perfil']})",
        font=fonte_titulo,
        bg="#FFFFFF",
        fg="#333"
    )
    lbl_boas_vindas.pack(pady=(0, 30))

    def criar_botao(texto, comando, cor="#4CAF50"):
        return tk.Button(
            frame,
            text=texto,
            font=fonte_padrao,
            bg=cor,
            fg="white",
            activebackground="#45A049" if cor == "#4CAF50" else "#c9302c",
            relief="flat",
            padx=10,
            pady=6,
            width=30,
            command=comando
        )

    criar_botao("➕ Cadastrar Produto", abrir_tela_cadastro_produto).pack(pady=5)
    criar_botao("📊 Visualizar Produtos", abrir_tela_visualizar_produtos).pack(pady=5)
    criar_botao("📦 Movimentar Estoque", lambda: abrir_tela_movimentacao(usuario)).pack(pady=5)
    criar_botao("📜 Ver Histórico de Movimentações", abrir_tela_historico_movimentacoes).pack(pady=5)

    if usuario["perfil"] == "administrador":
        criar_botao("👤 Cadastrar Novo Usuário", abrir_tela_cadastro_usuario).pack(pady=5)

    criar_botao("ℹ️ Sobre o Sistema", lambda: abrir_tela_sobre(janela)).pack(pady=5)
    criar_botao("🚪 Sair", janela.destroy, cor="#d9534f").pack(pady=(10, 0))

    janela.mainloop()
