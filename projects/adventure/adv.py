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
map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

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

def bfs(starting_vertex, destination_vertex):
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
            current_value_bfs = traversal_graph[current_value_bfs][current_including_path[-1]]
            print('*B', current_including_path,vertices_to_visit.size(),current_value_bfs)
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
            print('coding out bfs',player.current_room.id, player.current_room.get_exits(),end=' ')
            # breakpoint()
            for i in player.current_room.get_exits():
                print('i',i, end=' ')
                # new_path = current_including_path
                vertices_to_visit.enqueue(current_including_path+[i])
                

    # breakpoint()
    # print('you broke free without breakpoint')
    # print(directions_to_move)
    # print(vertices_to_visit)
    

while exit_room == False: #TODO: write out this condition

    print('You are in room', player.current_room.id)

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
        print("You've traversed all points. Here is the path and count so far", traversal_path, move_count)

    # NOT BASE CASE
    else:
        current_room = player.current_room #ADDED!!! REGRESSION TEST
        if player.current_room.get_room_in_direction(move) is None:
            print('Invalid direction')
            break
        else:
            player.travel(move)
        # breakpoint()
        print("You've moved to", player.current_room.id)
        traversal_path.append(move)
        move_count += 1 #delete later
        if player.current_room.id not in traversal_graph: 
            traversal_graph[player.current_room.id] = {}
            for i in player.current_room.get_exits(): 
                traversal_graph[player.current_room.id][i] = '?'
        traversal_graph[current_room.id][move] = player.current_room.id
        traversal_graph[player.current_room.id][opposite[move]] = current_room.id
        current_room = player.current_room
        # if player.current_room.id == 2:
        #     print('break here')
        #     breakpoint()
        # breakpoint()

        # JUNCTION WHERE THERE 2+ AVAILABLE PATHS
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
                # print('moving through, but path bends')
            elif move not in next_moves: #path bends
                move = next_moves[0]
                # print('moving through, but path bends')
            else:
                move = next_moves[0]
                # breakpoint()
            print('Moving',move)

        except Exception: #DEAD END!!!!
            print('Dead end but are there some paths to explore??!!!', 'current room', player.current_room.id)
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

                print("Perform a BFS to '?'")
                return_path = bfs(starting_vertex = player.current_room.id, destination_vertex = '?')[1:]
                print('return path:', return_path)
                while return_path:
                    player.travel(return_path.pop(0))

                # OUT OF BFS. NEXT PATH
                breakpoint()




# breakpoint()
print('===== tests =====')
print('traversal graph', traversal_graph)
print('traversal path', traversal_path)
print('move count', move_count)
print('current room', player.current_room.id)










"""
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


"""