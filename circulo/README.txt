Exercício 2 - Círculo
Alunos: Gabriel Coutinho Chaves, João Pedro Pereira Balieiro

Modularização do Código
O projeto é dividido em três módulos para uma clara separação de responsabilidades:

main.py: Ponto de entrada da aplicação. Sua única função é inicializar e exibir a janela principal.

janela.py: Camada de Interface do Usuário (UI). Define a estrutura da janela, widgets de controle (como sliders e botões) e gerencia as interações do usuário.

algoritmo.py: Camada de Lógica e Visualização. Contém a classe VisualizadorCirculo, que implementa os algoritmos de desenho de círculo (Ponto Médio e Trigonométrico) e renderiza a grade e os resultados na tela.