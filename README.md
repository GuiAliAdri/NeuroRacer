# 🏎️ NeuroRacer - IA Evolutiva

Um simulador de direção autônoma onde carros aprendem a dirigir sozinhos utilizando Redes Neurais e Algoritmos Genéticos (NEAT). A cada geração, a IA evolui, aprende a fazer curvas e desviar de obstáculos em uma pista gerada proceduralmente.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Pygame](https://img.shields.io/badge/Library-Pygame-green)
![NEAT](https://img.shields.io/badge/Algorithm-NEAT-orange)

## 🧠 Como Funciona?

O projeto utiliza a biblioteca **NEAT-Python** (NeuroEvolution of Augmenting Topologies).
1.  **Sensores (Input):** Cada carro possui 5 "raios" (lidar) que medem a distância até as paredes ou obstáculos.
2.  **Rede Neural:** Essas distâncias entram na rede neural do carro, que processa a informação.
3.  **Ação (Output):** A rede decide se o carro deve virar para a **Esquerda** ou para a **Direita**.
4.  **Evolução:** Os carros que chegam mais longe e passam por mais checkpoints sobrevivem. Os piores são eliminados. A próxima geração é criada a partir dos "filhos" dos melhores pilotos.

## 🚀 Funcionalidades

* **Geração Procedural de Pistas:** O traçado da pista, a linha de chegada e os obstáculos são gerados via código a cada execução, garantindo que a IA não apenas "decore" um mapa.
* **Visão da IA:** Linhas coloridas mostram exatamente o que o carro está enxergando em tempo real.
* **Sistema de Checkpoints:** Lógica robusta para garantir que os carros andem na direção correta.
* **Contador de Voltas:** Exibe quantos carros conseguiram completar o circuito.

## 🛠️ Instalação

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/seu-usuario/NeuroRacer.git](https://github.com/seu-usuario/NeuroRacer.git)
    cd NeuroRacer
    ```

2.  **Crie um ambiente virtual (Opcional, mas recomendado):**
    ```bash
    python -m venv venv
    # Windows:
    .\venv\Scripts\activate
    # Linux/Mac:
    source venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install pygame neat-python
    ```

## 🎮 Como Rodar

1.  **Gere os Assets (apenas na primeira vez):**
    Execute este script para criar a pasta `assets` e desenhar o sprite do carro automaticamente.
    ```bash
    python setup_assets.py
    ```

2.  **Inicie a Simulação:**
    ```bash
    python main.py
    ```

## ⚙️ Configuração (NEAT)

Você pode ajustar os parâmetros da inteligência artificial editando o arquivo `config-neat.txt`:
* `pop_size`: Quantidade de carros por geração (Padrão: 30).
* `max_stagnation`: Quantas gerações sem melhora antes de reiniciar as espécies.

## 📂 Estrutura do Projeto

* `main.py`: Arquivo principal que inicia o loop do NEAT.
* `src/`: Contém todo o código fonte do jogo.
    * `game.py`: Gerencia a janela, loop do jogo e renderização.
    * `car.py`: Lógica do carro, física, sensores e colisão.
    * `track_generator.py`: Algoritmo que desenha a pista e a máscara de colisão.
    * `config.py`: Constantes globais (cores, velocidade, dimensões).
* `assets/`: Imagens do jogo (geradas via script).

---
Desenvolvido com 🐍 Python
Feito por: Guilherme Ali Adri