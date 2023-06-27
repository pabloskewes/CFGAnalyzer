from src.graph.graph import Graph
from string import ascii_lowercase

def check_adj_list(letter, node, path, visited_nodes, graph: Graph):
    for n in graph.nodes:
        if n not in visited_nodes:
            if node in graph.adjacency_list[n]:
                if letter in n[:n.find('=')]:
                    visited_nodes.append(n)
                    pass
                else:
                    visited_nodes.append(n)
                    path.append(n)
                    path = check_adj_list(letter, n, path, visited_nodes, graph)
            if graph.adjacency_list[n]==[]:
                return path


def analize_graph(graph: Graph):
    # Debemos buscar todos los caminos entre el primer nodo y 'fin'
    # Encntramos si en algún bloque hay una variable, si no se define en ese nodo, buscamos en los nodos anteriores
    # Variable definida es de la forma: x=... siempre q x no esté al lado derecho de =
    # Eliminamos los espacios de cada nodo, buscamos si x está dentro de una función o al lado derecho de =
    # Luego buscamos x=... en nodos anteriores
    used_var = []
    used_in_node = []
    for letter in ascii_lowercase:
        for node in graph.nodes:
            if (('(' in node) and (')' in node)):
                if letter in node[node.find("(")+1:node.find(")")] and letter not in used_var:
                    used_var.append(letter)
                    used_in_node.append(node)
            elif '=' in node:
                if letter in node[node.find('=')+1:] and letter not in used_var:
                    used_var.append(letter)
                    used_in_node.append(node)
            else:
                pass

    undef_var = []
    paths = []

    for i in range(len(used_var)):
        start = used_in_node[i]
        path = check_adj_list(used_var[i], start, [start], [start], graph)
        if path != start:
            undef_var.append(used_var[i])
            paths.append(path)

    return undef_var



        
