import tkinter as tk

janela = tk.Tk()
janela.title("Meu Primeiro Caixa")
janela.geometry("600x400")

rotulo = tk.Label(janela, text="Digite o código do produto:", font=("Arial", 14))
rotulo.pack(pady=20)

campo_codigo = tk.Entry(janela, font=("Arial", 14))
campo_codigo.pack(pady=10)

botao = tk.Button(janela, text="Buscar Preço", font=("Arial", 12))
botao.pack(pady=20)

janela.mainloop()