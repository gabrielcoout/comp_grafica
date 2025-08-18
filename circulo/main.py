# main.py
import sys
from PyQt6.QtWidgets import QApplication
from janela import JanelaPrincipal

def main():
    """Função principal que inicia a aplicação."""
    app = QApplication(sys.argv)
    janela = JanelaPrincipal()
    janela.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()