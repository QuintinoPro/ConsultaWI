import pyodbc

import requests
from tkinter import *

# Função para executar a consulta com base no nome inserido pelo usuário
def executar_consulta():
    nome_pesquisa = entrada_nome.get()
    consulta_sql = f"SELECT * FROM pessoa WHERE nome LIKE '{nome_pesquisa}%'"

    cursor.execute(consulta_sql)

    results = cursor.fetchall()

    # Limpar a lista de resultados antes de exibir novos resultados
    lista_resultados.delete(0, END)

    for linha in results:
        lista_resultados.insert(END, linha)

# Conectar ao banco de dados MySQL
con = mysql.connector.connect(host='localhost', database='consultasqlpy', username='root', password='')

if con.is_connected():
    db_info = con.get_server_info()
    print("Conectado ao Servidor MySQL versão ", db_info)

    cursor = con.cursor()

# Interface gráfica usando Tkinter
janela = Tk()
janela.title("Consulta PY")

textohome = Label(janela, text="Consulta no Banco de Dados Utilizando Python!")
textohome.grid(column=0, row=0, padx=20, pady=20)

# Cria uma entrada de texto para o usuário inserir o nome
entrada_nome = Entry(janela, width=30)
entrada_nome.grid(column=0, row=1, padx=20)

# Botão para executar a consulta
botao_consultar = Button(janela, text="Consultar", command=executar_consulta)
botao_consultar.grid(column=1, row=1)

# Lista para exibir os resultados
lista_resultados = Listbox(janela, width=50, height=10)
lista_resultados.grid(column=0, row=2, columnspan=2, padx=20, pady=10)

janela.mainloop()

# Fechar a conexão com o banco de dados quando a janela Tkinter for fechada
con.close()

