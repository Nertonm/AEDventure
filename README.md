# AEDventure

## Visão Geral

AEDventure é um jogo educacional desenvolvido em Python usando a biblioteca Pygame. O objetivo do jogo é ensinar algoritmos e estruturas de dados de forma interativa e divertida. O jogador pode escolher diferentes níveis de dificuldade e enfrentar desafios como a Torre de Hanói e ordenação de arrays.

## Funcionalidades

- **Seleção de Dificuldade**: Fácil, Médio e Difícil.
- **Desafios**: Torre de Hanói, Ordenação de Arrays.
- **Mapas Interativos**: Navegue por diferentes salas e resolva puzzles.
- **Menu de Pausa**: Pause o jogo e acesse o menu a qualquer momento.

## Tecnologias Utilizadas

- **Python**
- **Pygame**
- **pytmx**: Para carregar e processar mapas TMX.

## Instalação

### Pré-requisitos

- Python 3.6 ou superior
- pip (Python package installer)

### Passos

1. Clone o repositório:
    ```bash
    git clone https://github.com/seu-usuario/AEDventure.git
    cd AEDventure
    ```

2. Crie um ambiente virtual (opcional, mas recomendado):
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows use `venv\Scripts\activate`
    ```

3. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

## Uso

### Executando o Jogo

Para iniciar o jogo, execute o seguinte comando:
```bash
python code/main.py
```
## Orientações do Mapa
### **O mapa precisa estar em tmx!!**
**A ultima linha do mapa deve ser prenchida com boundary para lidar com a colisão do mapa**

### **Tile e Tamanho**
- **Tamanho do Tile**: 128x128 pixels
- **Tamanho do Jogador**: 128x128 pixels

### **Objetos**
- **player**: Ponto de geração inicial do jogador no mapa.
- **door (Porta)**: Objeto que permite a transição entre mapas.
   - Cada porta tem um campo de string chamado **"path"**, que guarda o nome do mapa de destino.

### **Camadas do Mapa**
1. **floor (Chão)**: Primeira camada renderizada, onde o jogador caminha.
2. **door (Portas)**: Camada que contém as portas para troca de mapas.
3. **boundary (Limites)**: Define as bordas do mapa, impedindo que o jogador ultrapasse os limites.
