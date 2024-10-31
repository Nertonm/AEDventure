# AEDventure

### Instalar Dependências:

    Navegue até a pasta do seu projeto no terminal e execute:

    ```bash
    pip install -r requirements.txt
    ```
    
### Geração de Mapa
O mapa precisa estar em tmx!!

A ultima linha do mapa deve ser prenchida com boundary para lidar com a colisão do mapa
Tile e Tamanho

    Tamanho do Tile: 64x64 pixels
    Tamanho do Jogador: 128x128 pixels

Objetos

    player: Ponto de geração inicial do jogador no mapa.
    door (Porta): Objeto que permite a transição entre mapas.
        Cada porta tem um campo de string chamado "path", que guarda o nome do mapa de destino.

Camadas do Mapa

    floor (Chão): Primeira camada renderizada, onde o jogador caminha.
    door (Portas): Camada que contém as portas para troca de mapas.
    boundary (Limites): Define as bordas do mapa, impedindo que o jogador ultrapasse os limites.
