# # import cellular_automaton as ca
# #
# # ca.run_game_of_life()
# #
# # mc = ca.MainCycle(
# #     (70, 70),
# #     borders=False,
# #     update_frequency=20,
# #     forced_render=False,
# #     render_frequency=20,
# #     layer_by_layer_update=True,
# # )
# #
# # mc.run()
# #
# # """
# # This simple animation example shows how to use classes to animate
# # multiple objects on the screen at the same time.
# #
# # Note: Sprites draw much faster than drawing primitives
# #
# # If Python and Arcade are installed, this example can be run from the command line with:
# # python -m arcade.examples.shapes
# # """
# #
# import arcade
# import random
#
# # Set up the constants
# SCREEN_WIDTH = int(2560 / 1.5)
# SCREEN_HEIGHT = int(1440 / 1.5)
# SCREEN_TITLE = "Shapes!"
#
# NUMBER_OF_SHAPES = 500
#
#
# class Shape:
#     """ Generic base shape class """
#     def __init__(self, x, y, width, height, angle, delta_x, delta_y,
#                  delta_angle, color):
#         self.x = x
#         self.y = y
#         self.width = width
#         self.height = height
#         self.angle = angle
#         self.delta_x = delta_x
#         self.delta_y = delta_y
#         self.delta_angle = delta_angle
#         self.color = color
#
#     def move(self):
#         self.x += self.delta_x
#         self.y += self.delta_y
#         self.angle += self.delta_angle + 1
#         if self.x < 0 and self.delta_x < 0:
#             self.delta_x *= -1
#         if self.y < 0 and self.delta_y < 0:
#             self.delta_y *= -1
#         if self.x > SCREEN_WIDTH and self.delta_x > 0:
#             self.delta_x *= -1
#         if self.y > SCREEN_HEIGHT and self.delta_y > 0:
#             self.delta_y *= -1
#
#
# class Ellipse(Shape):
#
#     def draw(self):
#         arcade.draw_ellipse_filled(self.x, self.y, self.width, self.height,
#                                    self.color, self.angle)
#
#
# class Rectangle(Shape):
#
#     def draw(self):
#         arcade.draw_rectangle_filled(self.x, self.y, self.width, self.height,
#                                      self.color, self.angle)
#
#
# class Line(Shape):
#
#     def draw(self):
#         arcade.draw_line(self.x, self.y,
#                          self.x + self.width, self.y + self.height,
#                          self.color, 2)
#
#
# class Window(arcade.Window):
#     """ Main application class. """
#
#     def __init__(self):
#         # Call the parent __init__
#         super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
#
#         self.set_update_rate(1/60)
#         # Create a shape list
#         self.shape_list = []
#
#         for i in range(NUMBER_OF_SHAPES):
#
#             # Random spot
#             x = random.randrange(0, SCREEN_WIDTH)
#             y = random.randrange(0, SCREEN_HEIGHT)
#
#             # Random size
#             width = random.randrange(15, 40)
#             height = random.randrange(15, 40)
#
#             # Random angle
#             angle = random.randrange(0, 360)
#
#             # Random movement
#             d_x = random.randrange(-3, 4)
#             d_y = random.randrange(-3, 4)
#             d_angle = random.randrange(-3, 4)
#
#             # Random color
#             red = random.randrange(256)
#             green = random.randrange(256)
#             blue = random.randrange(256)
#             alpha = random.randrange(256)
#
#             # Random line, ellipse, or rect
#             shape_type = random.randrange(3)
#
#             if shape_type == 0:
#                 shape = Rectangle(x, y, width, height, angle, d_x, d_y,
#                                   d_angle, (red, green, blue, alpha))
#             elif shape_type == 1:
#                 shape = Ellipse(x, y, width, height, angle, d_x, d_y,
#                                 d_angle, (red, green, blue, alpha))
#             else:
#                 shape = Line(x, y, width, height, angle, d_x, d_y,
#                              d_angle, (red, green, blue, alpha))
#
#             # Add this new shape to the list
#             self.shape_list.append(shape)
#
#     def on_update(self, dt):
#         """ Move everything """
#         for shape in self.shape_list:
#             shape.move()
#
#     def on_draw(self):
#         """ Render the screen. """
#
#         # Clear teh screen
#         self.clear()
#
#         # Draw the shapes
#         for shape in self.shape_list:
#             shape.draw()
#
#
# def main():
#     Window()
#     arcade.run()
#
#
# if __name__ == "__main__":
#     main()
#!/usr/bin/env python

__author__ = "Dmitriy Krasota aka g0t0wasd"

# Minesweeper in Python using Tkinter.
# More at http://pythonicway.com/python-games/python-arcade/31-python-minesweep


from tkinter import *
import random

GRID_SIZE = 20 #  Размер поля
SQUARE_SIZE = 20 # Размер клетки
MINES_NUM = 40 # Количество мин на поле
mines = set(random.sample(range(1, GRID_SIZE**2+1), MINES_NUM)) # Устанавливаем случайным образом мины на поле
clicked = set() # Сет, хранящий все клетки, по которым мы кликнули


def check_mines(neighbors):
    """ Функция, возвращающая количество мин вокруг neighbors """
    return len(mines.intersection(neighbors))


