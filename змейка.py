import tkinter as tk
import random
import sys
import os


def resource_path(relative_path): # функция для конвертирования .py файла в .exe
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


#Настройка поля и все константы
WIDTH=400
HEIGHT=400
DIRECTIONS=["Up","Down","Left","Right"] #список всех значений движения змейки
CELL_SIZE=10 #размер одной клетки змейки и еды
DELAY=100 #скорость игры (задержка между движениями змейки в мс)


#Начальное состояние игры
snake=[(100,100),(90,100),(80,100)] #начальное положение змейки в виде списка, хранящего 3 координаты: snake[0] - голова, snake[1] - второй сегмент и т.д.
direction="Right" #направление движения змейки; возможные значения: Up, Down, Left, Right
food=None #переменная для еды
score=0 #переменная для счёта
game_over=False #флаг, который показывает состояние игры. False - игра идёт, True - игра окончена


#Создание главного окна
root=tk.Tk()
root.title(f"Змейка | Счёт: {score}") #название и начальное значение счётчика очков
root.resizable(False,False) #запрещает изменение ширины и высоты окна
root.iconbitmap("змея.ico") #аватарка игры


#Добавление Canvas(область, где будет рисоваться змейка и еда)
canvas=tk.Canvas(
    root, #окно
    width=WIDTH, #ширина поля
    height=HEIGHT, #высота поля
    bg="white", #задаю цвет фона
    highlightthickness=0 #убираю границу
)
canvas.pack() #размещение canvas в окне


#Функция для рандомного появления змейки
def create_snake():
    # Вычисляем максимальное значение по X и Y,
    # чтобы вся змейка (3 клетки) уместилась в пределах поля
    max_x = (WIDTH // CELL_SIZE) - 3
    max_y = (HEIGHT // CELL_SIZE) - 1

    # Случайная позиция головы змейки
    x = random.randint(0, max_x) * CELL_SIZE
    y = random.randint(0, max_y) * CELL_SIZE

    # Возвращаем список из 3 сегментов змейки, направленных вправо
    return [(x, y), (x - CELL_SIZE, y), (x - 2 * CELL_SIZE, y)]


#Функция для генерации еды
def create_food():
    while True:
        x=random.randint(0,(WIDTH-CELL_SIZE)//CELL_SIZE)*CELL_SIZE
        y=random.randint(0,(HEIGHT-CELL_SIZE)//CELL_SIZE)*CELL_SIZE
        if (x,y) not in snake:
            return (x,y)
food=create_food()


#Функция для отрисовки еды
def draw_food():
    canvas.create_rectangle(
        food[0],food[1], #верхний угол (x1,y1)
        food[0]+CELL_SIZE, #x-координата правого края
        food[1]+CELL_SIZE, #y-координата левого края
        fill="red", #цвет заливки
    )


#Функция для отрисовки змейки на экране
def draw_snake():
    for segment in snake:
        canvas.create_rectangle(
            segment[0],segment[1], #левый верхний угол
            segment[0]+CELL_SIZE, #правый нижний угол(x)
            segment[1]+CELL_SIZE, #правый нижний угол(y)
            fill="green", #цвет заливки
            outline="darkgreen" #цвет обводки
        )


#Функция перезапуска игры
def restart_game():
    global snake, direction, food, score, game_over

    # Начальное положение змейки
    snake = create_snake()
    direction = "Right"
    # Новая еда
    food = create_food()
    # Сброс счёта и статуса
    score = 0
    game_over = False
    # Очистим холст и обновим
    canvas.delete("all")
    draw_food()
    draw_snake()
    update_title()
    # Перезапускаем игровой цикл
    root.after(DELAY, game_loop)


#Функция для обработки нажатия клавиш
def on_key_press(event):
    global direction
    key=event.keysym #сохранение в переменную key название клавиши, которую нажал пользователь, в виде строки
    if key in DIRECTIONS and not game_over: #запрет на поворот в противоположную сторону
        if (key == "Up" and direction != "Down" or
            key == "Down" and direction != "Up" or
            key == "Left" and direction != "Right" or
            key == "Right" and direction != "Left"):
            direction = key
    elif key=="space" and game_over:
        restart_game()
root.bind("<KeyPress>",on_key_press) #привязывание обработчика к окну


#Функция для проверки, съедена ли еда
def check_food_collision():
    global food,score
    if snake[0]==food:
        score+=1 #увеличиваюсчёт на 1
        food=create_food() #генерирую новую еду
        return True #сообщаю, что еда съедена
    return False #еда не съедена


#Функция для обновления счёта
def update_title():
    root.title(f"Змейка | Счёт: {score}")


#Функция для движения змейки
def move_snake():
    head_x,head_y=snake[0]
    if direction == "Up":
        new_head = (head_x, head_y - CELL_SIZE)
    elif direction == "Down":
        new_head = (head_x, head_y + CELL_SIZE)
    elif direction == "Left":
        new_head = (head_x - CELL_SIZE, head_y)
    elif direction == "Right":
        new_head = (head_x + CELL_SIZE, head_y)

    snake.insert(0,new_head) #добавление новой головы
    if not check_food_collision(): #если еда не съедена
        snake.pop() #если еда не съедена, то удаляем хвост


#Функция, которая проверяет, вышла ли голова змейки за пределы поля
def check_wall_collision():
    head_x,head_y=snake[0]
    return (
        head_x<0 or head_x>=WIDTH or head_y<0 or head_y>=HEIGHT
    )


#Функция для завершения игры
def end_game():
    global game_over
    game_over=True #перестаю обновлять игру
    canvas.create_text(
        WIDTH//2,HEIGHT//2, #Координаты центра экрана
        text=f"  Игра окончена! Счет: {score}. \n   Нажмите пробел для\n      перезапуска",
        fill="black",
        font=("italic",20)
    )


#Функция, проверяющая, не столкнулась ли змейка сама с собой
def check_self_collision():
    return snake[0] in snake[1:]


#Функция для создания игрового цикла
def game_loop():
    global snake,food,score

    move_snake() #движение змейки
    if check_wall_collision() or check_self_collision():
        end_game()
        return
    canvas.delete("all") #очистка холста
    draw_food() #рисую еду
    draw_snake() #рисую змейку 
    update_title()
    root.after(DELAY,game_loop) #повтор через DELAY мс


#первоначальная отрисовка
draw_food()
draw_snake()
root.after(DELAY,game_loop)


#Запуск главного цикла программы
root.mainloop()