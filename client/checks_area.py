import pyautogui as pya
import time

# Здесь происходит показ областей, которые являются рабочими.
# Когда-нибудь запихаю параметры ввода обласей в графику

def cheking_area(points, text='Area', dur = 2, time_on_point = 0.5):

    #points = [x1, y1, x2, y2]
    x1, x2 = min(points[0], points[2]), max(points[0], points[2])
    y1, y2 = min(points[1], points[3]), max(points[1], points[3])

    print(f'\nПроверка {text}')
    pya.moveTo(x1, y1, duration = 1)
    print('Левый верхний угол области')
    time.sleep(3)
    pya.moveTo(x1, y2, duration = dur)
    time.sleep(time_on_point)
    pya.moveTo(x2, y2, duration = dur)
    time.sleep(time_on_point)
    pya.moveTo(x2, y1, duration = dur)
    time.sleep(time_on_point)
    pya.moveTo(x1, y1, duration = dur)
    time.sleep(time_on_point)


def take_screen():

    wei, hei = pya.size()

    interactive_areases = {
    'act' : [wei - 150, hei - 40, wei - 10, hei-10],
    'image' : [wei - 250, int(hei/4), wei-10, int(hei*3/4)],
    'text' : [150, 10, wei-300, int(hei/5)]}

    return interactive_areases

def tests(interactive_areases):

    cheking_area(interactive_areases['act'], 'Смена режимов')
    cheking_area(interactive_areases['image'], 'Изображение')
    cheking_area(interactive_areases['text'], 'Выделенный текст')


if __name__ == '__main__':
    tests(tests(take_screen()))