def generate_neighbors(square):
    """ Возвращает клетки соседствующие с square """
    # Левая верхняя клетка
    if square == 1:
        data = {GRID_SIZE + 1, 2, GRID_SIZE + 2}
    # Правая нижняя
    elif square == GRID_SIZE ** 2:
        data = {square - GRID_SIZE, square - 1, square - GRID_SIZE - 1}
    # Левая нижняя
    elif square == GRID_SIZE:
        data = {GRID_SIZE - 1, GRID_SIZE * 2, GRID_SIZE * 2 - 1}
    # Верхняя правая
    elif square == GRID_SIZE ** 2 - GRID_SIZE + 1:
        data = {square + 1, square - GRID_SIZE, square - GRID_SIZE + 1}
    # Клетка в левом ряду
    elif square < GRID_SIZE:
        data = {square + 1, square - 1, square + GRID_SIZE,
                square + GRID_SIZE - 1, square + GRID_SIZE + 1}
    # Клетка в правом ряду
    elif square > GRID_SIZE ** 2 - GRID_SIZE:
        data = {square + 1, square - 1, square - GRID_SIZE,
                square - GRID_SIZE - 1, square - GRID_SIZE + 1}
    # Клетка в нижнем ряду
    elif square % GRID_SIZE == 0:
        data = {square + GRID_SIZE, square - GRID_SIZE, square - 1,
                square + GRID_SIZE - 1, square - GRID_SIZE - 1}
    # Клетка в верхнем ряду
    elif square % GRID_SIZE == 1:
        data = {square + GRID_SIZE, square - GRID_SIZE, square + 1,
                square + GRID_SIZE + 1, square - GRID_SIZE + 1}
    # Любая другая клетка
    else:
        data = {square - 1, square + 1, square - GRID_SIZE, square + GRID_SIZE,
                square - GRID_SIZE - 1, square - GRID_SIZE + 1,
                square + GRID_SIZE + 1, square + GRID_SIZE - 1}
    return data


def clearance(ids):
    """ Итеративная (эффективная) функция очистки поля """
    clicked.add(ids) # добавляем нажатую клетку в сет нажатых
    ids_neigh = generate_neighbors(ids) # Получаем все соседние клетки
    around = check_mines(ids_neigh) # высчитываем количество мин вокруг нажатой клетки
    c.itemconfig(ids, fill="green") # окрашиваем клетку в зеленый

    # Если вокруг мин нету
    if around == 0:
        # Создаем список соседних клеток
        neigh_list = list(ids_neigh)
        # Пока в списке соседей есть клетки
        while len(neigh_list) > 0:
            # Получаем клетку
            item = neigh_list.pop()
            # Окрашиваем ее в зеленый цвет
            c.itemconfig(item, fill="green")
            # Получаем соседение клетки данной клетки
            item_neigh = generate_neighbors(item)
            # Получаем количество мин в соседних клетках
            item_around = check_mines(item_neigh)
            # Если в соседних клетках есть мины
            if item_around > 0:
                # Делаем эту проверку, чтобы писать по нескольку раз на той же клетке
                if item not in clicked:
                    # Получаем координаты этой клетки
                    x1, y1, x2, y2 = c.coords(item)
                    # Пишем на клетке количество мин вокруг
                    c.create_text(x1 + SQUARE_SIZE / 2,
                                  y1 + SQUARE_SIZE / 2,
                                  text=str(item_around),
                                  font="Arial {}".format(int(SQUARE_SIZE / 2)),
                                  fill='yellow')
            # Если в соседних клетках мин нету
            else:
                # Добавляем соседние клетки данной клетки в общий список
                neigh_list.extend(set(item_neigh).difference(clicked))
                # Убираем повторяющиеся элементы из общего списка
                neigh_list = list(set(neigh_list))
            # Добавляем клетку в нажатые
            clicked.add(item)
    # Если мины вокруг есть
    else:
        # Высчитываем координаты клетки
        x1, y1, x2, y2 = c.coords(ids)
        # Пишем количество мин вокруг
        c.create_text(x1 + SQUARE_SIZE / 2,
                      y1 + SQUARE_SIZE / 2,
                      text=str(around),
                      font="Arial {}".format(int(SQUARE_SIZE / 2)),
                      fill='yellow')


def rec_clearance(ids):
    """ Рекурсивная (неэффективная) функция очистки поля """
    clicked.add(ids)
    neighbors = generate_neighbors(ids)
    around = check_mines(neighbors)
    if around:
        x1, y1, x2, y2 = c.coords(ids)
        c.itemconfig(ids, fill="green")
        c.create_text(x1 + SQUARE_SIZE / 2,
                      y1 + SQUARE_SIZE / 2,
                      text=str(around),
                      font="Arial {}".format(int(SQUARE_SIZE / 2)),
                      fill='yellow')
    else:
        for item in set(neighbors).difference(clicked):
            c.itemconfig(item, fill="green")
            rec_clearance(item)


def click(event):
    ids = c.find_withtag(CURRENT)[0]
    if ids in mines:
        c.itemconfig(CURRENT, fill="red")
    elif ids not in clicked:
        clearance(ids)
        c.itemconfig(CURRENT, fill="green")
    c.update()


def mark_mine(event):
    ids = c.find_withtag(CURRENT)[0]
    if ids not in clicked:
        clicked.add(ids)
        x1, y1, x2, y2 = c.coords(ids)
        c.itemconfig(CURRENT, fill="yellow")
    else:
        clicked.remove(ids)
        c.itemconfig(CURRENT, fill="gray")


root = Tk()
root.title("Pythonicway Minesweep")
c = Canvas(root, width=GRID_SIZE * SQUARE_SIZE, height=GRID_SIZE * SQUARE_SIZE)
c.bind("<Button-1>", click)
c.bind("<Button-3>", mark_mine)
c.pack()
for i in range(GRID_SIZE):
    for j in range(GRID_SIZE):
      c.create_rectangle(i * SQUARE_SIZE, j * SQUARE_SIZE,
                         i * SQUARE_SIZE + SQUARE_SIZE,
                         j * SQUARE_SIZE + SQUARE_SIZE, fill='gray')
root.mainloop()