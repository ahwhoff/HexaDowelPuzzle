# HexaDowelPuzzle

This is a python program I wrote to solve the "Hexa Dowel" puzzle.  The "Hexa Dowel" puzzle
(see [Hexa Dowel Puzzle](https://www.prusaprinters.org/prints/28634#_ga=2.161124414.221543265.1614472305-640152636.1614472305))
is a set of 12 plastic hexagon-shaped disks, with holes in them.  There are 13 pegs (dowels) that you have to
put in the holes.  The goal is to stack the disks up, filling the holes with the pegs as you go, such that at
the end, all holes are filled.

![alt text](https://github.com/ahwhoff/HexaDowelPuzzle/blob/master/puzzle.png?raw=true)

The puzzle is challenging!  Rather than solving it manually, by trial and error, I thought it would be more
fun to write a program to solve it (plus, gives me some coding practice).  So, the rest of this description is
a description of the program and my experiences with running it.

:

## *STOP HERE, IF YOU WANT TO SOLVE THE PUZZLE YOURSELF!*

:

My first thought was to write a simple program that does a brute force search of all possible configurations
of the stack of disks.  A brute force program is not practical if there are a lot of possible configurations
to search, and there is only one (or very few) solutions, so that you end up searching a lot of possibilites.
However, I thought that it would be quick to write such a program, and I would also find out quickly if the
program would find a solution in a reasonable time.

The simple brute force program tries to create a stack of disks, one layer at a time, filling the holes with
the pegs as it goes.  When adding a layer to an existing stack, you can check whether the new layer is
compatible with the existing stack.  Namely, if any pegs are sticking up from the stack, the new layer must
have holes in those positions.  The final layer should have no pegs sticking up from it.  The correct solution has
every hole filled, and all pegs are used.

### Complexity

There are a lot of possible configurations to search! 
* There are 12 disks, to be placed in order.
* Each disk has 2 sides and 6 rotation angles, so there are 12 possible configurations for each disk.
* For the first layer, there are 12 choices for a disk to use, and for each of those, 
12 possible configurations, so 12x12 possibilities.
* For the second layer, there are 11 choices for a disk, and for each of those, 12 possible 
configurations, so 11x12 possibilities.

So, the total number of possibilites for the whole stack is
(12x12)(11x12)(10x12) ... (2x12)(1x12) = (12!)(12^12) = 4 x 10^21

This is a lot of possibilities!  It might take forever to run!

### Results
Fortunately, there seems to be many possible solutions, so the search can terminate quite a bit earlier
than exploring all possible configurations.  My program randomly chooses disk, angle, and side for each
layer.  The first time I ran it, it found a solution after  12234 steps.  The next time, it took 810598 
steps (this still takes only about 10 seconds to run).
I ran it 10 times, and the following are the number of steps required:
* 12234
* 810598
* 16116
* 2325
* 15753
* 6110
* 631037
* 685195
* 50430
* 30111

Each time the program finds a solution, it prints out the stack and terminates.  The following
is the output for the last run (the numbering of disks is arbitrary):
```
Got a solution after 30111 nodes:
Disks used:  [10, 1, 6, 2, 5, 3, 0, 11, 8, 4, 7, 9]
10  side:  1  angle:  2  pegs:  [0, 0, 0, 0, 1, 1]
1  side:  1  angle:  0  pegs:  [0, 1, 1, 0, 2, 2]
6  side:  1  angle:  3  pegs:  [1, 2, 2, 1, 3, 3]
2  side:  0  angle:  5  pegs:  [2, 3, 3, 2, 0, 0]
5  side:  0  angle:  3  pegs:  [3, 0, 0, 3, 0, 0]
3  side:  0  angle:  5  pegs:  [1, 1, 0, 0, 0, 1]
0  side:  0  angle:  4  pegs:  [2, 2, 0, 1, 0, 2]
11  side:  0  angle:  0  pegs:  [3, 3, 0, 2, 1, 3]
8  side:  1  angle:  4  pegs:  [1, 0, 0, 3, 2, 0]
4  side:  0  angle:  3  pegs:  [2, 0, 1, 0, 3, 0]
7  side:  0  angle:  4  pegs:  [3, 0, 2, 0, 0, 0]
9  side:  1  angle:  3  pegs:  [0, 0, 3, 0, 0, 0]
```

Here is a picture of one of the solutions:

![alt text](https://github.com/ahwhoff/HexaDowelPuzzle/blob/master/solved_puzzle.jpg?raw=true)

