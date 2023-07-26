import cv2
import pandas as pd
import numpy as np
import time
from ultralytics import YOLO
from tracker import Tracker

# Ініціалізація моделі YOLO
model = YOLO('yolov8s.pt')

# Функція для обробки події миші
def RGB(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        colorsBGR = [x, y]
        print(colorsBGR)

# Створення вікна та встановлення обробника подій миші
cv2.namedWindow('RGB')
cv2.setMouseCallback('RGB', RGB)

# Відкриття відео для захоплення
cap = cv2.VideoCapture('Walk.mp4')

# Завантаження списку класів
my_file = open("coco.txt", "r")
data = my_file.read()
class_list = data.split("\n")

# Ініціалізація змінних
count = 0
tracker = Tracker()d
enclosed_persons = 0

while True:
    start_time = time.time()
    ret, frame = cap.read()
    if not ret:
        break
    count += 1
    if count % 3 != 0:
        continue

    # Зміна розміру кадру
    frame = cv2.resize(frame, (1020, 500))

    # Виклик методу predict моделі YOLO
    results = model.predict(frame)

    # Обробка результатів детекції
    a = results[0].boxes.boxes
    px = pd.DataFrame(a).astype("float")
    bbox_list = []
    class_labels = []

    for index, row in px.iterrows():
        x1 = int(row[0])
        y1 = int(row[1])
        x2 = int(row[2])d
        y2 = int(row[3])
        d = int(row[5])
        c = class_list[d]

        if c == 'person':
            bbox_list.append([x1, y1, x2, y2])
            class_labels.append(c)

    # Оновлення відстежуваних об'єктів
    bbox_idx = tracker.update(bbox_list, class_labels)
    enclosed_persons = 0

    # Відображення відстежених об'єктів
    for bbox in bbox_idx:
        x3, y3, x4, y4, id = bbox
        cx = int((x3 + x4) / 2)
        cy = int((y3 + y4) / 2)
        cv2.rectangle(frame, (x3, y3), (x4, y4), (0, 255, 0), 2)
    #    cv2.putText(frame, str(int(id)), (x3, y3), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 0), 1)
        enclosed_persons += 1

    # Відображення кількості виявлених людей
    cv2.putText(frame, f"People recognized: {enclosed_persons}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # Відображення кадру
    cv2.imshow("RGB", frame)

    # Вимірювання часу виконання
    end_time = time.time()
    print("Execution Time:", end_time - start_time, "seconds")

    # Перевірка натискання клавіші "q"
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Закриття вікна та звільнення ресурсів
cv2.destroyAllWindows()
cap.release()






