"""
Simple graph implementation
"""
from util import Stack, Queue  # These may come in handy

class Graph:

    """Represent a graph as a dictionary of vertices mapping labels to edges."""
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex_id):
        """
        Add a vertex to the graph.
        """
        self.vertices[vertex_id] = set()

    def add_edge(self, v1, v2):
        """
        Add a directed edge to the graph.
        """
        self.vertices[v1].add(v2)

    def get_neighbors(self, vertex_id):
        """
        Get all neighbors (edges) of a vertex.
        """
        try:
            return self.vertices[vertex_id]
        except Exception:
            return None

    def bft(self, starting_vertex):
        """
        Print each vertex in breadth-first order
        beginning from starting_vertex.
        """
        to_visit = Queue()
        visited = set()

        to_visit.enqueue(starting_vertex)
        # breakpoint()

        while to_visit.size() != 0:
            current = to_visit.dequeue()
            
            if current not in visited:
                print(current)
                visited.add(current)


                for i in self.vertices[current]:
                    to_visit.enqueue(i)
            

    def dft(self, starting_vertex):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.
        """
        to_visit = Stack()
        visited = set()
        to_visit.push(starting_vertex)
        while to_visit.size() != 0:
            current = to_visit.pop()
            if current not in visited:
                print(current)
                visited.add(current)
                for i in self.vertices[current]:
                    to_visit.push(i)

    def dft_recursive(self, starting_vertex):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.

        This should be done using recursion.
        """
        # base case. when a node has no edges that have not already been visited
        # visited = set()
        # if starting node has any edges that]
        visited = set()
        self.dft_recursive_helper(starting_vertex, visited)
        
    def dft_recursive_helper(self, starting_vertex, visited):
        visited.add(starting_vertex)
        print(starting_vertex)#, visited)
        for i in self.vertices[starting_vertex]:
            if i not in visited:
                # print(i)
                visited.add(i)
                self.dft_recursive_helper(i,visited)




        

    def bfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing the shortest path from
        starting_vertex to destination_vertex in
        breath-first order.
        """
        visited = set() # will include the path to the last place visited
        to_visit = Queue()
        to_visit.enqueue([starting_vertex])

        while to_visit.size() != 0:
            
            current_including_path = to_visit.dequeue()
            current_value = current_including_path[-1]
            if current_value not in visited:
                visited.add(current_value)
                if current_value == destination_vertex:
                    return current_including_path
                else:
                    for i in self.vertices[current_value]:
                        # new_path = current_including_path
                        to_visit.enqueue(current_including_path+[i])

            
        

    def dfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.
        """
        visited = set()
        to_visit = Stack()
        to_visit.push([starting_vertex])

        while to_visit.size() != 0:
            current_including_path = to_visit.pop()
            current_value  = current_including_path[-1]
            if current_value not in visited:
                visited.add(current_value)
                if current_value == destination_vertex:
                    return current_including_path
                else:
                    for i in self.vertices[current_value]:
                        to_visit.push(current_including_path+[i])

    def dfs_recursive(self, starting_vertex, destination_vertex):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.

        This should be done using recursion.
        """
        visited = set()
        return_values = []
        return_values.append(self.dfs_recursive_helper([starting_vertex],destination_vertex,visited, return_values))
        result = None
        # breakpoint()
        for i in return_values:
            if i is not None:
                result = i
        # print(result)
        return result
        # print(return_values)
        # for i in return_values:
        #     if i is not None:
        #         return return_values

        # return self.dfs_recursive_helper([starting_vertex],destination_vertex,visited)

    def dfs_recursive_helper(self, starting_vertex, destination_vertex, visited, return_values):
        

        # if starting_vertex[-1] in visited:
        # visited.add(starting_vertex[-1])
        # print('s:', starting_vertex,'d:', destination_vertex,'v:',visited)
        # if starting_vertex[-1] == destination_vertex:
        #     return starting_vertex
        #     print('no match: ',end=' ')
        # for i in self.vertices[starting_vertex[-1]]:
        #     print('c: ',i)
        #     if i not in visited:
        #         return self.dfs_recursive_helper(starting_vertex+[i],destination_vertex,visited)
        return_value = None
        if starting_vertex[-1] not in visited:
            visited.add(starting_vertex[-1])
            # print('s:', starting_vertex,'d:', destination_vertex,'v:',visited)
            if starting_vertex[-1] == destination_vertex:
                return_value = starting_vertex
                # print('match: ',end=' ')
                # print('returning matched value!!!!', return_value)
                # return return_value
            else:
                for i in self.vertices[starting_vertex[-1]]:
                    # print('c: ',i)
                    if i not in visited:
                        return_value =  self.dfs_recursive_helper(starting_vertex+[i],destination_vertex,visited, return_values)
                        # return self.dfs_recursive_helper(starting_vertex+[i],destination_vertex,visited)
                    else:
                        return_value = None
                        # return None
        # print('**',return_value)
        return_values = return_values.append(return_value)





    # def dfs_recursive(self, starting_vertex, destination_vertex):
        

    # def get_next_parent(self, vertex, visited):
    #     vertices = self.vertices[vertex]
    #     for i in vertices:
    #         return i if i not in visited else None
        
        

            

        

if __name__ == '__main__':
    graph = Graph()  # Instantiate your graph
    # https://github.com/LambdaSchool/Graphs/blob/master/objectives/breadth-first-search/img/bfs-visit-order.png
    graph.add_vertex(1)
    graph.add_vertex(2)
    graph.add_vertex(3)
    graph.add_vertex(4)
    graph.add_vertex(5)
    graph.add_vertex(6)
    graph.add_vertex(7)
    graph.add_edge(5, 3)
    graph.add_edge(6, 3)
    graph.add_edge(7, 1)
    graph.add_edge(4, 7)
    graph.add_edge(1, 2)
    graph.add_edge(7, 6)
    graph.add_edge(2, 4)
    graph.add_edge(3, 5)
    graph.add_edge(2, 3)
    graph.add_edge(4, 6)

    # print(graph.get_neighbors(4))
    # print(graph.get_neighbors(8))

    '''
    Should print:
        {1: {2}, 2: {3, 4}, 3: {5}, 4: {6, 7}, 5: {3}, 6: {3}, 7: {1, 6}}
    '''
    print('vertices')
    print(graph.vertices)

    '''
    Valid BFT paths:
        1, 2, 3, 4, 5, 6, 7
        1, 2, 3, 4, 5, 7, 6
        1, 2, 3, 4, 6, 7, 5
        1, 2, 3, 4, 6, 5, 7
        1, 2, 3, 4, 7, 6, 5
        1, 2, 3, 4, 7, 5, 6
        1, 2, 4, 3, 5, 6, 7
        1, 2, 4, 3, 5, 7, 6
        1, 2, 4, 3, 6, 7, 5
        1, 2, 4, 3, 6, 5, 7
        1, 2, 4, 3, 7, 6, 5
        1, 2, 4, 3, 7, 5, 6
    '''
    
    print('bft 1')
    graph.bft(1)

    # '''
    # Valid DFT paths:
    #     1, 2, 3, 5, 4, 6, 7
    #     1, 2, 3, 5, 4, 7, 6
    #     1, 2, 4, 7, 6, 3, 5
    #     1, 2, 4, 6, 3, 5, 7
    # '''
    print('dft 1')
    graph.dft(1)

    print('dft recursive 1')
    graph.dft_recursive(1)

    # '''
    # Valid BFS path:
    #     [1, 2, 4, 6]
    # '''
    print('bfs 1,6')
    print(graph.bfs(1, 6))

    # '''
    # Valid DFS paths:
    #     [1, 2, 4, 6]
    #     [1, 2, 4, 7, 6]
    # '''
    print('dfs')
    print(graph.dfs(1, 6))
    # breakpoint()
    print('dfs recursive')
    print(graph.dfs_recursive(1, 6))
