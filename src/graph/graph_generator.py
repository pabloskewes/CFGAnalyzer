import os
from graph import Graph

def has_tab(line):
    line_list = list(line)
    if line_list[0:4]==[' ',' ',' ',' ']:
        return True
    else:
        return False
    
def tab_counter(line):
    line_list = list(line)
    tabs = 0
    i = 0
    while i < len(line_list):
        if line_list[i:i+4]==[' ',' ',' ',' ']:
            tabs += 1
        else:
            pass
        i += 4
    return tabs

def is_if(line):
    line_list = list(line.lstrip())
    if line_list[0:2]==['i','f']:
        return True
    else:
        return False
    
def is_while(line):
    line_list = list(line.lstrip())
    if line_list[0:5]==['w','h','i','l','e']:
        return True
    else:
        return False
    
def is_else(line):
    line_list = list(line.lstrip())
    if line_list[0:4]==['e','l','s','e']:
        return True
    else:
        return False
    
here = os.path.dirname(os.path.abspath(__file__))

filename = os.path.join(here, 'code_example1.txt')
f = open(filename, 'r')

graph = Graph()

line_to_add = ''
line_if = ''
line_else = ''
line_while = ''
main_line = ''
if_block = False
else_block = False
while_block = False
tabs = 0

for line in f:
    # Veo si la linea es un if
    if is_if(line):
        if_block = True
        else_block = False
        line_if = (line_to_add+line+'\n') # Agrego la linea al nodo por agregar
        graph.add_node(line_if) # Agrego el nodo
        tabs += 1 # Aumento el numero de tabs necesario para estar en el bloque
    # Si hay un bloque if activo las lineas deben tener la cantidad de tabs adecuadas
    if if_block and tab_counter(line)==tabs:
        line_to_add += (line+'\n') # Agrego cada linea dentro del bloque al bloque por agregar
    # Veo si la linea es un else y tiene un tab menos q los necesarios para estar dentro del bloque
    if is_else(line) and tab_counter(line)==tabs-1:
        if_block = False 
        else_block = True
        graph.add_node(line_to_add) # Agrego las lineas consideradas dentro del bloque if
        # Arco desde line_to_add a line_if
        line_to_add = '' # Reseteo las lineas a agregar
    # Si hay un bloque else activo las lineas deben tener la cantidad de tabs adecuados
    if else_block and tab_counter(line)==tabs:
        line_to_add += (line+'\n')
    # Si ya no tienen los tabs adecuados reseteo los bloques y las lineas a agregar
    if else_block and tab_counter(line)==tabs-1:
        graph.add_node(line_to_add)
        # Arco desde line_to_add a line_if
        line_to_add = ''
        else_block = False
        tabs -= 1
        line_to_add += (line+'\n')
    # Si no hay ningun bloque if o else simplemente agrego la linea
    else:
        line_to_add += (line+'\n')
# Finalmente agrego todas las lineas restantes
graph.add_node(line_to_add)


f.close()