import sys
import math

# Computes distnace between two points, passed in in the form [[x1, y1], [x2, y2]]
def computeDistance(pointPair):

    # Point will come in in the form: [[xint yint], [xint, yint]], need to split this up

    point1 = pointPair[0]
    point2 = pointPair[1]

    #Distance between points P(x1, y1) and Q(x2, y2) is given by: 
    #           sqrt((x2 - x1)^2 + (y2 - y1)^2)
    return math.sqrt(math.pow(int(point2[0]) - int(point1[0]), 2) + math.pow(int(point2[1]) - int(point1[1]), 2))

def merge():
    # Nothing

# Finds closest points in a list of points recursively. Points of form [x, y] given
def recursiveSearchPoints(points):
    if len(points) == 1:
        return points

    # First, find median x coordinate
    median = 0
    for point in points:
        median += point[0]

    # Call this on first and second half, to get lowest points of those halfs, then merge them
    median = len(points) // 2 # half way point in points
    firstHalf = recursiveSearchPoints(points[:m])
    secondHalf = recursiveSearchPoints(points[m:])

    return merge(firstHalf, secondHalf)


if len(sys.argv) != 2: 
    print("Incorrect number of arguments found, should be \"divideandconquer <file>\"")

temp = [line.rstrip('\n') for line in open(sys.argv[1])]
lines = [line.split() for line in temp]

lowestPoints = []
lowestPoints.append([lines[0], lines[1]]) # Give default points, so we have a starting case.
for index1, line1 in enumerate(lines):
    for line2 in lines[index1+1:]:

        if computeDistance([line1, line2]) < computeDistance(lowestPoints[0]):
            # First, clear all elements in our lowestPoints list
            lowestPoints.clear()
            lowestPoints.append([line1, line2])
        elif computeDistance([line1, line2]) == computeDistance(lowestPoints[0]):
            lowestPoints.append([line1, line2])

with open("output_divideandconquer.txt", "w") as file:
    file.write("%f\n" % computeDistance(lowestPoints[0]))
    for point in lowestPoints:
        file.write("%d %d %d %d\n" % (int(point[0][0]), int(point[0][1]), int(point[1][0]), int(point[1][1])))