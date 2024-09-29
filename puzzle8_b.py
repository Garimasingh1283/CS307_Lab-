from collections import defaultdict as dd

class Graph:
    def __init__(self):
        self.graph = dd(list)
        self.parent = dd(int)
        self.distance = dd(int)
        self.frontier = list()

    def initialize_distance(self, node):
        """Sets the distance for a node to -1 (unvisited)."""
        self.distance[node] = -1

    def add_edge(self, u, v):
        """Adds an undirected edge between nodes u and v."""
        self.graph[u].append(v)
        self.graph[v].append(u)

    def construct_path(self, start, goal):
        """Backtracks from the goal node to the start node to create the path."""
        path, current_node = [], goal
        while current_node != start:
            path.append(current_node)
            current_node = self.parent[current_node]
        path.append(start)
        path.reverse()
        return path

    def bfs(self, start, goal):
        """Performs the Breadth-First Search algorithm to find the shortest path."""
        self.distance[start] = 0
        self.frontier.append(start)
        while self.frontier:
            current_node = self.frontier.pop(0)
            for neighbor in self.graph[current_node]:
                if self.distance[neighbor] == -1:  # If the neighbor hasn't been visited
                    self.distance[neighbor] = self.distance[current_node] + 1
                    self.parent[neighbor] = current_node
                    self.frontier.append(neighbor)

        path_distance = self.distance[goal]
        if path_distance != -1:
            path = self.construct_path(start, goal)
        else:
            path = None
        return path, path_distance

def main():
    graph = Graph()
    num_nodes, num_edges = [int(x) for x in input('\nEnter number of nodes and edges: ').split()]
    for i in range(1, num_nodes + 1):
        graph.initialize_distance(i)
    
    print('\n')
    for i in range(num_edges):
        u, v = [int(x) for x in input(f'Enter the start and end nodes of edge {i + 1}: ').split()]
        graph.add_edge(u, v)

    start, goal = [int(x) for x in input('\nEnter the start and goal nodes: ').split()]
    path, distance = graph.bfs(start, goal)
    
    if distance == -1:
        print('\nNo path exists from the start node to the goal node.\n')
    else:
        path_route = ' --> '.join(map(str, path))
        print('\nPath from start node to goal node: ', path_route)
        print('Total path length: ', distance, '\n')

if __name__ == '__main__':
    main()
