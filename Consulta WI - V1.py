# Importa as bibliotecas utilizadas
import re
import os
import pyodbc

# Estabelece uma conexão com o banco de dados usando um DSN específico
cnxn = pyodbc.connect('DSN=DatalakeLLAP', autocommit=True)

# Cria um cursor para executar consultas SQL na conexão
cursor = cnxn.cursor()

# Padrões do CNPJ, Nome e Código do BNDES
padrao_cnpj = r'^\d{14}$'  # CNPJ com 14 dígitos
padrao_nome = r'^[A-Za-z\s]+$'  # Apenas letras e espaços são permitidos
padrao_codigo_bndes = r'^\d{6,8}$'  # BNDES com 6 a 8 dígitos

# Função para Limpar Tela
def limpar_tela():
    if os.name == 'nt':  # Verifica se o sistema operacional é Windows
        os.system('cls')
    else:  # Para sistemas Unix/Linux
        os.system('clear')

# Função para consultar dados
def consultar_dados():
    # Dados digitados pelo usuário
    dados = ['- CNPJ', '- Nome', '- Codigo BNDES']
    print("\nPesquise com os seguintes Dados:")
    for x in dados:
        print(x)
    dado = input('Digite o Dado que deseja Consultar: ')

    # Limpar a tela
    limpar_tela()

    # Verifica o tipo de dado usando
    if re.match(padrao_cnpj, dado):
        print(f"\nVocê digitou um CNPJ. ({dado}) \nResultado:")
        # Executa uma consulta SQL para selecionar os dados que tenham o CNPJ digitado pelo usuario
        cursor.execute(f"select cod_bndes, nome, cpf_cnpj, id_categoria, nome_categoria from rich_entidades.vi_n02_entidade where cpf_cnpj = '{dado}'")
    elif re.match(padrao_nome, dado):
        print(f"\nVocê digitou um Nome. ({dado}) \nResultado:")
        # Executa uma consulta SQL para selecionar os dados que tenham o Nome digitado pelo usuario
        cursor.execute(f"select cod_bndes, nome, cpf_cnpj, id_categoria, nome_categoria from rich_entidades.vi_n02_entidade where nome LIKE '%{dado}%'")
    elif re.match(padrao_codigo_bndes, dado):
        print(f"\nVocê digitou um Código do BNDES. ({dado}) \nResultado:")
        # Executa uma consulta SQL para selecionar os dados que tenham o Codigo BNDES digitado pelo usuario
        cursor.execute(f"select cod_bndes, nome, cpf_cnpj, id_categoria, nome_categoria from rich_entidades.vi_n02_entidade where cod_bndes = '{dado}'")
    else:
        print("\nDado não reconhecido.")

    # Obtém a primeira linha resultante da consulta
    row = cursor.fetchone()

    # Verifica se uma linha foi retornada pela consulta
    if row:
        # Imprime a linha resultante
        print(row)

# Loop principal
while True:
    consultar_dados()

    # Pergunta ao usuário se deseja fazer outra consulta ou sair
    resposta = input('\nDeseja fazer outra consulta? (S/N): ')

    # Se a resposta não for 'S' ou 's', sai do loop
    if resposta.lower() != 's':
        break

    limpar_tela()
