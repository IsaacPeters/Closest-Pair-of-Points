import sys
import math
from statistics import median
# Computes distnace between two points, passed in in the form [[x1, y1], [x2, y2]]
def computeDistance(pointPair):

    # Point will come in in the form: [[xint yint], [xint, yint]], need to split this up

    point1 = pointPair[0]
    point2 = pointPair[1]

    #Distance between points P(x1, y1) and Q(x2, y2) is given by: 
    #           sqrt((x2 - x1)^2 + (y2 - y1)^2)
    return math.sqrt(math.pow(point2[0] - point1[0], 2) + math.pow(point2[1] - point1[1], 2))

# Taken from bruteforce.py, used to sort groups of 3 items for our recursive approach. 
# This is the base case, in otherwords
def bruteSort(points):
    lowestPoints = []
    for index1, point1 in enumerate(points):
        for point2 in points[index1+1:]:
            if not lowestPoints:
                lowestPoints.append([point1, point2])
            elif computeDistance([point1, point2]) < computeDistance(lowestPoints[0]):
                # First, clear all elements in our lowestPoints list
                lowestPoints.clear()
                lowestPoints.append([point1, point2])
            elif computeDistance([point1, point2]) == computeDistance(lowestPoints[0]):
                lowestPoints.append([point1, point2])
    return lowestPoints

# Will take in all points within the lowest distance found of the median
# Returns the closest pair of points that it finds
def closestCrossPair(points, maxSeperation):
    closestPoints = []
    lowestCross = maxSeperation

    for i, point in enumerate(points[:len(points)-2]):
        j = i + 1
        while j < len(points) and points[j][1] - point[1] <= maxSeperation:
            d = computeDistance([point, points[j]])
            if d < lowestCross:
                closestPoints.clear()
                closestPoints.append([point, points[j]])
            elif d == maxSeperation and not closestPoints:
                closestPoints.append([point, points[j]])
            j = j + 1

    return closestPoints

# Finds closest points in a list of points recursively. Points of form [x, y] given
def recursiveSearchPoints(points):
    # Base case, we only have 3 elements so just find the shortest distance and return it; end here.
    if len(points) <= 3:
        return bruteSort(points)

    # Split array into two halves: we know this is sorted so the median is actually in the middle
    lowPoints = points[:len(points)//2]
    highPoints = points[len(points)//2:]
    if len(points) % 2 == 0:
        middle = (lowPoints[-1][0] + highPoints[0][0]) / 2
    else:
        middle = highPoints[0][0]

    # Call this on first and second half, to get lowest points of those halfs, then merge them
    # This is the recursive part
    leftClosestPoints = recursiveSearchPoints(lowPoints)
    rightClosestPoints = recursiveSearchPoints(highPoints)

    # Calculate distances based off returned closest points
    leftDistance = computeDistance(leftClosestPoints[0])
    rightDistance = computeDistance(rightClosestPoints[0])
    lowestDistance = min(leftDistance, rightDistance)

    # Find all the points within $lowestDistance of the median
    # We can start in the center and work outwards, ezpz
    middlePoints = []
    for point in reversed(lowPoints): # First do the lowest points
        if abs(point[0] - middle) < lowestDistance:
            middlePoints.append(point)
        else:
            break
    for point in highPoints: # Now to highest points
        if abs(point[0] - middle) < lowestDistance:
            middlePoints.append(point)
        else:
            break

    # Sort points near median by y coordinate
    middlePoints.sort(key=lambda x: x[1])

    # Check to see which pair(s) of points is closest, and then return those! woo
    crossPoints = closestCrossPair(middlePoints, lowestDistance)
    if (crossPoints): 
        # We found a crosspoint, we need to check to see if it is shorter than the other points we found
        # It could be the same, which is why we do this.
        if (computeDistance(crossPoints[0]) < lowestDistance):
            return crossPoints
        if (computeDistance(crossPoints[0]) == lowestDistance):
            if (lowestDistance == leftDistance):
                leftClosestPoints.extend(crossPoints)
                return leftClosestPoints
            elif (lowestDistance == rightDistance):
                rightClosestPoints.extend(crossPoints)
                return rightClosestPoints

    # We need to follow the same idea as ^^^ for the left and right, since the left and right branches could
    # have found two pairs of the same distance. Easier for these.
    elif leftDistance == rightDistance:
        leftClosestPoints.extend(rightClosestPoints)
        return leftClosestPoints
    elif leftDistance < rightDistance:
        return leftClosestPoints
    else:
        return rightClosestPoints

# Take input from file
if len(sys.argv) != 2: # Make sure we get a file argument, and only that
    print("Incorrect number of arguments found, should be \"enhanceddnc <file>\"")
temp = [line.rstrip('\n') for line in open(sys.argv[1])]
points = []
for line in temp:
    x, y = line.split()
    points.append((int(x), int(y)))

# First, lets sort this list so that we can do things faster!
# Sorted both by x, then y
points.sort(key = lambda element: (element[0], element[1]))

# Do the search!
closestPoints = recursiveSearchPoints(points)

with open("output_enhanceddnc.txt", "w") as file:
    file.write("%f\n" % computeDistance(closestPoints[0]))
    for point in closestPoints:
        file.write("%d %d %d %d\n" % (point[0][0], point[0][1], point[1][0], point[1][1]))