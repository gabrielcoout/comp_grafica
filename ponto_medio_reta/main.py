import sys
from PyQt6.QtWidgets import QApplication
from janela import JanelaPrincipal 

def main():
    aplicacao = QApplication(sys.argv)
    janela = JanelaPrincipal()
    janela.show()
    sys.exit(aplicacao.exec())

if __name__ == "__main__":
    main()