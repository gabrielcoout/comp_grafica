# ui.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QMainWindow, QLabel, QSlider, QRadioButton, QGroupBox, QSpinBox
)
from PyQt6.QtCore import Qt
from algoritmo import VisualizadorCirculo

HEIGHT, WIDTH = 400, 400
INITIAL_RADIUS = 10
INITIAL_GRID_SIZE, GRID_MIN, GRID_MAX = 20, 10, 500

class JanelaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Visualizador de Algoritmos de Círculo")
        
        self.seletor_grid = QSpinBox()
        self.seletor_grid.setRange(10, GRID_MAX)
        self.seletor_grid.setSingleStep(1)
        self.seletor_grid.setValue(INITIAL_GRID_SIZE)
        self.limite_grade = self.seletor_grid.value()
        
        self.tela = VisualizadorCirculo(self.limite_grade)
        
        self.slider_raio = QSlider(Qt.Orientation.Horizontal)
        self.slider_raio.setRange(0, self.limite_grade)
        self.slider_raio.setValue(10)
        self.label_raio_valor = QLabel(f"Raio (R): {self.slider_raio.value()}")

        self.radio_trig = QRadioButton("Trigonométrico")
        self.radio_ponto_medio = QRadioButton("Ponto Médio (Bresenham)")
        self.radio_ponto_medio.setChecked(True)

        self.botao_desenhar = QPushButton("Desenhar Círculo")
        
        self.label_tempo = QLabel("Tempo: -- s")
        
        controles_layout = self._criar_layout_controles()
        layout_principal = QVBoxLayout()
        layout_principal.addLayout(controles_layout)
        layout_principal.addWidget(self.tela)

        widget_central = QWidget()
        widget_central.setLayout(layout_principal)
        self.setCentralWidget(widget_central)
        self.resize(HEIGHT, WIDTH)

        self.tela.calculoFinalizado.connect(self.atualizar_label_tempo)

        self.slider_raio.valueChanged.connect(self.atualizar_label_raio)
        self.seletor_grid.valueChanged.connect(self.atualizar_grid)
        self.botao_desenhar.clicked.connect(self.desenhar)
        
        self.desenhar()
        
    def _criar_layout_controles(self):
        controles_principais = QVBoxLayout()
        grid_layout = QHBoxLayout()
        grid_layout.addWidget(QLabel("Limite da Grade:"))
        grid_layout.addWidget(self.seletor_grid)
        raio_layout = QHBoxLayout()
        raio_layout.addWidget(self.label_raio_valor)
        raio_layout.addWidget(self.slider_raio)
        controles_principais.addLayout(grid_layout)
        controles_principais.addLayout(raio_layout)
        algoritmo_box = QGroupBox("Algoritmo")
        algoritmo_layout = QVBoxLayout()
        algoritmo_layout.addWidget(self.radio_trig)
        algoritmo_layout.addWidget(self.radio_ponto_medio)
        algoritmo_box.setLayout(algoritmo_layout)
        resultados_box = QGroupBox("Resultados")
        resultados_layout = QVBoxLayout()
        resultados_layout.addWidget(self.label_tempo)
        resultados_box.setLayout(resultados_layout)
        layout = QHBoxLayout()
        layout.addLayout(controles_principais, stretch=4)
        layout.addWidget(algoritmo_box, stretch=2)
        layout.addWidget(resultados_box, stretch=2)
        layout.addWidget(self.botao_desenhar, stretch=1)
        return layout

    def atualizar_label_tempo(self, tempo):
        """Atualiza o label com o tempo de execução recebido pelo sinal."""
        self.label_tempo.setText(f"Tempo: {tempo:.6f} s")

    def atualizar_label_raio(self, valor):
        self.label_raio_valor.setText(f"Raio (R): {valor}")
        
    def atualizar_grid(self, novo_limite):
        self.limite_grade = novo_limite
        self.tela.definir_limite_grade(novo_limite)
        self.slider_raio.setRange(0, novo_limite)
        self.desenhar()
        
    def desenhar(self):
        R = self.slider_raio.value()
        
        id_algoritmo = "ponto_medio"
        if self.radio_trig.isChecked():
            id_algoritmo = "trig"
        
        self.tela.definir_circulo(R, id_algoritmo)