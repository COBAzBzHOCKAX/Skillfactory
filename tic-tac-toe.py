# На текущий момент работает только режим в два игрока. К сожалению пока не реализована игра с ботом.
# Выбирайте при запуске игры 2 игрока, иначе получите бесконечный цикл


# инициализация карты с координатами
maps = [[' ', 1, 2, 3],
        [1, '-', '-', '-'],
        [2, '-', '-', '-'],
        [3, '-', '-', '-']]

# инициализация победных линий [<№ строки>, <№ столбца>]
victories = [[[1, 1], [1, 2], [1, 3]],
             [[2, 1], [2, 2], [2, 3]],
             [[3, 1], [3, 2], [3, 3]],
             [[1, 1], [2, 1], [3, 1]],
             [[1, 2], [2, 2], [3, 2]],
             [[1, 3], [2, 3], [3, 3]],
             [[1, 1], [2, 2], [3, 3]],
             [[1, 3], [2, 2], [3, 1]],
             ]  # желательно заменить на логику веса сложения


stp_row = 0 # объявляем переменную строки
stp_column = 0 # объявляем переменную столбца

end_win = ''


def print_maps(): # вывод карты на экран
    for i in maps:
        print(*i)

def check(func): # Декоратор счётчика ходов
    global count_step
    count_step = 0 # объявляем переменную счётчика ходов
    # проверка на правильность ввода в ячейку
    def chk_step_maps(*args, **kwargs): # проверка правильности введёных данных пользователем
        XO_player(count_step) # вызываем функцию для определения чей сейчас ход
        print_maps()
        print()
        if XO == 'X' or AI == 2:
            while True:
                    step_player() # эта функция для людей
                    if (1 <= stp_row <= 3) and (1 <= stp_column <= 3):
                        if maps[stp_row][stp_column] == '-':
                            func()
                            break
                        print_maps()
                        print()
                        print(f'Вы можете поставить {XO} только в свободное окошко, обозначенное "-"')
                    else:
                        print_maps()
                        print()
                        print('вводите номера строки и столбца в диапазоне от 1 до 3-х')
        else:
            AI  # Запускаем AI
    return chk_step_maps

def step_player(): # эта функция принимает координаты игрока
    global stp_column
    global stp_row
    while True:
        print(f'Ход №{count_step + 1}. Сейчас ходят {XO}')
        input_int = input(f'введите номер строки и столбца куда поставить {XO} через пробел ').split()
        print()
        if len(input_int) == 2:
            stp_row = int(input_int[0])
            stp_column = int(input_int[1])
            break
        else:
            print('Вам нужно указать два числа через пробел!')

def XO_player(count_step): # эта функция в зависсимости от чётности хода определяет кто сейчас должен ходить (X или O)
    global XO
    if count_step % 2 == 0:
        XO = 'X'
    else:
        XO = 'O'


@check
def mark_in_maps(): # функция отметки на игровом поле, а так же +1 в счётчик ходов
    global count_step
    global end_win
    maps[stp_row][stp_column] = XO
    end_win = get_result()
    count_step += 1 # Обновляем счётчик хода

def get_result():
    win = ''
    for i in victories:
        if maps[i[0][0]][i[0][1]] == "X" and maps[i[1][0]][i[1][1]] == "X" and maps[i[2][0]][i[2][1]] == "X":
            win = "X"
            return win
        if maps[i[0][0]][i[0][1]] == "O" and maps[i[1][0]][i[1][1]] == "O" and maps[i[2][0]][i[2][1]] == "O":
            win = "O"
            return win


def check_line(sum_O, sum_X): # Искусственный интеллект: поиск линии с нужным количеством X и O на победных линиях
    step = 0
    global maps
    for line in victories:
        O = 0
        X = 0
        for j in range(3):
            if maps[line[j][0]][line[j][1]] == "X":
                X =+ 1
            if maps[line[j][0]][line[j][1]] == "O":
                O =+ 1
        if O == sum_O and X == sum_X:
            for j in range(3):
                if maps[line[j][0]][line[j][1]] == '-':
                    maps[line[j][0]][line[j][1]] = XO
                    step += 1
    return step

# Искусственный интеллект: выбор хода
def AI():
    global count_step
    step = 0

    # 1) если на какой либо из победных линий 2 свои фигуры и 0 чужих - ставим
    step = check_line(2, 0)

    # 2) если на какой либо из победных линий 2 чужие фигуры и 0 своих - ставим
    if not step:
       step = check_line(0, 2)

    # 3) если 1 фигура своя и 0 чужих - ставим
    if not step:
        step = check_line(1, 0)

    # 4) центр пуст, то занимаем центр
    if not step:
        if maps[2][2] != "X" and maps[2][2] != "O":
            maps[2][2] == XO
            step = 1

    # 5) если центр занят, то занимаем первую ячейку
    if not step:
        if maps[1][1] != "X" and maps[1][1] != "O":
            maps[1][1] == XO
            step = 1

    count_step += 1
    return step


print('Добро пожаловать в крестики нолики!')
print('Укажите число игроков числом - 1 или 2') # если 1, то с нами будет играть AI
AI = int(input())



while (not end_win) and (count_step != 9):
    mark_in_maps()

print()
if end_win:
    print(f'ПОБЕДА {end_win}!!!')
else:
    print('НИЧЬЯ!')