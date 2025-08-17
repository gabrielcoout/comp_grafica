# visualizador.py
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtCore import Qt, QPoint

class VisualizadorDeLinha(QWidget):
    def __init__(self, limite_grade):
        super().__init__()
        self.limite_grade = limite_grade
        self.setMinimumSize(400, 400)
        self.linha = None

    def definir_linha(self, x1, y1, x2, y2):
        """Define as coordenadas da linha a ser desenhada."""
        self.linha = (x1, y1, x2, y2)
        self.update()  # Solicita uma repintura do widget

    def algoritmo_ponto_medio(self, painter, x1, y1, x2, y2):
        """Implementação do algoritmo de Bresenham para desenhar uma linha."""
        dx = x2 - x1
        dy = y2 - y1

        sx = 1 if dx >= 0 else -1
        sy = 1 if dy >= 0 else -1

        dx = abs(dx)
        dy = abs(dy)
        
        x, y = x1, y1
        
        if dx >= dy:
            d = 2 * dy - dx
            incE = 2 * dy
            incNE = 2 * (dy - dx)
            
            for _ in range(dx + 1):
                painter.drawPoint(x, y)
                if d <= 0:
                    d += incE
                else:
                    d += incNE
                    y += sy
                x += sx
        else:
            d = 2 * dx - dy
            incE = 2 * dx
            incNE = 2 * (dx - dy)
            
            for _ in range(dy + 1):
                painter.drawPoint(x, y)
                if d <= 0:
                    d += incE
                else:
                    d += incNE
                    x += sx
                y += sy

    def desenhar_grid(self, painter):
        """Desenha a grade e os eixos no fundo do widget."""
        caneta_grade = QPen(QColor(220, 220, 220), 0)
        painter.setPen(caneta_grade)
        for i in range(self.limite_grade + 1):
            painter.drawLine(QPoint(i, 0), QPoint(i, self.limite_grade))
            painter.drawLine(QPoint(0, i), QPoint(self.limite_grade, i))

        caneta_eixos = QPen(QColor(150, 150, 150), 0)
        painter.setPen(caneta_eixos)
        painter.drawLine(QPoint(0, 0), QPoint(self.limite_grade, 0))
        painter.drawLine(QPoint(0, 0), QPoint(0, self.limite_grade))

    def paintEvent(self, event):
        """Método chamado automaticamente para desenhar o widget."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        painter.fillRect(self.rect(), Qt.GlobalColor.white)
        
        margem = 20
        w = self.width() - 2 * margem
        h = self.height() - 2 * margem
        
        if w <= 0 or h <= 0:
            return

        escala = min(w, h) / self.limite_grade
        
        offset_x = margem + (w - self.limite_grade * escala) / 2
        offset_y = margem + (h - self.limite_grade * escala) / 2

        painter.save()

        # Inverte o eixo Y para que (0,0) fique no canto inferior esquerdo
        painter.translate(offset_x, offset_y + self.limite_grade * escala)
        painter.scale(escala, -escala)

        self.desenhar_grid(painter)
        
        if self.linha:
            x1, y1, x2, y2 = self.linha
            
            # Desenha a linha ideal (vermelha)
            caneta_ideal = QPen(QColor("red"), 0.15)
            painter.setPen(caneta_ideal)
            painter.drawLine(QPoint(x1, y1), QPoint(x2, y2))
            
            # Desenha os pontos do algoritmo (azul)
            caneta_ponto_medio = QPen(QColor("blue"), 0.5, Qt.PenStyle.SolidLine)
            caneta_ponto_medio.setCapStyle(Qt.PenCapStyle.RoundCap)
            painter.setPen(caneta_ponto_medio)
            self.algoritmo_ponto_medio(painter, x1, y1, x2, y2)

        painter.restore()

    def definir_limite_grade(self, novo_limite):
        """Atualiza o limite da grade e força uma repintura."""
        self.limite_grade = novo_limite
        self.update()