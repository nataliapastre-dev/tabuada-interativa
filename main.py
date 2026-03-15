# main.py
import tkinter as tk
from tkinter import ttk, colorchooser, messagebox, filedialog
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Lista global para exportação
tabela = []

# Variáveis de cores padrão
cor_par = "#cce5ff"    # azul claro
cor_impar = "#d4edda"  # verde claro

def escolher_cor_par():
    global cor_par
    cor = colorchooser.askcolor(title="Escolha a cor para números pares")[1]
    if cor:
        cor_par = cor

def escolher_cor_impar():
    global cor_impar
    cor = colorchooser.askcolor(title="Escolha a cor para números ímpares")[1]
    if cor:
        cor_impar = cor

def gerar_tabuada():
    try:
        inicio = int(entry_inicio.get())
        fim = int(entry_fim.get())
        mult_inicio = int(entry_mult_inicio.get())
        mult_fim = int(entry_mult_fim.get())
    except ValueError:
        messagebox.showerror("Erro", "Digite números válidos!")
        return

    # Limpar tabela anterior
    for item in tree.get_children():
        tree.delete(item)
    global tabela
    tabela = []

    for i in range(inicio, fim + 1):
        for j in range(mult_inicio, mult_fim + 1):
            resultado = i * j
            tabela.append([i, j, resultado])
            tag = "par" if resultado % 2 == 0 else "impar"
            tree.insert("", tk.END, values=(i, j, resultado), tags=(tag,))
    
    tree.tag_configure("par", background=cor_par)
    tree.tag_configure("impar", background=cor_impar)

def exportar_excel():
    if not tabela:
        messagebox.showwarning("Aviso", "Gere a tabuada antes de exportar!")
        return
    caminho = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                           filetypes=[("Excel files","*.xlsx")])
    if caminho:
        df = pd.DataFrame(tabela, columns=["Número","Multiplicador","Resultado"])
        df.to_excel(caminho, index=False)
        messagebox.showinfo("Sucesso", f"Arquivo Excel salvo em:\n{caminho}")

def exportar_pdf():
    if not tabela:
        messagebox.showwarning("Aviso", "Gere a tabuada antes de exportar!")
        return
    caminho = filedialog.asksaveasfilename(defaultextension=".pdf",
                                           filetypes=[("PDF files","*.pdf")])
    if caminho:
        c = canvas.Canvas(caminho, pagesize=letter)
        largura, altura = letter
        y = altura - 50
        c.setFont("Helvetica", 12)
        for i, j, resultado in tabela:
            cor = (0,0,1) if resultado %2 ==0 else (0,0.5,0)
            c.setFillColorRGB(*cor)
            c.drawString(50, y, f"{i} x {j} = {resultado}")
            y -= 15
            if y < 50:
                c.showPage()
                c.setFont("Helvetica",12)
                y = altura - 50
        c.save()
        messagebox.showinfo("Sucesso", f"Arquivo PDF salvo em:\n{caminho}")

# Janela principal
root = tk.Tk()
root.title("Tabuada Interativa Avançada")
root.geometry("600x500")
root.configure(bg="#f5f5f5")

# Frame superior para entradas e botões
frame_top = ttk.Frame(root, padding=10)
frame_top.pack(fill="x")

# Entradas
ttk.Label(frame_top, text="Número início:").grid(row=0, column=0, padx=5)
entry_inicio = ttk.Entry(frame_top, width=5)
entry_inicio.grid(row=0, column=1, padx=5)

ttk.Label(frame_top, text="Número fim:").grid(row=0, column=2, padx=5)
entry_fim = ttk.Entry(frame_top, width=5)
entry_fim.grid(row=0, column=3, padx=5)

ttk.Label(frame_top, text="Multiplicador início:").grid(row=1, column=0, padx=5)
entry_mult_inicio = ttk.Entry(frame_top, width=5)
entry_mult_inicio.grid(row=1, column=1, padx=5)

ttk.Label(frame_top, text="Multiplicador fim:").grid(row=1, column=2, padx=5)
entry_mult_fim = ttk.Entry(frame_top, width=5)
entry_mult_fim.grid(row=1, column=3, padx=5)

# Botões principais
ttk.Button(frame_top, text="Gerar Tabuada", command=gerar_tabuada).grid(row=0, column=4, padx=10)
ttk.Button(frame_top, text="Exportar Excel", command=exportar_excel).grid(row=1, column=4, padx=10)
ttk.Button(frame_top, text="Exportar PDF", command=exportar_pdf).grid(row=1, column=5, padx=10)

# Botões para escolher cores
ttk.Button(frame_top, text="Cor Pares", command=escolher_cor_par).grid(row=0, column=5, padx=10)
ttk.Button(frame_top, text="Cor Ímpares", command=escolher_cor_impar).grid(row=0, column=6, padx=10)

# Treeview com scroll
tree_frame = ttk.Frame(root)
tree_frame.pack(padx=10, pady=10, fill="both", expand=True)

scrollbar = ttk.Scrollbar(tree_frame)
scrollbar.pack(side="right", fill="y")

tree = ttk.Treeview(tree_frame, columns=("Número","Multiplicador","Resultado"), show="headings", yscrollcommand=scrollbar.set)
tree.heading("Número", text="Número")
tree.heading("Multiplicador", text="Multiplicador")
tree.heading("Resultado", text="Resultado")
tree.column("Número", width=80, anchor="center")
tree.column("Multiplicador", width=100, anchor="center")
tree.column("Resultado", width=80, anchor="center")
tree.pack(fill="both", expand=True)
scrollbar.config(command=tree.yview)

root.mainloop()