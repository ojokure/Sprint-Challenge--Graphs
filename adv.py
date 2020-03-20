from room import Room
from player import Player
from world import World
import random
from ast import literal_eval
# Load world
world = World()


class Queue():
    def __init__(self):
        self.queue = []

    def enqueue(self, value):
        self.queue.append(value)

    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None

    def size(self):
        return len(self.queue)


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()
player = Player(world.starting_room)
# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

road_map = {}


def traverse(player, moves):

    queue = Queue()
    queue.enqueue([player.current_room.id])

    visited = set()

    while queue.size() > 0:
        route = queue.dequeue()
        last_visited = route[-1]

        if last_visited not in visited:
            visited.add(last_visited)
            edges = road_map[last_visited]
            for edge in edges:
                if road_map[last_visited][edge] == '?':
                    return route
                else:
                    traversed_route = route[:]
                    traversed_route.append(road_map[last_visited][edge])
                    queue.enqueue(traversed_route)
    return []


# Check for exits that haven't been traversed
def unCharted(player, new_moves):
    exits = road_map[player.current_room.id]
    unCharted_route = []

    for direction in exits:
        if exits[direction] == "?":
            unCharted_route.append(direction)

    if len(unCharted_route) == 0:

        # traverse until you find a room with unCharted exits
        untraversed = traverse(player, new_moves)
        new_room = player.current_room.id

        for room in untraversed:
            # in each room, check for untraversed exits and add them to new moves
            for direction in road_map[new_room]:
                if road_map[new_room][direction] == room:
                    new_moves.enqueue(direction)
                    new_room = room
                    break

    # at a random traverse uncharted exit
    else:
        new_moves.enqueue(
            unCharted_route[random.randint(0, len(unCharted_route) - 1)])


# create moves that only use unCharted exits
unCharted_room = {}

for direction in player.current_room.get_exits():

    # add all ? exits to unCharted_room
    unCharted_room[direction] = "?"
    # set the starting room to be an unCharted room
road_map[world.starting_room.id] = unCharted_room

new_moves = Queue()

unCharted(player, new_moves)

reverse_dir = {"n": "s", "s": "n", "e": "w", "w": "e"}

while new_moves.size() > 0:

    start = player.current_room.id
    move = new_moves.dequeue()

    player.travel(move)
    traversal_path.append(move)

    next_room = player.current_room.id
    road_map[start][move] = next_room

    if next_room not in road_map:
        road_map[next_room] = {}

        for exit in player.current_room.get_exits():

            road_map[next_room][exit] = "?"
    road_map[next_room][reverse_dir[move]] = start

    if new_moves.size() == 0:
        unCharted(player, new_moves)


# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)
for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)
if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
