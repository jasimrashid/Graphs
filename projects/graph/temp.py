def dfs_rec(graph,start,path = []):
    path = path + [start]
    for edge in graph[start]:
        if edge not in path:
            path = dfs_rec(graph, edge,path)
    return path
graph = {1: [2, 3],
         2: [1, 4, 5, 6],
         3: [1, 4],
         4: [2, 3, 5],
         5: [2, 4, 6],
         6: [2, 5]}

# print('hello')
print(dfs_rec(graph,1,[]))