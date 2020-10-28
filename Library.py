import cv2
import numpy as np
import cv2.aruco as aruco
from math import *
from time import *
global n
n = 9

def getPos(cap, rng, ser):
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_1000)
    parameters = aruco.DetectorParameters_create()
    while True:
        print("Checking Aruco")
        _, frame = cap.read()
        print("A")
        frame = frame[int(rng[1]): int(rng[1] + rng[3]), int(rng[0]): int(rng[0] + rng[2])]
        print("B")
        frame = cv2.resize(frame, (n * 100, n * 100))
        print("c")
        corners, ids, _ = aruco.detectMarkers(frame, aruco_dict, parameters=parameters)
        print("D")
        if len(corners) != 0:
            print("E")
            break
        ser.write(b's')
    pos = [(corners[0][0][0][0] + corners[0][0][2][0])//2, (corners[0][0][0][1] + corners[0][0][2][1])//2]
    vect = [(corners[0][0][0][0] - corners[0][0][3][0]), (corners[0][0][0][1] - corners[0][0][3][1])]
    i, j = pos[0]//100, pos[1]//100
    pn = n*j + i
    print("got")
    return pos, vect, int(pn)

def getProp(img):
    l, w = img.shape[:2]
    print("dimenion",l,w)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    bgrmin = np.array([5, 5, 5])
    bgrmax = np.array([100, 100, 100])
    redmin = np.array([0, 70, 60])
    redmax = np.array([10, 255, 255])
    yellowmin = np.array([20, 100, 100])
    yellowmax = np.array([50, 255, 255])
    bluemin = np.array([79, 106, 144])
    bluemax = np.array([122, 169, 198])
    centres = []
    shacol = []
    """0 - Red Circle 
        1 - Red Square
        2 - Yellow Circle
        3 - Yellow Square
        5 - Prison
        6 - Death Eater
        4 - Weapon"""
    for i in range(0, 81):
        for j in range(0, 81):
            count = 0
            imcrop = img[i * l // 9:(i + 1) * l // 9, j * w // 9:(j + 1) * w // 9]
            threshold = cv2.inRange(imcrop, bgrmin, bgrmax)
            result = cv2.bitwise_not(threshold)
            kernel = np.ones((3, 3), np.uint8)
            result = cv2.erode(result, kernel, iterations=2)
            result = cv2.dilate(result, kernel, iterations=2)
            _, contours, _ = cv2.findContours(result, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            threshred = cv2.inRange(imcrop, redmin, redmax)
            threshyellow = cv2.inRange(imcrop, yellowmin, yellowmax)
            #cv2.imshow("R1",threshyellow)
            threshblue = cv2.inRange(imcrop, bluemin, bluemax)
            _, contred, _ = cv2.findContours(threshred, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            _, contyellow, _ = cv2.findContours(threshyellow, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            _, contblue, _ = cv2.findContours(threshblue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if count == 0:
                for cnt in contred:
                    area = cv2.contourArea(cnt)
                    if area > 200:
                        approx = cv2.approxPolyDP(cnt, 0.04 * cv2.arcLength(cnt, True), True)
                        cen = cv2.moments(cnt)
                        cenx = int(cen["m10"] / cen["m00"])
                        ceny = int(cen["m01"] / cen["m00"])
                        centres.append((cenx + j * w // 5, ceny + i * l // 5))
                        if (len(approx) == 4):
                            shacol.append(1)
                            count = 1
                        else:
                            shacol.append(0)
                            count = 1
            if count == 0:
                for cnt in contyellow:
                    area = cv2.contourArea(cnt)
                    if area > 200:
                        cen = cv2.moments(cnt)
                        cenx = int(cen["m10"] / cen["m00"])
                        ceny = int(cen["m01"] / cen["m00"])
                        centres.append((cenx + j * w // 5, ceny + i * l // 5))
                        approx = cv2.approxPolyDP(cnt, 0.04 * cv2.arcLength(cnt, True), True)
                        if len(approx) == 4:
                            shacol.append(3)
                            count = 1
                        else:
                            shacol.append(2)
                            count = 1
            if count == 0:
                for cnt in contblue:
                    area = cv2.contourArea(cnt)
                    if area > 200:
                        cen = cv2.moments(cnt)
                        cenx = int(cen["m10"] / cen["m00"])
                        ceny = int(cen["m01"] / cen["m00"])
                        centres.append((cenx + j * w // 5, ceny + i * l // 5))
                        shacol.append(5)
                        count = 1
            if count == 0:
                for cnt in contours:
                    area = cv2.contourArea(cnt)
                    if area > 300:
                        cen = cv2.moments(cnt)
                        cenx = int(cen["m10"] / cen["m00"])
                        ceny = int(cen["m01"] / cen["m00"])
                        centres.append((cenx + j * w // 5, ceny + i * l // 5))
                    if (i == 0 and j == 0) or (i == 0 and j == 4) or (i == 4 and j == 0) or (i == 4 and j == 4):
                        shacol.append(6)
                    else:
                        shacol.append(4)
    return centres, shacol

def getPro(img):
    l, w = img.shape[:2]
    hsv = img
    # hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    brng = cv2.selectROI(img)
    yrng = cv2.selectROI(img)
    rrng = cv2.selectROI(img)
    wrng = cv2.selectROI(img)
    grng = cv2.selectROI(img)

    blue = hsv[int(brng[1]) : int(brng[1] + brng[3]) , int(brng[0]) : int(brng[0] + brng[2])]
    yellow = hsv[int(yrng[1]) : int(yrng[1] + yrng[3]) , int(yrng[0]) : int(yrng[0] + yrng[2])]
    red = hsv[int(rrng[1]) : int(rrng[1] + rrng[3]) , int(rrng[0]) : int(rrng[0] + rrng[2])]
    white = hsv[int(wrng[1]) : int(wrng[1] + wrng[3]) , int(wrng[0]) : int(wrng[0] + wrng[2])]
    green = hsv[int(grng[1]): int(grng[1] + grng[3]), int(grng[0]): int(grng[0] + grng[2])]

    thresh = 35

    redmin = np.array([red[:, :, 0].min() - thresh, red[:, :, 1].min() - thresh, red[:, :, 2].min() - thresh])
    redmax = np.array([red[:, :, 0].max() + thresh, red[:, :, 1].max() + thresh, red[:, :, 2].max() + thresh])
    yellowmin = np.array([yellow[:, :, 0].min() - thresh - 5, yellow[:, :, 1].min() - thresh-5, yellow[:, :, 2].min() - thresh-5])
    yellowmax = np.array([yellow[:, :, 0].max() + thresh+5, yellow[:, :, 1].max() + thresh+5, yellow[:, :, 2].max() + thresh+5])
    bluemin = np.array([blue[:, :, 0].min() - thresh, blue[:, :, 1].min() - thresh, blue[:, :, 2].min() - thresh])
    bluemax = np.array([blue[:, :, 0].max() + thresh, blue[:, :, 1].max() + thresh, blue[:, :, 2].max() + thresh])
    whimin = np.array([white[:, :, 0].min() - thresh, white[:, :, 1].min() - thresh, white[:, :, 2].min() - thresh])
    whimax = np.array([white[:, :, 0].max() + thresh, white[:, :, 1].max() + thresh, white[:, :, 2].max() + thresh])
    greenmin = np.array([green[:, :, 0].min() - thresh, green[:, :, 1].min() - thresh, green[:, :, 2].min() - thresh])
    greenmax = np.array([green[:, :, 0].max() + thresh, green[:, :, 1].max() + thresh, green[:, :, 2].max() + thresh])

    shacol = []
    centres = []
    greens = []
    for i in range(0, n):
        for j in range(0, n):
            count = 0
            imcrop = hsv[i * l // n:(i + 1) * l // n, j * w // n:(j + 1) * w // n]

            kernel = np.ones((3, 3), np.uint8)

            threshold = cv2.inRange(imcrop, whimin, whimax)
            result = cv2.erode(threshold, kernel, iterations=2)
            result = cv2.dilate(result, kernel, iterations=2)

            threshred = cv2.inRange(imcrop, redmin, redmax)
            threshred = cv2.erode(threshred, kernel, iterations=2)
            threshred = cv2.dilate(threshred, kernel, iterations=2)

            threshyellow = cv2.inRange(imcrop, yellowmin, yellowmax)
            threshyellow = cv2.erode(threshyellow, kernel, iterations=2)
            threshyellow = cv2.dilate(threshyellow, kernel, iterations=2)

            threshblue = cv2.inRange(imcrop, bluemin, bluemax)
            threshblue = cv2.erode(threshblue, kernel, iterations=2)
            threshblue = cv2.dilate(threshblue, kernel, iterations=2)

            threshgreen = cv2.inRange(imcrop, greenmin, greenmax)
            threshgreen = cv2.erode(threshgreen, kernel, iterations=2)
            threshgreen = cv2.dilate(threshgreen, kernel, iterations=2)

            _, contred, _ = cv2.findContours(threshred, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            _, contyellow, _ = cv2.findContours(threshyellow, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            _, contblue, _ = cv2.findContours(threshblue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            _, contwhi, _ = cv2.findContours(result, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            _, contgreen, _ = cv2.findContours(threshgreen, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if count == 0:
                for cnt in contwhi:
                    area = cv2.contourArea(cnt)
                    if area > 100:
                        cen = cv2.moments(cnt)
                        cenx = int(cen["m10"] / cen["m00"])
                        ceny = int(cen["m01"] / cen["m00"])
                        centres.append((cenx + j * w // n, ceny + i * l // n))
                        for cn in contgreen:
                            are = cv2.contourArea(cn)
                            if are > 250:
                                shacol.append(6)
                                count = 1
                                break
                        else:
                            for cn in contblue:
                                are = cv2.contourArea(cn)
                                if are > 250:
                                    shacol.append(7)
                                    count = 1
                                    break
                            else:
                                shacol.append(4)
                                count = 1
            if count == 0:
                for cnt in contyellow:
                    area = cv2.contourArea(cnt)
                    if area > 250:
                        cen = cv2.moments(cnt)
                        cenx = int(cen["m10"] / cen["m00"])
                        ceny = int(cen["m01"] / cen["m00"])
                        centres.append((cenx + j * w // n, ceny + i * l // n))
                        approx = cv2.approxPolyDP(cnt, 0.04 * cv2.arcLength(cnt, True), True)
                        if len(approx) == 4:
                            shacol.append(3)
                            count = 1
                        else:
                            shacol.append(2)
                            count = 1
            if count == 0:
                for cnt in contred:
                    area = cv2.contourArea(cnt)
                    if area > 250:
                        approx = cv2.approxPolyDP(cnt, 0.04 * cv2.arcLength(cnt, True), True)
                        cen = cv2.moments(cnt)
                        cenx = int(cen["m10"] / cen["m00"])
                        ceny = int(cen["m01"] / cen["m00"])
                        centres.append((cenx + j * w // n, ceny + i * l // n))
                        if (len(approx) == 4):
                            shacol.append(1)
                            count = 1
                        else:
                            shacol.append(0)
                            count = 1

            if count == 0:
                for cnt in contblue:
                    area = cv2.contourArea(cnt)
                    if area > 250:
                        cen = cv2.moments(cnt)
                        cenx = int(cen["m10"] / cen["m00"])
                        ceny = int(cen["m01"] / cen["m00"])
                        centres.append((cenx + j * w // n, ceny + i * l // n))
                        shacol.append(5)

    for i in centres:
        cv2.circle(img, i, 2, [255, 0, 0], 2)
        cv2.putText(img, str(shacol[centres.index(i)]), i, cv2.FONT_HERSHEY_SIMPLEX, 0.5, [255, 0, 0])
    img = cv2.resize(img, (500, 500))
    cv2.imshow("Shacol", img)
    cv2.waitKey(0)
    return centres, shacol


def dijsktra(graph, src, dest):
    maxint = 100000000

    class Graph:
        def __init__(self, vertices):
            self.V = vertices
            self.graph = [[-1 for column in range(vertices)]
                          for row in range(vertices)]

        def minDistance(self, dist, sptSet):

            min = maxint
            min_index = 0
            for v in range(self.V):
                if dist[v] < min and sptSet[v] == False:
                    min = dist[v]
                    min_index = v

            return min_index

        def dj(self, src):

            dist = [maxint] * self.V
            dist[src] = 0
            sptSet = [False] * self.V

            for cout in range(self.V):
                u = self.minDistance(dist, sptSet)
                sptSet[u] = True
                for v in range(self.V):
                    if self.graph[u][v] >= 0 and sptSet[v] == False and dist[v] > dist[u] + self.graph[u][v]:
                        dist[v] = dist[u] + self.graph[u][v]
                        parent[v] = u

    g = Graph(n ** 2)
    parent = [0] * (n ** 2)
    g.graph = graph
    g.dj(src)
    sol = [dest]
    v = dest
    while True:
        if v == src:
            break
        else:
            sol.append(parent[v])
            v = parent[v]
    sol.reverse()
    return sol


def getGraph1(wen):
    graph = [[-1 for column in range(n ** 2)]
             for row in range(n ** 2)]
    for i in range(0, n ** 2):
        if i + n < n ** 2:
            graph[i][i + n] = 1
        if i - n >= 0:
            graph[i][i - n] = 1
        if i % n != 0:
            graph[i][i - 1] = 1
        if (i + 1) % n != 0:
            graph[i][i + 1] = 1
    for j in wen:
        for i in range(0, n ** 2):
            graph[i][j] = -1
            graph[j][i] = -1
    return graph


def getGraph2(req, shacol, obst):
    graph = [[-1 for column in range(n ** 2)]
             for row in range(n ** 2)]
    for i in range(0, n ** 2):
        if shacol[i] == req:
            if i + n < n ** 2:
                if shacol[i + n] == req:
                    graph[i][i + n] = 0
                else:
                    graph[i][i + n] = 1
            if i - n >= 0:
                if shacol[i - n] == req:
                    graph[i][i - n] = 0
                else:
                    graph[i][i - n] = 1
            if i % n != 0:
                if shacol[i - 1] == req:
                    graph[i][i - 1] = 0
                else:
                    graph[i][i - 1] = 1
            if (i + 1) % n != 0:
                if shacol[i + 1] == req:
                    graph[i][i + 1] = 0
                else:
                    graph[i][i + 1] = 1
        else:
            if i + n < n ** 2:
                if shacol[i + n] == req:
                    graph[i][i + n] = 1
                else:
                    graph[i][i + n] = 2
            if i - n >= 0:
                if shacol[i - n] == req:
                    graph[i][i - n] = 1
                else:
                    graph[i][i - n] = 2
            if i % n != 0:
                if shacol[i - 1] == req:
                    graph[i][i - 1] = 1
                else:
                    graph[i][i - 1] = 2
            if (i + 1) % n != 0:
                if shacol[i + 1] == req:
                    graph[i][i + 1] = 1
                else:
                    graph[i][i + 1] = 2
    for i in obst:
            for j in range(0, n ** 2):
                graph[i][j] = -1
                graph[j][i] = -1
    return graph


def move(pos, vect, cnb, rea, ser):

    print("Sent")
    v0 = np.array(vect)
    v1 = np.array([cnb[0]-pos[0], cnb[1]-pos[1]])
    angle = np.math.atan2(np.linalg.det([v0, v1]), np.dot(v0, v1))
    angle = np.degrees(angle)
    if angle < 0:
        angle += 360
    print(angle)
    if 0 <= angle < 160 and rea == 0:
        ser.write(b'L')
        print("l")
        return 0
    elif 200 < angle <= 360 and rea == 0:
        ser.write(b'R')
        print("r")
        return 0
    elif 0 <= angle < 170 and rea == 1:
        ser.write(b'L')
        return 0
    elif 190 < angle <= 360 and rea == 1:
        ser.write(b'R')
        return 0
    elif (sqrt((cnb[0]-pos[0])**2 + (cnb[1]-pos[1])**2) > 30) and rea == 0:
        ser.write(b'F')
        print("f")
        return 0
    elif (sqrt((cnb[0]-pos[0])**2 + (cnb[1]-pos[1])**2) > 50) and rea == 1:
        ser.write(b'F')
        return 0
    else:
        ser.write(b's')
        return 1

def moveAc(pos, vect, cnb, rea, ser):
    v0 = np.array(vect)
    v1 = np.array([cnb[0] - pos[0], cnb[1] - pos[1]])
    angle = np.math.atan2(np.linalg.det([v0, v1]), np.dot(v0, v1))
    angle = np.degrees(angle)
    if angle < 0:
        angle += 360
    print(angle)
    if 0 <= angle < 160 and rea == 0:
        ser.write(b'L')
        print("l")
        return 0
    elif 200 < angle <= 360 and rea == 0:
        ser.write(b'R')
        print("r")
        return 0
    around = []
    if rea == 0:
        dis = 25
        for i in range(0, dis):
            for j in range(0, dis):
                around.append((cnb[0]+j, cnb[1]+i))
        if pos in around:
            ser.write(b's')
            return 1
        else:
            ser.write(b'F')
            return 0
    else:
        dis = 50
        for i in range(0, dis):
            for j in range(0, dis):
                around.append((cnb[0]+j, cnb[1]+i))
        if pos in around:
            ser.write(b's')
            return 1

def moveB(pos, vect, cna, cnb, rea, ser):
    turn = 70
    v0 = np.array(vect)
    v1 = np.array([cnb[0] - pos[0], cnb[1] - pos[1]])
    angle = np.math.atan2(np.linalg.det([v0, v1]), np.dot(v0, v1))
    angle = np.degrees(angle)
    if angle < 0:
        angle += 360
    if 0 <= angle <= 160 and rea == 0:
        a = turn * (180 - angle) // 90
        data = str(a) + '01'
        ser.write(str.encode(data))
        return 0
    elif 200 < angle <= 360 and rea == 0:
        a = turn * (angle - 180) // 90
        data = str(a) + '10'
        ser.write(str.encode(str(a)))
        return 0
    elif 0 <= angle <= 170 and rea == 1:
        a = turn * (180 - angle) // 90
        data = str(a) + '01'
        ser.write(str.encode(data))
        return 0
    elif 190 < angle <= 360 and rea == 1:
        a = turn * (angle - 180) // 90
        data = str(a) + '10'
        ser.write(str.encode(data))
        return 0
    elif ((cnb[0] - pos[0]) > 20 or cnb[1] - pos[1] > 20) and rea == 0:
        data = str(turn) + '11'
        ser.write(str.encode(data))
        return 0
    else:
        ser.write(str.encode('1'))
        return 1
def move_(pos, vect, cnb, rea, ser, tl, tr):
    v0 = np.array(vect)
    v1 = np.array([cnb[0] - pos[0], cnb[1] - pos[1]])
    angle = np.math.atan2(np.linalg.det([v0, v1]), np.dot(v0, v1))
    angle = np.degrees(angle)
    if angle < 0:
        angle += 360
    if 20 < angle <= 180:
        ser.write(b'L')
        sleep(tl * angle / 90)
        return 0
    elif 180 < angle < 340:
        ser.write(b'R')
        sleep(tr * angle / 90)
        return 0
    elif (sqrt((cnb[0] - pos[0]) ** 2 + (cnb[1] - pos[1]) ** 2) > 50) and rea == 0:
        ser.write(b'F')
        return 0
    else:
        return 1


def moveBack(pos, vect, cnb, ser):
    v0 = np.array([-vect[0], -vect[1]])
    v1 = np.array([cnb[0] - pos[0], cnb[1] - pos[1]])
    angle = np.math.atan2(np.linalg.det([v0, v1]), np.dot(v0, v1))
    angle = np.degrees(angle)
    if angle < 0:
        angle += 360
    if 0 <= angle <= 160:
        ser.write(b'L')
        return 0
    elif 200 < angle <= 360:
        ser.write(b'R')
        return 0
    elif (sqrt((cnb[0]-pos[0])**2 + (cnb[1]-pos[1])**2) > 20):
        ser.write(b'B')
        return 0
    else:
        ser.write(b's')
        return 1
