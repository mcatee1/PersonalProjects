from collections import deque

# Room and door data
rooms = {
    1: ['White'],
    2: ['Aqua'],
    3: ['Black', 'White'],
    4: ['Pink', 'White'],
    5: ['Yellow', 'Purple'],
    6: ['Magenta'],
    7: ['White', 'Lime'],
    8: ['Black', 'Purple'],
    9: ['Lime'],
    10: ['Yellow', 'Black', 'Blue', 'White'],
    11: [],
    12: ['Pink', 'Gray', 'White'],
    13: ['Magenta', 'White', 'Lime'],
    14: ['Magenta', 'White', 'Lime'],
    15: ['Magenta', 'Green', 'Aqua', 'Orange'],
    16: ['Gray'],
    17: ['Black', 'Magenta'],
    18: ['Lime', 'White'],
    19: ['Magenta', 'Blue', 'White', 'Black', 'Orange'],
    20: ['Purple'],
    21: ['White', 'Pink'],
    22: ['Lime', 'Pink', 'Blue'],
    23: ['Lime', 'Yellow'],
    24: ['Black', 'White']
}

doors = {
    'Magenta': [(1, 2), (2, 3)],
    'Lime': [(2, 5), (6, 9), (9, 10), (19, 20)],
    'White': [(1, 16), (2, 4), (1, 6), (11, 12), (20, 21), (19, 22), (19, 23)],
    'Black': [(3, 5), (9, 11), (9, 10)],
    'Pink': [(6, 18), (10, 12)],
    'Orange': [(1, 19)],
    'Aqua': [(2, 15), (10, 13)],
    'Yellow': [(6, 17), (6, 18), (10, 13)],
    'Gray': [(12, 13), (3, 4), (19, 21), (19, 24)],
    'Purple': [(13, 14), (19, 22)],
    'Blue': [(14, 15)],
    'Green': [(10, 15)],
    'One-way': [(17, 18)]
}

goal_room = 19
goal_player_count = 2

def get_possible_moves(room1, room2, rooms, button_door_map):
    possible_moves = set()

    # Check if room2 has a button matching the color of a door from room1
    for color in rooms[room2]:
        for door in button_door_map.get(color, []):
            if door[0] == room1:  # Two-way door
                possible_moves.add((door[1], room2, color))
            elif door[1] == room1:  # One-way door requiring a button
                possible_moves.add((door[0], room2, color))

    # Check if room1 has a button matching the color of a door from room2
    for color in rooms[room1]:
        for door in button_door_map.get(color, []):
            if door[0] == room2:  # Two-way door
                possible_moves.add((room1, door[1], color))
            elif door[1] == room2:  # One-way door requiring a button
                possible_moves.add((room1, door[0], color))

    # Special handling for one-way doors that do not require a button
    for door in button_door_map.get('One-way', []):
        if door[0] == room1:
            possible_moves.add((door[1], room2, 'One-way'))
        if door[0] == room2:
            possible_moves.add((room1, door[1], 'One-way'))

    return possible_moves

def solve_puzzle(rooms, doors, goal_room):
    solutions = []
    button_door_map = {color: door_list for color, door_list in doors.items()}

    start_state = (1, 1, frozenset([(1, 1)]), [])
    queue = deque([start_state])

    while queue:
        # Dequeue the next state
        current_room1, current_room2, visited_sets, moves = queue.popleft()
        
        # Check if either player has reached the goal room
        if (goal_player_count == 1 and (current_room1 == goal_room or current_room2 == goal_room)) or \
           (goal_player_count == 2 and current_room1 == goal_room and current_room2 == goal_room):
            solutions.append(moves)
            continue

        # Explore all possible moves from the current state
        for next_room1, next_room2, color in get_possible_moves(current_room1, current_room2, rooms, button_door_map):
            new_room_set = (next_room1, next_room2)
            if new_room_set not in visited_sets:
                queue.append((next_room1, next_room2, visited_sets | {new_room_set}, moves + [(current_room1, current_room2, color)]))

    return solutions

valid_moves = solve_puzzle(rooms, doors, goal_room)
for i, move_set in enumerate(valid_moves, 1):
    print("\nSOLUTION", i)
    print(move_set)
