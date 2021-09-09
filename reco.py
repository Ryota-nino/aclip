import cv2

XML_PATH = "./data/cascade/cascade.xml"
INPUT_IMG_PATH = "./IMG_4960.jpg"
OUTPUT_IMG_PATH = "output.png"

classifier = cv2.CascadeClassifier(XML_PATH)
img = cv2.imread(INPUT_IMG_PATH)
color = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
targets = classifier.detectMultiScale(color)
for x, y, w, h in targets:
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
cv2.imwrite(OUTPUT_IMG_PATH, img)
