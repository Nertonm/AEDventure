from itertools import permutations


# Função de DFS para calcular todos os percursos
def dfs(graph, node, visited, path, all_paths):
    visited[node] = True
    path.append(node)

    # Se todos os nós foram visitados, adiciona o caminho à lista
    if len(path) == len(graph):
        all_paths.append(list(path))
    else:
        for neighbor in graph[node]:
            if not visited[neighbor]:
                dfs(graph, neighbor, visited, path, all_paths)

    # Desfaz o passo, removendo o nó da lista de caminho e marcando como não visitado
    path.pop()
    visited[node] = False


# Função principal para gerar todas as permutações possíveis com o nó 'A' como ponto inicial
def find_all_permutations(graph):
    all_paths = []

    # Para gerar todas as permutações dos nós do grafo, excluindo 'A'
    nodes = list(graph.keys())
    nodes.remove('room0')  # Remove 'A' da lista de permutação

    # Gerar permutações apenas dos outros nós (excluindo 'A')
    for perm in permutations(nodes):
        visited = {node: False for node in graph}
        path = ['room0']  # Começa com 'A'

        # Realiza o DFS a partir de 'A' e percorre a permutação
        current_node = 'room0'
        for next_node in perm:
            # Realiza o DFS apenas com os vizinhos não visitados
            if next_node in graph[current_node]:
                dfs(graph, next_node, visited, path, all_paths)

    return all_paths


# Definindo um grafo de exemplo (como um dicionário de listas de adjacência)
graph = {
    'room0': ['room1_up', 'room1_down', 'room1_left', 'room1_right', 'room1_down_right'],
    'room1_up': ['room2_up_left', 'room2_up_right'],
    'room1_down': ['room2_left_down', 'room2_down'],
    'room1_left': ['room2_up_left', 'room2_left'],
    'room1_right': ['room2_right', 'room2_up_right'],
    'room1_down_right': ['room2_down_right', 'room2_right'],
    'room2_up_left': ['room3_up_left', 'room3_up'],
    'room2_up_right': ['room3_up_right', 'room3_up'],
    'room2_left_down': ['room3_down_left'],
    'room2_down': ['room3_down_left', 'room3_down_right'],
    'room2_right': ['room3_right_down', 'room3_right_up'],
    'room2_down_right': ['room3_down_right'],
    'room2_left': ['room3_left', 'room3_left_up', 'room3_left_down'],
    'room3_up_left': [],
    'room3_up': [],
    'room3_up_right': [],
    'room3_down_left': [],
    'room3_down_right': [],
    'room3_right_down': [],
    'room3_right_up': [],
    'room3_left': [],
    'room3_left_up': [],
    'room3_left_down': [],
}

# Chamando a função para encontrar todas as permutações possíveis com o nó 'A' sempre começando
paths = find_all_permutations(graph)

# Exibindo todos os percursos possíveis
print("Todos os percursos possíveis no grafo começando de A:")
for path in paths:
    print(" -> ".join(path))
