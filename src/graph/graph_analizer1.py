from src.graph.graph import Graph
from string import ascii_lowercase

def find_all_paths(graph: Graph, start, end, path=[]):
        path = path + [start]
        if start == end:
            return [path]
        if start not in graph.nodes:
            return []
        paths = []
        for node in graph.adjacency_list[start]:
            if node not in path:
                newpaths = find_all_paths(graph, node, end, path)
                for newpath in newpaths:
                    paths.append(newpath)
        return paths 

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

    undef_var = {var:True for var in used_var}
    undef_var_print = []
    paths = []
    undef_path = []

    # Para encontrar un camino que no define una variable, debemos encontrar todos los caminos desde el comienzo hasta 'fin'
    # Luego vemos si para todos los caminos existe al menos un nodo donde se define la variable
    start = graph.nodes[1]
    end = 'fin'
    paths = find_all_paths(graph, start, end)
    for path in paths:
        for node in path:
            separated_node = node.split('\n')
            for step in separated_node:
                if '=' in step:
                    for letter in used_var:
                        if letter in step and letter not in step[step.find('=')+1:]:
                            undef_var[letter] = False
        for letter in used_var:
            if undef_var[letter] == True:
                undef_var_print.append(letter)
                undef_path.append(path)

    return [undef_var_print, undef_path]



        
