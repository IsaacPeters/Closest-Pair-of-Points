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

# Taken from bruteforce.py, used to sort groups of 3 items for our recursive approach. 
# This is the base case, in otherwords
def bruteSort(points):
    lowestPoints = []
    lowestPoints.append([points[0], points[1]]) # Give default points, so we have a starting case.
    for index1, point1 in enumerate(points, start=1):
        for point2 in points[index1+1:]:

            if computeDistance([point1, point2]) < computeDistance(lowestPoints[0]):
                # First, clear all elements in our lowestPoints list
                lowestPoints.clear()
                lowestPoints.append([point1, point2])
            elif computeDistance([point1, point2]) == computeDistance(lowestPoints[0]):
                print("Found equal case!")
                print([point1, point2])
                print("\n")
                lowestPoints.append([point1, point2])
    return lowestPoints

# Will take in all points within the lowest distance found of the median
# Returns the closest pair of points that it finds
def closestCrossPair(points, maxSeperation):
    closestPoints = []
    lowestCross = maxSeperation

    for i, point in enumerate(points[:len(points)-2]):
        j = i + 1
        while j < len(points) and int(points[j][1]) - int(point[1]) <= maxSeperation:
            d = computeDistance([point, points[j]])
            if d < lowestCross:
                closestPoints.clear()
                closestPoints.append([point, points[j]])
            elif d == maxSeperation:
                closestPoints.append([point, points[j]])
            j = j + 1

    return closestPoints

def getMedian(points):
    sortedPoints = sorted(points)
    pointsLength = len(sortedPoints)
    if pointsLength < 1:
        return None

    if pointsLength % 2 == 0:
        return ( int(sortedPoints[pointsLength//2][0]) + int(sortedPoints[(pointsLength//2) - 1][0]) ) / 2
    else:
        return int(sortedPoints[(pointsLength-1) // 2][0])


# Finds closest points in a list of points recursively. Points of form [x, y] given
def recursiveSearchPoints(points):
    if len(points) <= 3:
        return bruteSort(points)

    # First, find median x coordinate
    median = getMedian(points)

    # Split array into two halves based on median
    lowPoints = []
    highPoints = []
    for point in points:
        if int(point[0]) <= median:
            lowPoints.append(point)
        else:
            highPoints.append(point)

    # Call this on first and second half, to get lowest points of those halfs, then merge them
    # This is the recursive part
    leftClosestPoints = recursiveSearchPoints(lowPoints)
    rightClosestPoints = recursiveSearchPoints(highPoints)

    # Calculate distances based off returned closest points
    leftDistance = computeDistance(leftClosestPoints[0])
    rightDistance = computeDistance(rightClosestPoints[0])
    lowestDistance = min(leftDistance, rightDistance)

    # Find all the points within $lowestDistance of the median
    middlePoints = []
    for point in points:
        if abs(int(point[0]) - median) < lowestDistance:
            middlePoints.append(point)

    # Sort points near median by y coordinate
    middlePoints.sort(key=lambda x: x[1])

    # Check to see which pair(s) of points is closest, and then return those! woo
    crossPoints = closestCrossPair(middlePoints, lowestDistance)
    if (crossPoints):
        # if (computeDistance(crossPoints[0]) < lowestDistance):
        print(crossPoints)
        print("\n")
        return crossPoints
        # if (computeDistance(crossPoints[0]) == lowestDistance):
        #     if (lowestDistance == leftDistance):
        #         leftClosestPoints.extend(crossPoints)
        #         return leftClosestPoints
        #     elif (lowestDistance == rightDistance):
        #         rightClosestPoints.extend(crossPoints)
        #         return rightClosestPoints
    elif leftDistance == rightDistance:
        leftClosestPoints.extend(rightClosestPoints)
        return leftClosestPoints
    elif leftDistance < rightDistance:
        return leftClosestPoints
    else:
        return rightClosestPoints

# Take input from file
if len(sys.argv) != 2: # Make sure we get a file argument, and only that
    print("Incorrect number of arguments found, should be \"divideandconquer <file>\"")
lines = [line.rstrip('\n') for line in open(sys.argv[1])]
points = [list(map(int, line.split())) for line in lines]

# Do the search!
closestPoints = recursiveSearchPoints(points)

with open("output_divideandconquer.txt", "w") as file:
    file.write("%f\n" % computeDistance(closestPoints[0]))
    for point in closestPoints:
        file.write("%d %d %d %d\n" % (int(point[0][0]), int(point[0][1]), int(point[1][0]), int(point[1][1])))