Exercício 1 - Reta
Alunos: Gabriel Coutinho Chaves, João Pedro Pereira Balieiro

Modularização do Código
O projeto é dividido em três módulos distintos para separar as responsabilidades:

main.py: Ponto de entrada. Apenas inicializa e executa a aplicação.

janela.py: Camada de Interface (UI). Gerencia a janela, os botões e as entradas do usuário, sem conhecer a lógica do algoritmo.

algoritmo.py: Camada de Lógica e Visualização. Contém a implementação do algoritmo de Bresenham e a lógica para desenhar a grade e as linhas na tela.