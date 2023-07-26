import math


class Tracker:
    def __init__(self):
        # Зберігати центральні позиції об'єктів
        self.center_points = {}
        # Лічильник для ідентифікаторів
        # при кожному виявленні нового об'єкту лічильник збільшується на одиницю
        self.id_count = 0

    def update(self, objects_rect, class_labels):
        # Координати та ідентифікатори об'єктів
        objects_bbs_ids = []

        # Отримати центральну точку нового об'єкту
        for rect, class_label in zip(objects_rect, class_labels):
            x, y, w, h = rect
            cx = (x + x + w) // 2
            cy = (y + y + h) // 2

            # Перевірити, чи об'єкт є людиною (мітка класу 'person')
            if class_label == 'person':
                # Перевірити, чи ця людина вже була виявлена раніше
                same_person_detected = False
                for id, pt in self.center_points.items():
                    dist = math.hypot(cx - pt[0], cy - pt[1])

                    if dist < 50:
                        self.center_points[id] = (cx, cy)
                        objects_bbs_ids.append([x, y, w, h, id])
                        same_person_detected = True
                        break

                # Нова людина виявлена, призначити їй ідентифікатор
                if not same_person_detected:
                    self.center_points[self.id_count] = (cx, cy)
                    objects_bbs_ids.append([x, y, w, h, self.id_count])
                    self.id_count += 1

        # Очистити словник центральних точок від не використовуваних ідентифікаторів
        new_center_points = {}
        for obj_bb_id in objects_bbs_ids:
            if len(obj_bb_id) >= 5:  # Перевірити, чи містить bbox принаймні 5 значень
                _, _, _, _, object_id = obj_bb_id
                center = self.center_points[object_id]
                new_center_points[object_id] = center

        # Оновити словник, видаливши не використовувані ідентифікатори
        self.center_points = new_center_points.copy()
        return objects_bbs_ids




