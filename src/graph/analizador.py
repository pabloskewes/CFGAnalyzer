from src.graph.graph import Graph, ciclomatic_complexity
from src.graph.graph_generator1 import generate_graph
from src.graph.graph_analizer1 import analize_graph

def analizador(file):
    graph = generate_graph(file)
    print('CFG')
    print('Nodos: '+str(graph.num_nodes))
    print('Arcos: '+str(graph.num_edges))
    print('Componentes conexos: 1\n')
    print('Variables indefinidas')
    undef_var, undef_paths = analize_graph(graph)
    for i in range(len(undef_var)):
        print('Variable: '+undef_var[i])
        camino = ''
        for node in undef_paths[i]:
            separated_node = node.split('\n')
            for step in separated_node:
                if step != '':
                    camino += (step.lstrip()+', ')
        print('Camino: '+camino)
    print('\nComplejidad ciclomática')
    print(str(ciclomatic_complexity(graph)))
