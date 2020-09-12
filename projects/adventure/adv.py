from room import Room
from player import Player
from world import World
from util import Queue #for DFS

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

traversal_graph = {}
visited_rooms = set()
traversal_path = []

player.current_room = world.starting_room
order_of_rooms =  ['n','s','w','e'] #configurable
# order_of_rooms_density_weighted = None #TBA
move_count = 0 #may later delete
opposite = {'n':'s','s':'n','w':'e','e':'w'}
current_room = player.current_room #keep this to use in next move
traversal_graph[current_room.id] = {}
for i in current_room.get_exits():
    traversal_graph[current_room.id][i] = '?'

# move = random available direction from above
# Pick random direction A: in order of n > s > w > e
move = 'n' #initial static direction TODO implement above
retrace_point = None
retrace_direction = None

traversed_all_paths = False #Base case condition
exit_room = False

def bfs(graph, starting_vertex, destination_vertex):
    visited = set() # will include the path to the last place visited
    vertices_to_visit = Queue()
    directions_to_move = Queue()
    vertices_to_visit.enqueue([starting_vertex])
    directions_to_move.enqueue([starting_vertex])
    current_value_bfs = None
    last_move_direction = None

    graph_reverse_map = {}
    for k1,v1 in graph.items():
        # breakpoint()
        graph_reverse_map[k1] = {}
        for k2,v2 in v1.items():
            graph_reverse_map[k1][v2] = k2

    while vertices_to_visit.size() != 0:

        current_including_path = vertices_to_visit.dequeue()
        dirmove = directions_to_move.dequeue()
        current_value_bfs = current_including_path[-1]

        if current_value_bfs not in visited:
            visited.add(current_value_bfs)
            if current_value_bfs == destination_vertex:
                return_path = []
                for i in range(len(current_including_path)-1):   
                    return_path.append(graph_reverse_map[current_including_path[i]][current_including_path[i+1]])
                return_path[-1]=dirmove[-1]

                return current_including_path, return_path
            else:
                for i in world.rooms[current_value_bfs].get_exits():
                    if graph[current_value_bfs][i] not in visited:
                        directions_to_move.enqueue(current_including_path+[i])
                        vertices_to_visit.enqueue(current_including_path+[graph[current_value_bfs][i]])
                        # print(f"cvbfs {current_value_bfs} i: '{i}' queue: {vertices_to_visit.queue}", end=' ',)

        # print('cv:',current_value_bfs, 'visited',visited)
        


# #TEST OUT BFS
# #PROVIDE 3 SCNEARIOS. RETURN CORRECT PATH

# # went up dead end
# test_graph_1 = {0: {'n': 1, 's': '?', 'w': '?', 'e': '?'}, 
# 1: {'n': 2, 's': 0}, 
# 2: {'s': 1}}
# #actual output = [2, 's', 's', 's']

# # went down up dead end, went down
# test_graph_2 = {0: {'n': 1, 's': 5, 'w': '?', 'e': '?'}, 
# 1: {'n': 2, 's': 0}, 
# 2: {'s': 1}, 
# 5: {'n': 0, 's': 6}, 
# 6: {'n': 5}}

# test_graph_3 = {0: {'n': 1, 's': 5, 'w': 7, 'e': '?'}, 
# 1: {'n': 2, 's': 0}, 
# 2: {'s': 1}, 
# 5: {'n': 0, 's': 6}, 
# 6: {'n': 5},
# 7: {'w':'?','e':0}}


# print(bfs(test_graph_1, 2,'?'))
# print()
# #actual output = [2, 's', 's', 's']

# print(bfs(test_graph_2, 6,'?'))
# print()
# # actual output = [6, 'n', 'n', 'w']

# print(bfs(test_graph_3, 6,'?'))
# print()
# # actual output = [6, 'n', 'n', 'w']




