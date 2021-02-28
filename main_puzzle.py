# Solve "Hexa Dowel" puzzle.  For information about the puzzle, see
# https://www.prusaprinters.org/prints/28634#_ga=2.161124414.221543265.1614472305-640152636.1614472305
# Bill Hoff   Feb 2021

# It uses a brute force search.
# Theoretically, the number of steps needed to search every possibility is:
#   There are 12 disks, to be placed in order.
#   Each disk has 2 sides and 6 rotation angles, so there are 12 possible
#   configurations for each disk.
#   For the first position, there are 12 choices for a disk, and for each of
#   those, 12 possible configurations, so 12*12 possibilities.
#   For the second position, there are 11 choices for a disk, and for each of
#   those, 12 possible configurations, so 11*12 possibilities.
#   So, the total number of possibilites for the whole stack is
#       (12*12)(11*12)(10*12) ... (2*12)(1*12) = (12!)(12^12) = 4 x 10^21
#   Which is a lot!
# Fortunately, there seems to be many possible solutions, so the search can
# terminate quite a bit earlier.
import random

# There are 12 disks.  We'll arbitrarily assign ids (0..11) to them.
all_disk_ids = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

# Each disk has a face-up side (0), and a face-down side (1).
# When placed, the disk has a discrete rotation angle (0..5).
# Angles are clockwise with respect to the base stand.

# Each disk has a hole pattern with up to 6 holes.
# A hole is represented by a "1", and a space by a "0".
# These are the patterns, going clockwise from the disk's starting point.
hole_patterns = [
    [0, 1, 0, 1, 1, 1],  # 0
    [1, 1, 0, 1, 1, 0],  # 1
    [1, 1, 1, 0, 0, 1],  # 2
    [1, 0, 0, 0, 1, 1],  # 3
    [0, 1, 0, 1, 0, 1],  # 4
    [1, 0, 0, 1, 0, 0],  # 5
    [1, 1, 1, 1, 1, 1],  # 6
    [1, 0, 0, 0, 1, 0],  # 7
    [0, 1, 0, 1, 1, 0],  # 8
    [1, 0, 0, 0, 0, 0],  # 9
    [0, 0, 0, 0, 1, 1],  # 10
    [1, 1, 0, 1, 1, 1],  # 11
]

# The hole patterns for the face-down sides are the
# reverse of the above.  For example, disk 0 is
#   0, 1, 0, 1, 0, 0        face-up
#   0, 0, 1, 0, 1, 0        face-down

# As each disk is placed on the stack, pegs are placed in the holes.
# A peg occupies 3 consecutive holes.

# A stack is a list of layers, with up to 12 layers.
# Each layer is represented by:
#   (disk id, side, rotation, hole_config, peg_config)
# See below for a description of a peg_config.

number_of_nodes_searched = 0

def main():
    print("Solve disk puzzle")
    disk_ids_used = []
    stack_so_far = []
    explore(disk_ids_used, stack_so_far)

# A hole_config is an array of 6 values (0,1) that are produced
# by taking the hole pattern for the disk with the given id, reversing
# it if it is face-down, and then rotating it by the given value.
def get_hole_config(disk_id, side, angle):
    h = hole_patterns[disk_id]
    if side==1:
        h.reverse()     # Reverse the pattern
    hole_config = h[angle:] + h[:angle]     # Rotate right
    return hole_config

# A stack is a list of up to 11 layers.
# Each layer consists of:
#   peg_config ('p')
#   disk_id ('i')
#   side ('s')
#   angle ('a')
# A peg_config is the same as the hole_config, but where the non-zero
# elements indicate the height of the peg placed in each hole (1,2, or 3).

# To see if a hole_config is compatible with the given stack, do the following.
# Look at the ith position in the hole_config, h_i.
# Look at the ith position in the peg_config in the last layer in the stack, p_i.
# If h_i is 0 (a space)
#   if p_i is 1 or 2
#       then the new layer is not compatible
def compatible(stack, h):
    if len(stack) == 0:
        return True     # This is the first layer
    last_layer = stack[-1]       # Get the last layer in the stack
    p = last_layer['p']
    for i in range(6):
        if h[i] == 0 and (p[i] == 1 or p[i] == 2):
            return False
    return True     # Looks like all positions are compatible

# Compute a new peg_config q from hole_config h, and a previous peg_config p.
# Initialize q = h.
# If h_i is 1 (meaning a hole)
#   q_i = p_i + 1
#   If q_i == 4
#       q_i = 1
def get_peg_config(stack, h):
    q = h
    if len(stack) == 0:
        return q     # This is the first layer
    last_layer = stack[-1]       # Get the last layer in the stack
    p = last_layer['p']
    for i in range(6):
        if h[i] == 1:
            q[i] = p[i] + 1
            if q[i] == 4:
                q[i] = 1
    return q

# This recursive function tries to find a solution, starting from the partial
# solution given by the stack so far and the disks already used.  It terminates
# the program if a solution is found.
def explore(disk_ids_used, stack_so_far):
    global number_of_nodes_searched
    number_of_nodes_searched += 1
    if number_of_nodes_searched % 1000 == 0:
        print(number_of_nodes_searched)

    # # Print stack so far (for debugging)
    # print(number_of_nodes_searched, " ", end='')
    # for layer in stack_so_far:
    #     print(" %d(%d,%d)" % (layer['i'], layer['s'], layer['a']), end='')
    # print("")

    # Create a list of disk ids that we haven't used.
    disk_ids_unused = get_unused(disk_ids_used)

    # Are we done yet?
    if len(disk_ids_unused) == 0:
        if is_solution_valid(stack_so_far):
            # Looks like we found a solution!
            print("\nGot a solution after %d nodes:" % number_of_nodes_searched)
            print("Disks used: ", disk_ids_used)
            for layer in stack_so_far:
                print(layer['i'], " side: ", layer['s'], " angle: ", layer['a'], " pegs: ", layer['p'])
            exit(0)
        return      # Not a valid solution, we need to backtrack

    # Try each possible disk and configuration.
    disk_ids_to_try = disk_ids_unused.copy()
    random.shuffle(disk_ids_to_try)     # Pick disks to try in random order
    for disk_id in disk_ids_to_try:

        sides_to_try = [0, 1]
        random.shuffle(sides_to_try)    # Pick sides to try in random order
        for side in sides_to_try:

            angles_to_try = [0, 1, 2, 3, 4, 5]
            random.shuffle(angles_to_try)   # Pick angles to try in random order
            for angle in angles_to_try:
                hole_config = get_hole_config(disk_id, side, angle)

                if compatible(stack_so_far, hole_config):
                    # The new layer is compatible with the stack so far.
                    # Create the new peg_config for the new layer.
                    peg_config = get_peg_config(stack_so_far, hole_config)

                    # Create the new layer.
                    new_layer = {
                        'p': peg_config,
                        'i': disk_id,
                        's': side,
                        'a': angle
                    }

                    explore(disk_ids_used + [disk_id], stack_so_far + [new_layer])
                else:
                    # No good, don't pursue this line any further.
                    pass

def get_unused(disk_ids_used):
    return [elem for elem in all_disk_ids if not elem in disk_ids_used]

# Check if the stack is a solution.
def is_solution_valid(stack):
    if len(stack) != 12:
        return False

    # We may have a solution; make sure the final layer has no pegs sticking up.
    # That means that its "peg_config" should have only 0's and 3's.
    final_layer = stack[-1]
    p = final_layer['p']
    for i in range(6):
        if not (p[i] == 0 or p[i] == 3):
            return False    # Bad layer, since a peg is sticking up.
    return True

if __name__ == "__main__":
    main()
