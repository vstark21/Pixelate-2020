import cv2
import numpy as np
import Library
cap = cv2.VideoCapture(1)
_, frame = cap.read()
# frame = cv2.imread("mainArena.jpg")
img = cv2.resize(frame, (500, 500))
rng = cv2.selectROI(img)
img = img[int(rng[1]) : int(rng[1] + rng[3]) , int(rng[0]) : int(rng[0] + rng[2])]
img = cv2.resize(img, (900, 900))
centres, shacol = Library.getPro(img)
print(len(centres))
for i in centres:
    cv2.circle(img, i, 2, [255, 0, 0], 2)
    cv2.putText(img, str(i), i, cv2.FONT_HERSHEY_SIMPLEX, 0.5, [255, 0, 0])
# print(greens)
img = cv2.resize(img, (600, 600))
cv2.imshow("re", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
