class Node(object):
    
    def __init__(self, parents, children, is_goal=False, name=''):
        """
        :param parents: an iterable of Nodes that have a (directed) edge to this Node
        :param children: an iterable of Nodes to which this Node has a (directed) edge
        :param is_goal: whether, for a given search through a graph, this Node is the goal
        :param name: name of this Node; only used for string representations
        """
        
        self.parents = set(parents)
        self.children = set(children) # so children can also be passed in as a list or tuple
        self.is_goal = is_goal
        self.name = name
        self.path = []
    
    def get_children(self):
        return self.children
    
    def get_parents(self):
        return self.parents
    
    def is_goal_node(self):
        return self.is_goal
    
    def set_goal_status(self, boolean):
        self.is_goal = boolean
    
    def name(self):
        return self.name
    
    def __str__(self):
        return "Node {}; Parents: {}; Children: {}".format(self.name, [parent.name for parent in self.parents],
                                                           [child.name for child in self.children])
    
    def __repr__(self):
        return self.__str__()


# This is essentially just a list of Nodes, as an idea of a simple Graph class
# in real life, you would probably want more functionality like the list of edges as well, the adjacency matrix of the graph,
# ability to compute centralities, etc. There are already libraries for these sort of tasks 
class Graph(object):
    
    def __init__(self, nodes):
        self.nodes = list(nodes)
        self.start_node = None
    
    def __iter__(self):
        for node in self.nodes:
            yield node
    
    def __getitem__(self, index):
        return self.nodes[index] # so you can do graph[i] and get back graph.nodes[i]
    
    def __str__(self):
        return "\n".join(str(node) for node in self.nodes[:5]) + "..."
    
    def __repr__(self):
        return self.__str__()
    
    def __len__(self):
        return len(self.nodes)
    
    def set_goal(self, node_name):
        for node in self.nodes:
            if node.name == node_name:
                node.set_goal_status(True)
                return
        print(f"Node {node_name} was not found!")
    
    def set_start(self, node_name):
        for node in self.nodes:
            if node.name == node_name:
                self.start_node = node
                return
        print(f"Node {node_name} was not found!")


def make_graph(node_map):
    """
    A utility function for creating graphs. In general, one makes a graph from an edge list or an adjacency matrix, but I used a 'node map' here (see example below).
    :param node_map: a dictionary where the keys are the names of nodes from which a graph should be built and the values are tuples where the first element is a list of the parents of the node and the second is a list of the children
    Usage:
    # 'node_name': (parents_list, children_list)
    node_map = {"A": ([], ["B", "C", "D"]), "B": (["A"], ["E", "H"]), "C": (["A"], ["I"]), "D": (["A"], ["G"]), "E": (["B"], ["F"]), "F": (["E"], ["G"]), "G": (["F"], []), "H": (["B"], []), "I": (["C"], [])}
    graph = make_graph(node_map)
    """
    
    # in the map, the nodes are all referenced by name; we need to set the children, etc. to the actual node instances, so first
    # create all the necessary nodes, then update their children/parents
    nodes_by_name = {name: Node([], [], name=name) for name in node_map.keys()}
    
    for name in node_map:
        parents, children = node_map[name]
        node = nodes_by_name[name]
        node.parents = [nodes_by_name[name] for name in parents]
        node.children = [nodes_by_name[name] for name in children]
    
    return Graph(nodes_by_name.values())