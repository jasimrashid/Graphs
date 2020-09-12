def bfs(traversal_graphstarting_vertex, destination_vertex):
    visited = set() # will include the path to the last place visited
    vertices_to_visit = Queue()
    vertices_to_visit.enqueue([starting_vertex])
    directions_to_move = []
    current_value_bfs = None

    while vertices_to_visit.size() != 0:
        
        # breakpoint()
        current_including_path = vertices_to_visit.dequeue()
        if len(visited) == 0:
            print('*A')
            current_value_bfs = current_including_path[-1]
        else:
            # if current_value_bfs == 0:
            try:
                current_value_bfs = traversal_graph[current_value_bfs][current_including_path[-1]]
                print('*B', current_including_path,vertices_to_visit.size(),current_value_bfs)
            except:
                print('*B exception')
                breakpoint()
        # breakpoint()
        if current_value_bfs == destination_vertex:
            # breakpoint()
            return current_including_path
        elif current_value_bfs not in visited:
            # breakpoint()
            directions_to_move.append(current_including_path[-1])
            visited.add(current_value_bfs)
            # if current_value_bfs == destination_vertex:
            #     return current_including_path
            # else:
            try:
                print('coding out bfs',player.current_room.id, player.current_room.get_exits(),end=' ')
            except:
                print('bfs error')
                breakpoint()
            # breakpoint()
            for i in player.current_room.get_exits():
                print('i',i, 'exits ', player.current_room.get_exits(), end=' ')
                # new_path = current_including_path
                vertices_to_visit.enqueue(current_including_path+[i])

