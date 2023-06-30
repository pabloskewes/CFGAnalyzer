from src.graph.graph import Graph, ciclomatic_complexity, GraphSettings
from src.graph.graph_generator1 import generate_graph
from src.graph.graph_analizer1 import analize_graph
from src.parser.program_parser import ProgramParser
from src.parser.block_parser import ProgramBlock
from typing import List



def node_to_string(parser, node: ProgramBlock, lines: List[str]) -> str:
    if not isinstance(node, ProgramBlock):
        node = parser.node_content[node]
    if node.id < 0:
        return ""
    first_line = node.id
    last_line = node.lines[-1].line_number
    lines = lines[first_line:last_line+1]
    result = '\n'.join(lines).replace('\n\n', '\n')
    return result


def generate_graph_new(file):
    parser = ProgramParser.from_file(file)
    parser.graph.settings = GraphSettings(
        allow_adding_existing_nodes=True,
        allow_adding_edges_to_non_existing_nodes=True,
    )
    parser.populate_graph()

    with open(file, "r") as f:
        program_lines = f.readlines()
    program_lines = [line for line in program_lines if line != '\n']
    
    graph = Graph()
    graph.settings = GraphSettings(
        allow_adding_existing_nodes=True,
        allow_adding_edges_to_non_existing_nodes=True,
    )
    graph.add_node('fin')
    for node in parser.graph.nodes:
        node_str = node_to_string(parser, node, program_lines)
        graph.add_node(node_str)
        
    for source, target in parser.graph.edges:
        graph.add_edge(
            node_to_string(parser, source, program_lines),
            node_to_string(parser, target, program_lines)
        )
        
    last_node = node_to_string(parser, parser.last_node, program_lines)
    graph.add_edge(last_node, 'fin')
    return graph


def analizador(file):
    graph = generate_graph(file)
    print('CFG')
    print('Nodos: '+str(graph.num_nodes))
    print('Arcos: '+str(graph.num_edges))
    print('Componentes conexos: 1\n')
    print('Variables indefinidas')
    undef_var, undef_paths = analize_graph(graph, file)
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
