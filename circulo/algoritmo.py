# visualizador_circulo.py
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtCore import Qt, QPoint, pyqtSignal 
import numpy as np 
from numpy import cos, sin, pi 
import time

class VisualizadorCirculo(QWidget):
    calculoFinalizado = pyqtSignal(float)
    def __init__(self, limite_grade):
        super().__init__()
        self.limite_grade = limite_grade
        self.setMinimumSize(500, 500)
        self.raio = 0
        
        self.algoritmo_id = None

    def definir_circulo(self, R, algoritmo_id):
        """Recebe os parâmetros do círculo e solicita uma repintura."""
        self.raio = R
        self.algoritmo_id = algoritmo_id
        self.update()

    def definir_limite_grade(self, novo_limite):
        self.limite_grade = novo_limite
        self.update()

    # Algoritmo Trigonométrico
    def _circulo_trigonometrico(self, painter, R):
        inicio = time.perf_counter()
        
        if R == 0:
            painter.drawPoint(0, 0)
        else:
            num_passos = int(2 * pi * R)
            for theta in np.linspace(0, 2 * pi, num_passos):
                x = int(round(R * cos(theta))) 
                y = int(round(R * sin(theta)))
                painter.drawPoint(x, y)

        fim = time.perf_counter()
        # MODIFICADO: Emite o sinal com o tempo de execução
        self.calculoFinalizado.emit(fim - inicio)

    def _ponto_medio_circulo(self, painter, R):
        inicio = time.perf_counter()

        if R == 0:
            painter.drawPoint(0, 0)
        else:
            x = 0
            y = R
            d = 1 - R
            
            while y >= x:
                painter.drawPoint(x, y)
                painter.drawPoint(y, x)
                painter.drawPoint(-x, y)
                painter.drawPoint(-y, x)
                painter.drawPoint(-x, -y)
                painter.drawPoint(-y, -x)
                painter.drawPoint(x, -y)
                painter.drawPoint(y, -x)

                if d < 0:
                    d += 2 * x + 3
                else:
                    d += 2 * (x - y) + 5
                    y -= 1
                x += 1
        
        fim = time.perf_counter()
        self.calculoFinalizado.emit(fim - inicio)
            
    def _desenhar_grid(self, painter, escala):
        pen_grade = QPen(QColor(230, 230, 230), 0)
        painter.setPen(pen_grade)
        for i in range(-self.limite_grade, self.limite_grade + 1, 1):
            if i == 0: continue
            painter.drawLine(QPoint(i, -self.limite_grade), QPoint(i, self.limite_grade))
            painter.drawLine(QPoint(-self.limite_grade, i), QPoint(self.limite_grade, i))
        pen_eixos = QPen(QColor(150, 150, 150), 0)
        painter.setPen(pen_eixos)
        painter.drawLine(QPoint(-self.limite_grade, 0), QPoint(self.limite_grade, 0))
        painter.drawLine(QPoint(0, -self.limite_grade), QPoint(0, self.limite_grade))


    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), Qt.GlobalColor.white)
        
        centro_x, centro_y = self.width() / 2, self.height() / 2
        margem = 20
        largura_util = self.width() - 2 * margem
        altura_util = self.height() - 2 * margem
        
        if largura_util <= 0 or altura_util <= 0: return
        
        escala = min(largura_util, altura_util) / (2 * self.limite_grade)

        painter.save()
        painter.translate(centro_x, centro_y)
        painter.scale(escala, -escala)

        self._desenhar_grid(painter, escala)

        if self.raio > 0:
            # Desenha o círculo teórico (vermelho)
            pen_teorico = QPen(QColor("red"), 0.15)
            painter.setPen(pen_teorico)
            painter.drawEllipse(QPoint(0, 0), self.raio, self.raio)
            
            # Desenha os pontos do algoritmo (azul) selecionado
            caneta_ponto_medio = QPen(QColor("blue"), 0.5, Qt.PenStyle.SolidLine)
            caneta_ponto_medio.setCapStyle(Qt.PenCapStyle.RoundCap)
            painter.setPen(caneta_ponto_medio)

            if self.algoritmo_id == "ponto_medio":
                self._ponto_medio_circulo(painter, self.raio)
            elif self.algoritmo_id == "trig":
                self._circulo_trigonometrico(painter, self.raio)

        painter.restore()