import tkinter as tk

def abrir_tela_sobre(janela_anterior=None):
    if janela_anterior:
        janela_anterior.withdraw()

    janela = tk.Toplevel()
    janela.title("Sobre o Sistema")
    janela.geometry("520x350") 
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

    tk.Label(frame, text="ℹ️ Sobre o Sistema", font=fonte_titulo, bg="#FFFFFF", fg="#333").pack(pady=(0, 20))

    infos = [
        "📦 Sistema: Controle de Estoque",
        "🧾 Versão: 1.0",
        "👩 Desenvolvido por: Carol Portela",
        "🛠️ Tecnologias: Python, Tkinter, MySQL",
        "📅 Projeto acadêmico - 18/04/2025"
    ]

    for info in infos:
        tk.Label(frame, text=info, font=fonte_padrao, bg="#FFFFFF", anchor="w").pack(anchor="w", pady=2)

    def fechar():
        janela.destroy()
        if janela_anterior:
            janela_anterior.deiconify()

    tk.Button(
        frame,
        text="❌ Fechar Janela",
        font=("Segoe UI", 13, "bold"),
        bg="#d9534f",
        fg="white",
        activebackground="#c9302c",
        relief="flat",
        padx=15,
        pady=10,
        width=25,
        command=fechar
    ).pack(pady=(40, 0))

