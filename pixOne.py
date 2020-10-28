from Library import *
import serial

nodes = []
n = 9
shacol = []
deathNode = []
weaponNode = []
centres = []
prisonNode = []
obstacle = []
for i in range(0, n ** 2):
    nodes.append(i)
cap = cv2.VideoCapture(1)
print("Cam Connected")
ser = serial.Serial("COM6", baudrate = 9600, timeout = 0)
print("Serial Connected")
_, frame = cap.read()
_, frame = cap.read()
_, frame = cap.read()
_, frame = cap.read()
_, frame = cap.read()
rng = cv2.selectROI(frame)
frame = frame[int(rng[1]) : int(rng[1] + rng[3]) , int(rng[0]) : int(rng[0] + rng[2])]
frame = cv2.resize(frame, (n * 100, n * 100))
centres, shacol = getPro(frame)
print(len(shacol), len(centres))
_, frame = cap.read()
_, frame = cap.read()
_, frame = cap.read()
_, frame = cap.read()
_, frame = cap.read()
pos, vect, presNode = getPos(cap, rng, ser)
print("Aruco Detected")
for i in range (0,len(shacol)):
    if shacol[i] == 6:
        deathNode.append(i)
        obstacle.append(i)
    elif shacol[i] == 4:
        weaponNode.append(i)
        obstacle.append(i)
    elif shacol[i] == 5:
        prisonNode.append(i)
    elif shacol[i] == 7:
        obstacle.append(i)
print("Prisons in ")
print(prisonNode)
print("Death Eaters in ")

print(deathNode)
sleep(3)
befend = presNode
for i in range(0, len(deathNode)):
    obstacle.remove(deathNode[i])
    graph1 = getGraph1(obstacle)
    Solution = dijsktra(graph1, befend, deathNode[i])
    print(Solution)
    Solution.remove(Solution[0])
    befend = Solution[len(Solution) - 2]
    while True:
        _, frame = cap.read()
        frame = frame[int(rng[1]): int(rng[1] + rng[3]), int(rng[0]): int(rng[0] + rng[2])]
        frame = cv2.resize(frame, (n * 100 // 2, n * 100 // 2))
        pos, vect, presNode = getPos(cap, rng, ser)
        print(Solution)
        nex = Solution[0]
        if len(Solution) == 1:
            ret = move(pos, vect, centres[nex], 1, ser)
        else:
            ret = move(pos, vect, centres[nex], 0, ser)
        if ret == 1:
            Solution.remove(nex)
            if len(Solution) == 0:
                break
        cv2.imshow("Image", frame)
        cv2.waitKey(1)
    sleep(1)
    ser.write(b'D')
    sleep(1)
    Solution = dijsktra(graph1, befend, prisonNode[i])
    print(Solution)
    Solution.remove(Solution[0])
    befend = Solution[len(Solution) - 2]
    while True:
        _, frame = cap.read()
        frame = frame[int(rng[1]): int(rng[1] + rng[3]), int(rng[0]): int(rng[0] + rng[2])]
        frame = cv2.resize(frame, (n * 100 // 2, n * 100 // 2))
        pos, vect, presNode = getPos(cap, rng, ser)
        print(Solution)
        nex = Solution[0]
        if len(Solution) == 1:
            ret = move(pos, vect, centres[nex], 1, ser)
        else:
            ret = move(pos, vect, centres[nex], 0, ser)
        if ret == 1:
            Solution.remove(nex)
            if len(Solution) == 0:
                break
        cv2.imshow("Image", frame)
        cv2.waitKey(1)
    sleep(1)
    ser.write(b'b')
    sleep(3)
    ser.write(b'U')
    ser.write(b's')
    sleep(1)
    obstacle.append(prisonNode[i])

for i in range(0, len(weaponNode)):
    obstacle.remove(weaponNode[i])
    graph1 = getGraph1(obstacle)
    Solution = dijsktra(graph1, befend, weaponNode[i])
    print(Solution)
    Solution.remove(Solution[0])
    befend = Solution[len(Solution) - 2]
    while True:
        _, frame = cap.read()
        frame = frame[int(rng[1]): int(rng[1] + rng[3]), int(rng[0]): int(rng[0] + rng[2])]
        frame = cv2.resize(frame, (n * 100 // 2, n * 100 // 2))
        pos, vect, presNode = getPos(cap, rng, ser)
        print(Solution)
        nex = Solution[0]
        if len(Solution) == 1:
            ret = move(pos, vect, centres[nex], 1, ser)
        else:
            ret = move(pos, vect, centres[nex], 0, ser)
        if ret == 1:
            Solution.remove(nex)
            if len(Solution) == 0:
                break
        cv2.imshow("Image", frame)
        cv2.waitKey(1)
    sleep(1)
    ser.write(b'D')
    sleep(1)
    ser.write(b'L')
    sleep(1.5)
    _, frame = cap.read()
    _, frame = cap.read()
    _, frame = cap.read()
    _, frame = cap.read()
    _, sha = getPro(frame)
    shacol[weaponNode[i]] = sha[weaponNode[i]]
    end = shacol[weaponNode[i]]
    for e in deathNode:
        if sha[e] == end:
            graph2 = getGraph1(obstacle)
            Solution = dijsktra(graph2, befend, e)
            print(Solution)
            Solution.remove(Solution[0])
            befend = Solution[len(Solution) - 2]
            while True:
                _, frame = cap.read()
                frame = frame[int(rng[1]): int(rng[1] + rng[3]), int(rng[0]): int(rng[0] + rng[2])]
                frame = cv2.resize(frame, (n * 100 // 2, n * 100 // 2))
                pos, vect, presNode = getPos(cap, rng, ser)
                print(Solution)
                nex = Solution[0]
                if len(Solution) == 1:
                    ret = move(pos, vect, centres[nex], 1, ser)
                else:
                    ret = move(pos, vect, centres[nex], 0, ser)
                if ret == 1:
                    Solution.remove(nex)
                    if len(Solution) == 0:
                        break
                cv2.imshow("Image", frame)
                cv2.waitKey(1)
                sleep(1)
                ser.write(b'U')
                sleep(1)



