def findOutput(planeInfo, index, result, curRes, listL, listG, listT):
    if len(result) != 0:
        return
    if checkValid(listL, listG, listT) is False:
        return
    if index == len(planes):
        result.append(curRes[:])
        return
    plane = planeInfo[index]
    planeId = plane[0]
    R = int(plane[1])
    M = int(plane[2])
    S = int(plane[3])
    O = int(plane[4])
    C = int(plane[5])
    for x in xrange(0, R + 1):
        for y in xrange(x + M + S, x + M + C + 1):
            # next level
            curRes.append([planeId, x, y])
            listL.append([x, x + M])
            listG.append([x + M, y])
            listT.append([y, y + O])
            findOutput(planeInf, index + 1, result, curRes, listL, listG, listT)
            # backtrack
            curRes = curRes[:-1]
            listL = listL[:-1]
            listG = listG[:-1]
            listT = listT[:-1]


def checkValid(listL, listG, listT):
    if checkHelper(listL, L) is False:
        return False
    if checkHelper(listG, G) is False:
        return False
    if checkHelper(listT, T) is False:
        return False
    return True


# refer to a Leetcode problem to find minimum Meeting Rooms
def checkHelper(aList, capacity):
    start = []
    end = []
    for interval in aList:
        start.append(interval[0])
        end.append(interval[1])
    start.sort()
    end.sort()
    s = e = 0
    needed = available = 0
    while s < len(start):
        if start[s] < end[e]:
            if available == 0:
                needed += 1
            else:
                available -= 1
            s += 1
        else:
            available += 1
            e += 1
    if needed > capacity:
        return False
    else:
        return True


if __name__ == "__main__":
    inputFile = open('input.txt', 'r')
    lines = []
    for line in inputFile.readlines():
        lines.append(line)
    L = int(lines[0].strip().split()[0])
    G = int(lines[0].strip().split()[1])
    T = int(lines[0].strip().split()[2])
    N = int(lines[1].strip())
    planes = []
    for i in range(N):
        planes.append(lines[i + 2].strip().split())
    # ------
    planeId = 0
    planeInfo = []
    for line in lines[2:]:
        oneLine = line.strip().split()
        parDict = []
        parDict.append(planeId)
        parDict.append(int(oneLine[0]))
        parDict.append(int(oneLine[1]))
        parDict.append(int(oneLine[2]))
        parDict.append(int(oneLine[3]))
        parDict.append(int(oneLine[4]))
        planeInfo.append(parDict[:])
        planeId += 1
    planeInf = sorted(planeInfo, key=lambda x: (int(x[1]) + int(x[2])))
    # -------
    result = []
    findOutput(planeInf, 0, result, [], [], [], [])
    print(result)
    result = sorted(result[0], key=lambda x: x[0])
    output = open("output.txt", "w")
    for i in range(len(result)):
        output.write(str(result[i][1]) + " " + str(result[i][2]) + "\n")
    output.close()
