import sys
import pyodbc
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QScrollArea, QListWidget, QDialog
from PyQt5.QtGui import QPixmap, QColor, QPalette
from PyQt5.QtCore import Qt

# Estabelece uma conexão com o banco de dados usando um DSN específico
cnxn = pyodbc.connect('DSN=DatalakeLLAP', autocommit=True)
cursor = cnxn.cursor()

# Classe para a janela de detalhes
class DetalhesDialog(QDialog):
    def __init__(self, detalhes, logo_path):
        super().__init__()

        self.setWindowTitle('Detalhes do Resultado')
        self.setGeometry(100, 100, 400, 300)

        # Defina o fundo verde
        self.setStyleSheet("background-color: #04944B;")

        # Adicione um QLabel para o logotipo na parte superior
        logo_label = QLabel(self)
        logo_label.setGeometry(10, 10, 100, 100)  # Ajuste as dimensões e a posição conforme necessário
        pixmap = QPixmap(logo_path)  # Substitua 'logo.png' pelo caminho da sua imagem do logotipo
        pixmap = pixmap.scaled(100, 100, aspectRatioMode=Qt.KeepAspectRatio)
        logo_label.setPixmap(pixmap)

        detalhes_label = QLabel(detalhes, self)
        detalhes_label.setGeometry(10, 120, 380, 170)  # Ajuste as dimensões e a posição conforme necessário
        detalhes_label.setStyleSheet("color: white;")  # Define a cor do texto como branco

# Função para consultar dados
def consultar_dados():
    dado = input_text.text()

    # Limpa o campo de resultados
    result_list.clear()

    # Realiza a consulta SQL
    cursor.execute(f"SELECT cod_bndes, cpf_cnpj, nome, nome_categoria FROM rich_entidades.vi_n02_entidade WHERE cpf_cnpj = '{dado}' OR nome LIKE '%{dado}%' OR cod_bndes = '{dado}'")

    rows = cursor.fetchall()
    if rows:
        for row in rows:
            formatted_data = [f"{label}: {value}" for label, value in
                              zip(['Código BNDES', 'CPF/CNPJ', 'Razão Social', 'Categoria'], row)]
            result_list.addItem("\n".join(formatted_data))
    else:
        result_list.addItem("Nenhum resultado encontrado.")

# Função para exibir detalhes do item
def mostrar_detalhes(item):
    detalhes_dialog = DetalhesDialog(item.text(), 'logo.png')
    detalhes_dialog.exec_()

# Função para limpar o campo de entrada de texto
def clear_input_text():
    input_text.clear()
    result_list.clear()

# Cria a aplicação Qt
app = QApplication(sys.argv)

# Cria a janela principal
window = QWidget()
window.setWindowTitle('Consulta de Dados WI')
window.setGeometry(100, 100, 800, 400)

# Definir a cor de fundo do aplicativo (cor: 04944B)
palette = QPalette()
palette.setColor(QPalette.Window, QColor(4, 148, 75))
window.setPalette(palette)

# Layout da janela
layout = QVBoxLayout()

# Layout para a imagem do logotipo
logo_layout = QHBoxLayout()

# Adicionar a imagem do logotipo (substitua 'logo.png' pelo caminho da sua imagem)
logo_pixmap = QPixmap('logo.png')
logo_pixmap = logo_pixmap.scaledToWidth(100)  # Redimensionar logotipo
logo_label = QLabel()
logo_label.setPixmap(logo_pixmap)
logo_layout.addWidget(logo_label)
logo_layout.addStretch(1)  # Adicionar espaço flexível para alinhar à direita

layout.addLayout(logo_layout)

# Adiciona um rótulo (label) com texto estático
label = QLabel("Digite o Dado que deseja Consultar:")
label.setStyleSheet("color: white;")
layout.addWidget(label)

# Campo de entrada de texto
input_text = QLineEdit()
layout.addWidget(input_text)

# Botões de consulta e limpeza
button_layout = QHBoxLayout()
query_button = QPushButton('Consultar')
query_button.setFixedSize(100, 30)  # Definir tamanho do botão
query_button.clicked.connect(consultar_dados)
button_layout.addWidget(query_button)

clear_button = QPushButton('Limpar')
clear_button.setFixedSize(100, 30)  # Definir tamanho do botão
clear_button.clicked.connect(clear_input_text)
button_layout.addWidget(clear_button)

layout.addLayout(button_layout)

# Cria um widget de rolagem para a área de resultados
scroll_area = QScrollArea()
scroll_area.setWidgetResizable(True)

# Widget de lista para exibir resultados
result_list = QListWidget()
result_list.itemClicked.connect(mostrar_detalhes)
scroll_area.setWidget(result_list)

layout.addWidget(scroll_area)

# Define o layout da janela
window.setLayout(layout)

# Exibe a janela
window.show()

# Inicia a aplicação
sys.exit(app.exec_())
