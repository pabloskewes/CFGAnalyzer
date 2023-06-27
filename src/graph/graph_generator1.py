import os
from src.graph import Graph


def has_tab(line):
    line_list = list(line)
    if line_list[0:4] == [" ", " ", " ", " "]:
        return True
    else:
        return False


def tab_counter(line):
    line_list = list(line)
    tabs = 0
    i = 0
    while i < len(line_list):
        if line_list[i : i + 4] == [" ", " ", " ", " "]:
            tabs += 1
        else:
            pass
        i += 4
    return tabs


def is_if(line):
    line_list = list(line.lstrip())
    if line_list[0:2] == ["i", "f"]:
        return True
    else:
        return False


def is_while(line):
    line_list = list(line.lstrip())
    if line_list[0:5] == ["w", "h", "i", "l", "e"]:
        return True
    else:
        return False


def is_else(line):
    line_list = list(line.lstrip())
    if line_list[0:4] == ["e", "l", "s", "e"]:
        return True
    else:
        return False


def generate_graph(path: str) -> Graph:
    """Run the graph generator."""
    f = open(path, "r")

    graph = Graph()
    graph.add_node("fin")

    line_to_add = ""
    line_if = ""
    end_of_if = ""
    end_of_else = ''
    end_of_while = ''
    if_block = False
    else_block = False
    while_block = False
    edge_from_if = True
    edge_to_if = True
    edge_to_else = True
    edge_from_else = True
    edge_from_while = True
    edge_to_while = True
    edge_end_while = True

    tabs = 0

    for line in f:
        # Veo si la linea es un if
        if is_if(line) and tab_counter(line) == tabs:
            if_block = True
            else_block = False
            line_if = line_to_add + line  # Agrego la linea al nodo por agregar
            edge_to_if = False
            graph.add_node(line_if)  # Agrego el nodo
            line_to_add = ""
            tabs += 1  # Aumento el numero de tabs necesario para estar en el bloque
            if while_block:
                graph.add_edge(line_while, line_if)
                edge_from_while = True
        # Si hay un bloque if activo las lineas deben tener la cantidad de tabs adecuadas
        elif if_block and tab_counter(line) == tabs:
            line_to_add = (
                line_to_add + line
            )  # Agrego cada linea dentro del bloque al bloque por agregar
        # Veo si la linea es un else y tiene un tab menos q los necesarios para estar dentro del bloque
        elif is_else(line) and tab_counter(line) == tabs - 1:
            if_block = False
            else_block = True
            edge_to_else = False
            edge_from_else = False
            graph.add_node(
                line_to_add
            )  # Agrego las lineas consideradas dentro del bloque if
            # Arco desde line_to_add a line_if
            graph.add_edge(line_if, line_to_add)
            edge_to_if = True
            end_of_if = line_to_add
            edge_from_if = False
            line_to_add = ''  # Reseteo las lineas a agregar
        # Si se acabo el bloque if y no hay else
        elif if_block and tab_counter(line) == tabs-1:
            if_block = False
            graph.add_node(
                line_to_add
            )  # Agrego las lineas consideradas dentro del bloque if
            # Arco desde line_to_add a line_if
            graph.add_edge(line_if, line_to_add)
            end_of_if = line_to_add
            edge_from_if = False
            line_to_add = line  # Reseteo las lineas a agregar
            tabs = tabs - 1
            line_if = ''
        # Si hay un bloque else activo las lineas deben tener la cantidad de tabs adecuados
        elif else_block and tab_counter(line) == tabs:
            line_to_add += line
        # Si ya no tienen los tabs adecuados reseteo los bloques y las lineas a agregar
        elif else_block and tab_counter(line) == tabs - 1:
            end_of_else = line_to_add
            graph.add_node(line_to_add)
            # Arco desde line_to_add a line_if
            graph.add_edge(line_if, line_to_add)
            edge_to_else = True
            line_to_add = ""
            else_block = False
            tabs = tabs- 1
            line_to_add += line
        # Si la linea es un while
        elif is_while(line) and tab_counter(line)==tabs:
            if_block = False
            else_block = False
            while_block = True
            graph.add_node(line_to_add)
            line_while = line
            graph.add_node(line_while)
            graph.add_edge(line_to_add, line_while)
            edge_from_while = False
            edge_to_while = False
            edge_end_while = False
            line_to_add = ''
            tabs += 1
        elif while_block and tab_counter(line) == tabs-1:
            while_block = False
            graph.add_node(line_to_add)
            graph.add_edge(line_while, line_to_add)
            edge_from_while = True
            graph.add_edge(line_to_add, line_while)
            edge_to_while = True
            line_to_add = line
            tabs = tabs - 1
        # Si no hay ningun bloque if o else simplemente agrego la linea
        else:
            line_to_add += line

    # Finalmente agrego todas las lineas restantes
    if line_to_add != '':
        graph.add_node(line_to_add)
        if else_block:
            end_of_else = line_to_add
        elif while_block:
            end_of_while = line_to_add
        line_to_add == ''
        
    # Confirmamos los arcos de los bloques if/else
    if not edge_from_if:
        if line_to_add == '' or line_to_add == end_of_else: 
            graph.add_edge(end_of_if, 'fin')
        else:
            graph.add_edge(end_of_if, line_to_add)
        edge_from_if = True
    if not edge_from_else:
        if line_to_add == '' or line_to_add == end_of_else: 
            pass
        else:
            graph.add_edge(end_of_else, line_to_add)
        edge_from_else = True
    if not edge_to_if:
        graph.add_edge(line_if, line_to_add)
        edge_to_if = True
    if not edge_to_else:
        graph.add_edge(line_if, line_to_add)
        edge_to_else = True
    if not edge_end_while:
        if line_to_add == '' or line_to_add == end_of_while:
            graph.add_edge(line_while, 'fin')
        else:
            graph.add_edge(line_while, line_to_add)
    if not edge_to_while:
        graph.add_edge(end_of_while, line_while)

    if tab_counter(line_to_add) == 0:
        graph.add_edge(line_to_add, 'fin')

    f.close()
    return graph


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(here, "code_example3.txt")
    graph = generate_graph(filepath)
    print(graph.edges)
