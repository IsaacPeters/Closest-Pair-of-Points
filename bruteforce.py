import sys
import math

def computeDistance(pointPair):

    # Point will come in in the form: [[xint yint], [xint, yint]], need to split this up

    point1 = pointPair[0]
    point2 = pointPair[1]

    #Distance between points P(x1, y1) and Q(x2, y2) is given by: 
    #           sqrt((x2 - x1)^2 + (y2 - y1)^2)
    return math.sqrt(math.pow(point2[0] - point1[0], 2) + math.pow(point2[1] - point1[1], 2))

if len(sys.argv) != 2: 
    print("Incorrect number of arguments found, should be \"bruteforce <file>\"")

temp = [line.rstrip('\n') for line in open(sys.argv[1])]
points = []
for line in temp:
    x, y = line.split()
    points.append((int(x), int(y)))



def bruteSort(points):
    lowestPoints = []
    minDist = -1
    for index1, point1 in enumerate(points):
        for point2 in points[index1+1:]:
            distance = computeDistance((point1, point2))
            if minDist < 0:
                minDist = distance
                lowestPoints.append((point1, point2))
            elif distance < minDist:
                # First, clear all elements in our lowestPoints list
                minDist = distance
                lowestPoints.clear()
                lowestPoints.append((point1, point2))
            elif distance == minDist:
                lowestPoints.append((point1, point2))
    return lowestPoints

lowestPoints = bruteSort(points)

with open("output_bruteforce.txt", "w") as file:
    file.write("%f\n" % computeDistance(lowestPoints[0]))
    for point in lowestPoints:
        file.write("%d %d %d %d\n" % (int(point[0][0]), int(point[0][1]), int(point[1][0]), int(point[1][1])))