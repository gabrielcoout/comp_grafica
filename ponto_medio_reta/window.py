# ui.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QMainWindow, QLabel, QSpinBox, QFrame
)
from ponto_medio_reta.algoritmo import VisualizadorDeLinha # Importa o widget de desenho

class JanelaPrincipal(QMainWindow):
    """
    Define a janela principal da aplicação, incluindo os controles
    de entrada e a tela de visualização.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Algoritmo do Ponto Médio - Bresenham")
        
        self.limite_grade = 20
        
        # Cria a instância do nosso widget de desenho customizado
        self.tela = VisualizadorDeLinha(self.limite_grade)

        # Configura os widgets de controle (SpinBoxes)
        self.seletor_x1 = QSpinBox()
        self.seletor_y1 = QSpinBox()
        self.seletor_x2 = QSpinBox()
        self.seletor_y2 = QSpinBox()
        for seletor in [self.seletor_x1, self.seletor_y1, self.seletor_x2, self.seletor_y2]:
            seletor.setRange(0, self.limite_grade)

        # Define valores iniciais
        self.seletor_x1.setValue(1)
        self.seletor_y1.setValue(2)
        self.seletor_x2.setValue(18)
        self.seletor_y2.setValue(8)

        self.botao_desenhar = QPushButton("Desenhar")

        # Monta o layout dos controles
        layout_controles = self._criar_layout_controles()

        # Monta o layout principal da janela
        layout_principal = QVBoxLayout()
        layout_principal.addLayout(layout_controles)
        layout_principal.addWidget(self.tela)

        widget_central = QWidget()
        widget_central.setLayout(layout_principal)
        self.setCentralWidget(widget_central)

        # Conecta o sinal do botão à função de desenho
        self.botao_desenhar.clicked.connect(self.desenhar)
        
        # Desenha a linha inicial
        self.desenhar()

    def _criar_layout_controles(self):
        """Cria e retorna o layout para os controles de entrada."""
        layout = QHBoxLayout()
        layout.addWidget(QLabel("P1:"))
        layout.addWidget(QLabel("x:"))
        layout.addWidget(self.seletor_x1)
        layout.addWidget(QLabel("y:"))
        layout.addWidget(self.seletor_y1)

        separador = QFrame()
        separador.setFrameShape(QFrame.Shape.VLine)
        separador.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(separador)

        layout.addWidget(QLabel("P2:"))
        layout.addWidget(QLabel("x:"))
        layout.addWidget(self.seletor_x2)
        layout.addWidget(QLabel("y:"))
        layout.addWidget(self.seletor_y2)

        layout.addStretch()
        layout.addWidget(self.botao_desenhar)
        return layout

    def desenhar(self):
        x1 = self.seletor_x1.value()
        y1 = self.seletor_y1.value()
        x2 = self.seletor_x2.value()
        y2 = self.seletor_y2.value()
        self.tela.definir_linha(x1, y1, x2, y2)