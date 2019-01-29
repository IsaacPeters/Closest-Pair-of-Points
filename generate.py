import sys
import math
import random

# Figure out what we should name our output file, and how big it should be
if len(sys.argv) != 3: # Make sure we get a file argument, and only that
    print("Incorrect number of arguments found, should be \"generate <file> 10^<x>\"")

for i in range(10):
    with open("./gen/%s%d" % (sys.argv[1], i), "w") as file:
        for x in range(pow(10, int(sys.argv[2]))):
            xNum = random.randint(1, 10000)
            yNum = random.randint(1, 10000)
            file.write("%d %d\n" % (xNum, yNum))