# visualizador_circulo.py
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtCore import Qt, QPoint, pyqtSignal 
from math import factorial, pi
import time
import numpy as np

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

    def _taylor_sin(self, x, termos=5):
        """ Aproximação de sin(x) por série de Taylor """
        resultado = 0.0
        sinal = 1
        for n in range(termos):
            termo = (x**(2*n + 1)) / factorial(2*n + 1)
            resultado += sinal * termo
            sinal *= -1
        return resultado

    def _taylor_cos(self, x, termos=5):
        """ Aproximação de cos(x) por série de Taylor """
        resultado = 0.0
        sinal = 1
        for n in range(termos):
            termo = (x**(2*n)) / factorial(2*n)
            resultado += sinal * termo
            sinal *= -1
        return resultado
    
    # Algoritmo Trigonométrico para desenhar círculos
    def _circulo_trigonometrico(self, painter, R):
        inicio = time.perf_counter()
        
        if R == 0:
            # Caso degenerado: círculo de raio zero é apenas um ponto
            painter.drawPoint(0, 0)
        else:
            # Número de pontos proporcional ao perímetro do círculo (2πR)
            num_passos = int(2 * pi * R)
            # Varremos o ângulo theta de 0 a 2π
            for theta in np.linspace(0, 2 * pi, num_passos):
                # Fórmulas paramétricas: x = Rcosθ, y = Rsinθ
                x = int(round(R * np.cos(theta))) 
                y = int(round(R * np.sin(theta)))
                painter.drawPoint(x, y)

        fim = time.perf_counter()
        # Emite o tempo total de execução
        self.calculoFinalizado.emit(fim - inicio)

    def _circulo_trigonometrico_delta(self, painter, R):
        """
        Algoritmo trigonométrico incremental para círculo,
        usando apenas seno e cosseno aproximados por Taylor em Δθ.
        """
        inicio = time.perf_counter()

        if R == 0:
            painter.drawPoint(0, 0)
        else:
            # Número de pontos proporcional ao perímetro
            num_passos = int(2 * pi * R)
            delta = (2 * pi) / num_passos

            # Aproximações de sin(Δθ) e cos(Δθ) por Taylor
            cos_delta = self._taylor_cos(delta, termos=7)
            sin_delta = self._taylor_sin(delta, termos=7)

            # Ponto inicial (cos(0), sin(0)) = (1,0)
            cos_theta = 1.0
            sin_theta = 0.0

            for _ in range(num_passos + 1):
                x = int(round(R * cos_theta))
                y = int(round(R * sin_theta))
                painter.drawPoint(x, y)

                # Atualização incremental via rotação
                novo_cos = cos_theta * cos_delta - sin_theta * sin_delta
                novo_sin = sin_theta * cos_delta + cos_theta * sin_delta
                cos_theta, sin_theta = novo_cos, novo_sin

        fim = time.perf_counter()
        # Emite o sinal com o tempo de execução
        self.calculoFinalizado.emit(fim - inicio)


    def _ponto_medio_circulo(self, painter, R):
        """
        Desenha um círculo de raio R utilizando o algoritmo do ponto médio (Midpoint Circle Algorithm).
        """
        inicio = time.perf_counter()

        if R == 0:
            # Caso especial: círculo de raio zero é apenas um ponto
            painter.drawPoint(0, 0)
        else:
            # Começa do ponto mais alto do círculo (0, R)
            x = 0
            y = R

            # Parâmetro de decisão
            d = 1 - R
            
            while y >= x:
                # Desenha os 8 pontos simétricos em relação ao centro
                painter.drawPoint(x, y) 
                painter.drawPoint(y, x)
                painter.drawPoint(-x, y)
                painter.drawPoint(-y, x)
                painter.drawPoint(-x, -y)
                painter.drawPoint(-y, -x)
                painter.drawPoint(x, -y)
                painter.drawPoint(y, -x)

                if d < 0:
                    # Próximo ponto é o vizinho "leste" (E)
                    d += 2 * x + 3
                else:
                    # Próximo ponto é o vizinho "sudeste" (SE)
                    d += 2 * (x - y) + 5
                    y -= 1
                # Avança em x
                x += 1
        
        fim = time.perf_counter()
        # Emite o tempo de execução
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
            elif self.algoritmo_id == "trig1":
                self._circulo_trigonometrico(painter, self.raio)
            elif self.algoritmo_id == "trig2":
                self._circulo_trigonometrico_delta(painter, self.raio)

        painter.restore()