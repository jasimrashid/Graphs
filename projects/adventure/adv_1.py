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
map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']

# KEY: think of drawing a map as you go along
traversal_graph = {}
visited_rooms = set()
traversal_path = []

# general logic

# store anticipated direction/move and current room as temporary variables
# construct traversal_graph initial entry: {0:{'n':'?','s':'?','w':'?','e':'?'}
# pick a **random** direction to move ('next_direction' or 'move'). set 'current_room_temp' to 'current_room'
# TRAVERSAL: while you haven't explored all paths
#       player.travel(move)
#       store move into traversal_path
#       add dictionary entry for room, filling it up based on where you were previously
#       if dead end: then travel to next open path **** e.g. based on BFS last node you passed which had an open path
#       else: keep traveling in direction that was decided 


# plan: 1. write up the logic for moving in one random direction until a dead end
# 2. DFS search.... 

player.current_room = world.starting_room
order_of_rooms =  ['n','s','w','e'] #configurable
order_of_rooms_density_weighted = None #TBA
move_count = 0 #may later delete
opposite = {'n':'s','s':'n','w':'e','e':'w'}
current_room = player.current_room #keep this to use in next move
# traversal_graph[current_room]
traversal_graph[current_room.id] = {}
for i in current_room.get_exits():
    traversal_graph[current_room.id][i] = '?'
# move = random available direction from above
# Pick random direction A: in order of n > s > w > e
move = 'w' #TODO implement above
retrace_point = None
retrace_direction = None
test = None
# move = [k for (k,v) in traversal_graph[current_room.id].items() if v == '?'][0] #if this is non-empty

exit_room = False
while exit_room == False: #TODO: write out this condition
    player.travel(move)
    traversal_path.append(move)
    move_count += 1 #delete later
    if player.current_room.id not in traversal_graph: 
        traversal_graph[player.current_room.id] = {}
        for i in player.current_room.get_exits(): 
            traversal_graph[player.current_room.id][i] = '?'
    # traversal_graph[player.current_room.id] = {'n': '?', 's': '?', 'w': '?', 'e': '?'}
    
    traversal_graph[current_room.id][move] = player.current_room.id
    traversal_graph[player.current_room.id][opposite[move]] = current_room.id
    current_room = player.current_room

    # JUNCTION WHERE THERE 2+ AVAILABLE PATHS
    try:
        # move = [k for (k,v) in traversal_graph[current_room.id].items() if v == '?'][0] #if this is non-empty
        next_moves = [k for (k,v) in traversal_graph[current_room.id].items() if v == '?'] #if this is non-empty
        
        # if path direction changes
        if move not in next_moves and len(next_moves) >= 2:
            move = next_moves[0]
            
            # pre
            # retrace_point = next_moves[1]
            # retrace_point = current_room.get_room_in_direction(retrace_point).id
            
            retrace_direction = next_moves[1]
            # retrace_direction = current_room.get_room_in_direction(retrace_direction).id
            retrace_point = current_room.id
            
        elif move not in next_moves: #path bends
            move = next_moves[0]
        elif move in next_moves and len(next_moves) >= 2:
            # retrace_point = next_moves
            # move remains the same
            temp = set(next_moves) - set(move)
            retrace_direction = [i for i in temp][0] #this is a direction
            # retrace_direction = current_room.get_room_in_direction(retrace_direction).id
            retrace_point = current_room.id
            # breakpoint()


    except Exception:
        print('Dead end!!!', 'retrace point', retrace_point, test)
        # breakpoint()
        if retrace_point is None:
            exit_room = True
        else:
            # move = retrace_point #TODO check if this is redundant
            print('retrace')
            print('BFS to retrace point', retrace_point)

            # breakpoint()
            
            # BFS implementation -> without re-using any existing objects / for simplicity
            visited = set()
            to_visit = Queue()
            to_visit.enqueue([current_room.id]) #removing dot
            # to_visit.enqueue([current_room]) #removing dot
            while to_visit.size() != 0:
                # breakpoint()
                current_path = to_visit.dequeue()
                # current_value = current_path[-1]
                next_value = current_path[-1]
                if len(visited) != 0: #first time here. dont move player forward
                    # current_path = to_visit.dequeue()
                    next_value = current_path[-1] #next value
                    # get direction/key  to move, given the value/next_value
                    next_direction = [k for k,v in traversal_graph[current_value].items() if v==next_value][0]
                    player.travel(next_direction)
                    current_value = next_value
                    breakpoint()
                else: #TODO some redundant code here
                    current_path = to_visit.dequeue()
                    current_value = current_path[-1]
                    # current_room = current_value #TODO: redundant code --> reverse into player.current_room given index

                
                if current_value not in visited:
                    visited.add(current_value)
                    # if current_value == retrace_point: #move in direction of retrace_direction
                    if current_value == retrace_point: #move in direction of retrace_direction #added dot
                        # move in the direction of retrace. we assume the queue is empty and this while loop ends
                        print("you're back in action")
                        move = retrace_direction #next step will be line 73
                        breakpoint()
                        # breakpoint()
                    else:
                        for (k,v) in traversal_graph[current_value].items():
                            # breakpoint()
                            to_visit.enqueue(current_path+[v]) #YOU DONT NEED THE PATH!!!!!
                            print('okaayyyyy')
                            # breakpoint()





            # retrace_point = None

            #DST to retrace point
    
    # if current_room.id == 2:
    #     exit_room = True


# breakpoint()
print(traversal_graph)
print(traversal_path)
print(move_count)
print(current_room)










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