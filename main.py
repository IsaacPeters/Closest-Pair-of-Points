# This main file will run the scripts needed to generate and find the shortest pairs in a variety of data

import os
import time

fileNames = ["hundred", "thousand", "tenThous"]#, "hundoThous"]

# # Generate the files
# for i, name in enumerate(fileNames, start=2):
#         os.system("py generate.py %s %d" % (name, i))

# Run brute force on files
def runPointFinder(scriptName):
        elapsedTimes = []
        for i, name in enumerate(fileNames, start=2):
                for x in range(10):
                        print("%s, file=%s%d, n=%d:" % (scriptName, name, x, i), end=" ")
                        start = time.time()
                        os.system("py %s ./gen/%s%d" % (scriptName, name, x))
                        end = time.time()
                        print("%f\n" % float(end - start))
                        elapsedTimes.append([i, end - start])
        return elapsedTimes

bruteTimes = runPointFinder("bruteforce.py")
with open("output_bruteforceTimes.txt", "w") as file:
        for line in bruteTimes:
                file.write("%d, %f\n" % (10 ** line[0], line[1]))

naiveTimes = runPointFinder("divideandconquer.py")
with open("output_divideandconquerTimes.txt", "w") as file:
        for line in naiveTimes:
                file.write("%d, \t%f\n" % (10 ** line[0], line[1]))