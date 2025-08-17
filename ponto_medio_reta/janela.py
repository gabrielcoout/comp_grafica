# ui.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QMainWindow, QLabel, QSpinBox, QFrame
)
from visualizador import VisualizadorDeLinha

LIMITE_GRID = 500


class JanelaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Algoritmo do Ponto Médio - Bresenham")
        
        self.grid = 20
        
        self.tela = VisualizadorDeLinha(self.grid)

        # Configura os widgets de controle (SpinBoxes)
        self.seletor_x1 = QSpinBox()
        self.seletor_y1 = QSpinBox()
        self.seletor_x2 = QSpinBox()
        self.seletor_y2 = QSpinBox()
        
        for seletor in [self.seletor_x1, self.seletor_y1, self.seletor_x2, self.seletor_y2]:
            seletor.setRange(0, self.grid)

        # Define valores iniciais
        self.seletor_x1.setValue(1)
        self.seletor_y1.setValue(2)
        self.seletor_x2.setValue(18)
        self.seletor_y2.setValue(8)

        self.botao_desenhar = QPushButton("Desenhar")
        
        # NOVO: Criação do seletor para o tamanho da grade
        self.seletor_limite_grade = QSpinBox()
        self.seletor_limite_grade.setRange(5, LIMITE_GRID) # Define um limite razoável
        self.seletor_limite_grade.setValue(self.grid)

        # Monta o layout dos controles
        layout_controles = self._criar_layout_controles()

        # Monta o layout principal da janela
        layout_principal = QVBoxLayout()
        layout_principal.addLayout(layout_controles)
        layout_principal.addWidget(self.tela)

        widget_central = QWidget()
        widget_central.setLayout(layout_principal)
        self.setCentralWidget(widget_central)

        # Conecta os sinais às funções
        self.botao_desenhar.clicked.connect(self.desenhar)
        # NOVO: Conecta o seletor de grade à função de atualização
        self.seletor_limite_grade.valueChanged.connect(self.atualizar_grade)
        
        # Desenha a linha inicial
        self.desenhar()

    def _criar_layout_controles(self):
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
        
        # NOVO: Adiciona o controle de tamanho da grade ao layout
        layout.addWidget(QLabel("Tamanho da Grade:"))
        layout.addWidget(self.seletor_limite_grade)
        
        separador2 = QFrame() # Adiciona um separador visual
        separador2.setFrameShape(QFrame.Shape.VLine)
        separador2.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(separador2)
        
        layout.addWidget(self.botao_desenhar)
        return layout

    # NOVO: Função para lidar com a mudança do tamanho da grade
    def atualizar_grade(self):
        """
        Atualiza o limite da grade em toda a aplicação quando o valor do seletor muda.
        """
        novo_limite = self.seletor_limite_grade.value()
        self.grid = novo_limite
        
        # Atualiza o widget de visualização com o novo limite
        self.tela.definir_limite_grade(novo_limite)
        
        # Atualiza o range dos seletores de coordenadas
        for seletor in [self.seletor_x1, self.seletor_y1, self.seletor_x2, self.seletor_y2]:
            seletor.setRange(0, novo_limite)
            
        # Força o redesenho da linha atual com a nova grade
        self.desenhar()

    def desenhar(self):
        x1 = self.seletor_x1.value()
        y1 = self.seletor_y1.value()
        x2 = self.seletor_x2.value()
        y2 = self.seletor_y2.value()
        self.tela.definir_linha(x1, y1, x2, y2)