while exit_room == False: #TODO: write out this condition

    # print('You are in room', player.current_room.id,end=' ')

    count = 0
    for k1,v1 in traversal_graph.items():
        for k2,v2 in v1.items():
            if v2=='?':
                count += 1

    # if player.current_room.id == 2:
    #     breakpoint()

    # BASE CASE TEST
    if traversed_all_paths == True:
        exit_room = True
        # print("You've traversed all points. Here is the path and count so far", traversal_path, move_count)

    # NOT BASE CASE
    else:
        current_room = player.current_room #ADDED!!! REGRESSION TEST
        if player.current_room.get_room_in_direction(move) is None:
            # print('Invalid direction')
            breakpoint()
        else:
            player.travel(move)
        # print(". You've moved to room", player.current_room.id,'.',end=' ')
        traversal_path.append(move)
        move_count += 1 #delete later
        if player.current_room.id not in traversal_graph: 
            traversal_graph[player.current_room.id] = {}
            for i in player.current_room.get_exits(): 
                traversal_graph[player.current_room.id][i] = '?'
        traversal_graph[current_room.id][move] = player.current_room.id
        traversal_graph[player.current_room.id][opposite[move]] = current_room.id
        current_room = player.current_room
        try:
            next_moves = [k for (k,v) in traversal_graph[current_room.id].items() if v == '?'] #if this is non-empty    
            # if path direction changes
            if move not in next_moves and len(next_moves) >= 2:
                move = next_moves[0]        
                retrace_direction = next_moves[1]
                retrace_point = current_room.id
            elif move in next_moves and len(next_moves) >= 2:
                temp = set(next_moves) - set(move)
                retrace_direction = [i for i in temp][0] #this is a direction
                retrace_point = current_room.id
            else:
                move = next_moves[0]
                # breakpoint()
            # print('Moving',move)

        except Exception: #DEAD END!!!!
            # print('Dead end but are there some paths to explore??!!!', 'current room', player.current_room.id)
             # BFS implementation -> without re-using any existing objects / for simplicity
            
            # traversed all paths? if yes, stop. else. BFS to '?'
            count = 0
            # breakpoint()
            for k1,v1 in traversal_graph.items():
                for k2,v2 in v1.items():
                    if v2=='?':
                        count += 1

            if count == 0:
                traversed_all_paths = True
                exit_room = True
            else:

                # print("Perform a BFS to '?'")
                # try:
                return_path = bfs(traversal_graph.copy(), starting_vertex = player.current_room.id, destination_vertex = '?')[1]

                # breakpoint()
                # except:
                #     print('handle!')
                #     breakpoint()
                # print('return path:', return_path)
                # breakpoint()
                temp_room = None
                bfs_room = None
                while len(return_path) != 0:
                    try:
                        temp_room = player.current_room
                        bfs_move = return_path.pop(0)
                        player.travel(bfs_move)
                        if player.current_room.id in traversal_graph: #not exited yet:
                            traversal_graph[temp_room.id][bfs_move] = player.current_room.id
                            traversal_graph[player.current_room.id][opposite[bfs_move]] = temp_room.id
                        traversal_path.append(bfs_move)
                        move_count += 1 #delete later
                    except Exception:
                        print('exception')
                        breakpoint()

                # OUT OF BFS. NEXT PATH. MOVE WILL BE NEXT AVAILABLE EXIT / REPEAT LOGIC IN BEGNNING


                # GET NEXT MOVE
                current_room = player.current_room #ADDED!!! REGRESSION TEST
                # if player.current_room.get_room_in_direction(move) is None:
                #     print('Invalid direction')
                #     break
                # else:
                #     player.travel(move)
                # breakpoint()
                # print("You've moved to", player.current_room.id)
                # traversal_path.append(move)
                # move_count += 1 #delete later
                if player.current_room.id not in traversal_graph: 
                    traversal_graph[player.current_room.id] = {}
                    for i in player.current_room.get_exits(): 
                        traversal_graph[player.current_room.id][i] = '?'
                # breakpoint()
                # traversal_graph[current_room.id][move] = player.current_room.id
                traversal_graph[temp_room.id][bfs_move] = player.current_room.id
                traversal_graph[player.current_room.id][opposite[bfs_move]] = temp_room.id
                current_room = player.current_room
                next_moves = [k for (k,v) in traversal_graph[player.current_room.id].items() if v == '?']
                # breakpoint()
                try:
                    move = next_moves.pop(0)
                except: #DEAD END TO DEAD END EXCEPTION. HERE JUST FORCE A MOVE. LATER DO A COUNT CHECK. THIS COULD BE THE LAST STEP IN GAME.AND YOU'LL END PREMATURELY
                    move = player.current_room.get_exits()[0]
                    # print('dead end exception', player.current_room.id,'Moving:',move)




# breakpoint()
print('===== tests =====')
print('traversal graph', traversal_graph)
print('traversal path', traversal_path)
print('move count', move_count)
print('current room', player.current_room.id)











# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    elif cmds[0] == 'break':
        breakpoint()
    else:
        print("I did not understand that command.")


