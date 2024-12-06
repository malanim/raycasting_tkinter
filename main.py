import tkinter as tk
import math

def read_obj(file_path):
    vertices = []
    faces = []

    with open(file_path, 'r') as file:
        for line in file:
            # Удаляем пробелы в начале и конце строки
            line = line.strip()
            # Пропускаем пустые строки
            if not line:
                continue
            
            # Разделяем строку на части
            parts = line.split()
            # Если строка начинается с 'v', это вершина
            if parts[0] == 'v':
                # Добавляем вершину в список
                vertex = tuple(map(float, parts[1:4]))  # x, y, z
                vertices.append(vertex)
            # Если строка начинается с 'f', это грань
            elif parts[0] == 'f':
                # Добавляем грань в список
                face = [int(p.split('/')[0]) - 1 for p in parts[1:]]  # индексы вершин
                faces.append(face)

    return vertices, faces

# # Пример использования read_obj
# vertices, faces = read_obj('model.obj')
# print("Вершины:", vertices)
# print("Грани:", faces)

# Определение 3D-объекта
class Object3D:
    def __init__(self, vertices, faces):
        self.vertices = vertices
        self.faces = faces
        self.angle_x = 0
        self.angle_y = 0

    def rotate(self, delta_time):
        rotation_speed = 1
        self.angle_y += rotation_speed * delta_time

        cos_y = math.cos(self.angle_y)
        sin_y = math.sin(self.angle_y)

        for i in range(len(self.vertices)):
            x, y, z = self.vertices[i]
            x, z = x * cos_y + z * sin_y, -x * sin_y + z * cos_y
            self.vertices[i] = [x, y, z]

    def project(self, width, height, fov, viewer_distance):
        projected = []
        for vertex in self.vertices:
            x, y, z = vertex
            factor = fov / (viewer_distance + z)
            x_proj = x * factor + width / 2
            y_proj = -y * factor + height / 2
            projected.append((x_proj, y_proj))
        return projected

# Рисование рёбер
def draw_edges(canvas, projected, faces):
    edges = []
    for face in faces:
        for i in range(len(face)):
            start = face[i]
            end = face[(i + 1) % len(face)]  # Соединяем последнюю грань с первой
            edges.append((start, end))
    canvas.delete("all")  # Очистка канваса перед перерисовкой
    for edge in edges:
        start, end = edge
        x1, y1 = projected[start]
        x2, y2 = projected[end]
        canvas.create_line(x1, y1, x2, y2)

# Основная функция
def main():
    width, height = 1600, 800
    fov = 512
    viewer_distance = 3

    vertices, faces = read_obj('monkey.obj')
    object3d = Object3D(vertices, faces)

    root = tk.Tk()
    canvas = tk.Canvas(root, width=width, height=height, bg='white')
    canvas.pack()

    import time
    last_time = time.time()  # Получаем текущее время

    def update():
        nonlocal last_time
        current_time = time.time()  # Получаем текущее время
        delta_time = (current_time - last_time) / 1000.0  # Время в секундах
        last_time = current_time
        object3d.rotate(delta_time)  # Вращаем объект с учетом времени
        projected = object3d.project(width, height, fov, viewer_distance)
        draw_edges(canvas, projected, object3d.faces)
        root.after(1, update)  # Обновление каждые 1 мс

    update()  # Запускаем обновление
    root.mainloop()

if __name__ == "__main__":
    main()