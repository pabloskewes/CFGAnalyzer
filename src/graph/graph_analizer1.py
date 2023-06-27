from src.graph.graph import Graph
from string import ascii_lowercase

def path_generator(start, end, path, graph: Graph):
    if start == end:
        return path
    else:
        if graph.adjacency_list[start] == []:
            return 'No path'
        else:
            for node in graph.adjacency_list[start]:
                path.append[node]
                path_generator(node, end, path, graph)



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

    # Para encontrar un camino que no define una variable, debemos encontrar todos los caminos desde el comienzo hasta 'fin'
    # Luego vemos si para todos los caminos existe al menos un nodo donde se define la variable
    paths = path_generator(graph.node[1], graph.node[0], [graph.node[1]])

    return paths



        
