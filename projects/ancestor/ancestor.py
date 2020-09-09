
def earliest_ancestor(ancestors, starting_node):

    from util import Queue

    # Parent map is the same as ancestors except edges are reversed, so you can traverse from child to parent
    parent_map = {}
    for i in ancestors:
        parent_map[i[1]] = set() #define set/dictionary with populated keys but empty values
    for i in ancestors:
        parent_map[i[1]].add(i[0]) #populate values for given child keys
    
    # if starting node does not exist in parent-map
    if starting_node not in parent_map:
        return -1

    # List to keep track of path(s) to ancestors. A child may have multiple ancestors
    paths_to_ancestor = []
    visited = set() #paths traveled
    to_visit = Queue()
    to_visit.enqueue([starting_node]) #keep track of path to node + node, since we have to pick the longest path

    while to_visit.size() != 0:
        current_path = to_visit.dequeue()
        current_value = current_path[-1]
        if current_value not in visited:
            visited.add(current_value)
            if current_value not in parent_map:
                paths_to_ancestor.append(current_path)
            else:
                for i  in parent_map[current_value]:
                    # breakpoint()
                    to_visit.enqueue(current_path+[i])
    
    max_lengths = max([len(i) for i in paths_to_ancestor]) #length of the longest path
    
    # Populate ancestors, an array that stores the ancestors corresponding to the longest paths
    ancestors = []
    for i in paths_to_ancestor:
        if len(i) == max_lengths:
            ancestors.append(i[-1])

    # if there are multiple ancestors tied with the same path length, return one with the lowest numeric ID
    return min(ancestors)


# testing
# ancestors = [(1,3),(2,3),(3,6),(5,6),(5,7),(4,5),(4,8),(8,9),(11,8),(10,1)]
# print(earliest_ancestor(ancestors,7 ))
