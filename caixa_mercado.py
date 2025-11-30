import tkinter as tk
from tkinter import ttk
# Note que eu removi o 'from tkinter import messagebox' porque não vamos mais usar!
import sqlite3

# --- BANCO DE DADOS ---
def configurar_banco():
    conexao = sqlite3.connect("loja.db")
    cursor = conexao.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        preco REAL NOT NULL
    )
    """)
    conexao.commit()
    conexao.close()

# --- FUNÇÃO: CADASTRAR (COM FEEDBACK NA TELA) ---
def cadastrar_produto():
    nome = entry_cad_nome.get()
    preco = entry_cad_preco.get()

    # Validação simples
    if nome == "" or preco == "":
        # Configura o Label de aviso para VERMELHO
        lbl_status.config(text="❌ Erro: Preencha nome e preço!", fg="red")
        return

    try:
        conexao = sqlite3.connect("loja.db")
        cursor = conexao.cursor()
        
        cursor.execute("INSERT INTO produtos (nome, preco) VALUES (?, ?)", (nome, float(preco)))
        id_gerado = cursor.lastrowid
        
        conexao.commit()
        conexao.close()
        
        # SUCESSO: Configura o Label de aviso para VERDE
        msg = f"✅ Sucesso! '{nome}' cadastrado.\nO código é: {id_gerado}"
        lbl_status.config(text=msg, fg="green")
        
        # Limpa os campos e joga o foco (cursor) de volta pro nome
        # Assim você já pode digitar o próximo sem usar o mouse!
        entry_cad_nome.delete(0, tk.END)
        entry_cad_preco.delete(0, tk.END)
        entry_cad_nome.focus()
        
    except ValueError:
        lbl_status.config(text="❌ Erro: O preço deve ser número (ex: 10.50)", fg="red")

# --- FUNÇÃO: BUSCAR ---
def buscar_preco():
    cod = entry_busca_codigo.get()
    
    conexao = sqlite3.connect("loja.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT nome, preco FROM produtos WHERE id = ?", (cod,))
    resultado = cursor.fetchone()
    conexao.close()
    
    if resultado:
        lbl_resultado_nome.config(text=resultado[0], fg="blue")
        lbl_resultado_preco.config(text=f"R$ {resultado[1]:.2f}")
    else:
        lbl_resultado_nome.config(text="Não encontrado", fg="red")
        lbl_resultado_preco.config(text="R$ 0.00")

# --- INTERFACE GRÁFICA ---
configurar_banco()

janela = tk.Tk()
janela.title("Mercadinho - Feedback Rápido")
janela.geometry("500x450") # Aumentei um pouquinho a altura

notebook = ttk.Notebook(janela)
notebook.pack(fill="both", expand=True)

# --- ABA 1: CAIXA ---
aba_caixa = tk.Frame(notebook)
notebook.add(aba_caixa, text="  CAIXA  ")

tk.Label(aba_caixa, text="Digite o Código do Produto:", font=("Arial", 12)).pack(pady=10)
entry_busca_codigo = tk.Entry(aba_caixa, font=("Arial", 14))
entry_busca_codigo.pack(pady=5)
tk.Button(aba_caixa, text="Consultar Preço", font=("Arial", 12), command=buscar_preco).pack(pady=10)

lbl_resultado_nome = tk.Label(aba_caixa, text="...", font=("Arial", 18, "bold"))
lbl_resultado_nome.pack(pady=10)
lbl_resultado_preco = tk.Label(aba_caixa, text="R$ 0.00", font=("Arial", 25, "bold"), fg="green")
lbl_resultado_preco.pack(pady=5)

# --- ABA 2: CADASTRO ---
aba_estoque = tk.Frame(notebook, bg="#f0f0f0")
notebook.add(aba_estoque, text="  NOVO PRODUTO  ")

tk.Label(aba_estoque, text="Nome do Produto:", bg="#f0f0f0").pack(pady=(20, 5))
entry_cad_nome = tk.Entry(aba_estoque, width=30)
entry_cad_nome.pack()

tk.Label(aba_estoque, text="Preço:", bg="#f0f0f0").pack(pady=5)
entry_cad_preco = tk.Entry(aba_estoque, width=10)
entry_cad_preco.pack()

tk.Button(aba_estoque, text="CADASTRAR", bg="#4CAF50", fg="white", 
          font=("Arial", 10, "bold"), command=cadastrar_produto).pack(pady=20)

# --- NOVIDADE: A BARRA DE STATUS ---
# Ela começa com texto vazio "" para não atrapalhar
lbl_status = tk.Label(aba_estoque, text="", font=("Arial", 12, "bold"), bg="#f0f0f0")
lbl_status.pack(pady=10)

janela.mainloop()