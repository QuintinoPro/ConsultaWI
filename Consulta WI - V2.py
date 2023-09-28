import sys
import re
import pyodbc
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton

# Estabelece uma conexão com o banco de dados usando um DSN específico
cnxn = pyodbc.connect('DSN=DatalakeLLAP', autocommit=True)
cursor = cnxn.cursor()

# Padrões do CNPJ, Nome e Código do BNDES
padrao_cnpj = r'^\d{14}$'  # CNPJ com 14 dígitos
padrao_nome = r'^[A-Za-z\s]+$'  # Apenas letras e espaços são permitidos
padrao_codigo_bndes = r'^\d{6,8}$'  # BNDES com 6 a 8 dígitos


# Função para consultar dados
def consultar_dados():
    dado = input_text.text()

    # Limpa o campo de resultados
    result_label.setText("")

    # Verifica o tipo de dado usando
    if re.match(padrao_cnpj, dado):
        cursor.execute(
            f"select cod_bndes, nome, cpf_cnpj, id_categoria, nome_categoria from rich_entidades.vi_n02_entidade where cpf_cnpj = '{dado}'")
    elif re.match(padrao_nome, dado):
        cursor.execute(
            f"select cod_bndes, nome, cpf_cnpj, id_categoria, nome_categoria from rich_entidades.vi_n02_entidade where nome LIKE '%{dado}%'")
    elif re.match(padrao_codigo_bndes, dado):
        cursor.execute(
            f"select cod_bndes, nome, cpf_cnpj, id_categoria, nome_categoria from rich_entidades.vi_n02_entidade where cod_bndes = '{dado}'")
    else:
        result_label.setText("Dado não reconhecido.")
        return

    rows = cursor.fetchall()
    if rows:
        for row in rows:
            formatted_data = [f"{label}: {value}" for label, value in
                              zip(['Código BNDES', 'Nome', 'CPF/CNPJ', 'ID Categoria', 'Nome Categoria'], row)]
            result_label.setText(result_label.text() + "\n".join(formatted_data) + "\n\n")
    else:
        result_label.setText("Nenhum resultado encontrado.")


# Função para limpar o campo de entrada de texto
def clear_input_text():
    input_text.clear()
    result_label.setText("")


# Cria a aplicação Qt
app = QApplication(sys.argv)

# Cria a janela principal
window = QWidget()
window.setWindowTitle('Consulta de Dados')
window.setGeometry(100, 100, 800, 400)

# Layout da janela
layout = QVBoxLayout()

# Adiciona um rótulo (label) com texto estático
label = QLabel("Digite o Dado que deseja Consultar:")
layout.addWidget(label)

# Campo de entrada de texto
input_text = QLineEdit()
layout.addWidget(input_text)

# Botões de consulta e limpeza
query_button = QPushButton('Consultar')
query_button.clicked.connect(consultar_dados)
layout.addWidget(query_button)

clear_button = QPushButton('Limpar')
clear_button.clicked.connect(clear_input_text)
layout.addWidget(clear_button)

# Rótulo para exibir resultados
result_label = QLabel("")
layout.addWidget(result_label)

# Define o layout da janela
window.setLayout(layout)

# Exibe a janela
window.show()

# Inicia a aplicação
sys.exit(app.exec_())
