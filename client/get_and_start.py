import pyautogui as pya
import time
import socket_client as socc
from subprocess import Popen, PIPE
import os
import pyscreenshot as pysh
import pytesseract
from PIL import Image
import checks_area as car
import conf_client


# Распознавание текста на изображении
def txt_from_image():
    st1 = pytesseract.image_to_string(Image.open(conf_client.PyScreen.name), lang='rus')
    print(st1)
    return st1


# ПОлучение перевичного буфера обмена (выделенный текст)
def out_prim():
    p = Popen(['xsel', '-o'], stdout=PIPE)
    return p.communicate()[0].decode()


def take_screenshot():
    # Любой угол прямоугольника текста
    print('Prepare')
    time.sleep(conf_client.PyScreen.time_before_first)
    x1, y1 = pya.position()

    # Противоположный угол
    print('Prepare 2')
    time.sleep(conf_client.PyScreen.time_before_second)
    x2, y2 = pya.position()

    # Углы могут быть любой парой
    x1, x2 = min(x1, x2), max(x1, x2)
    y1, y2 = min(y1, y2), max(y1, y2)

    # Стоять на месте мышке теперь можно
    if x1 == x2 or y1 == y2 or x1 == y1 or x2 == y2:
        return None

    im = pysh.grab(bbox=(x1, y1, x2, y2))
    name = conf_client.PyScreen.name
    im.save(name)
    print('Complite')
    return name


def catch_and_send():
    interactive_areases = car.take_screen()

    another_comp = conf_client.for_while.server_ip
    screen_image = conf_client.for_while.get_image
    is_active = conf_client.for_while.start_status_active

    prev_val = ''
    os.system('cvlc ./sounds/client_is_active.wav --play-and-exit')

    points_of_act = interactive_areases['act']
    points_of_image = interactive_areases['image']
    points_of_text = interactive_areases['text']

    last_time = time.time() - 10
    not_time = conf_client.for_while.notification_time  # not_time = 39

    while 1:
        if abs(time.time() - last_time) > not_time:
            # time.sleep(0.2)
            socc.send_qw('watch', 'inf', another_comp)
            last_time = time.time()
            time.sleep(conf_client.for_while.wacth_time)

        x, y = pya.position()

        # Смена режимов
        # [x1, y1, x2, y2]
        if points_of_act[0] < x < points_of_act[2] and points_of_act[1] < y < points_of_act[3]:
            if not is_active:
                is_active = True
                # os.system('cvlc ./sounds/act.wav --play-and-exit')
                socc.send_qw('status:active', 'inf', another_comp)
                time.sleep(conf_client.for_while.status_change)

            else:
                is_active = False
                # os.system('cvlc ./sounds/deac.wav --play-and-exit')
                socc.send_qw('status:deactive', 'inf', another_comp)
                time.sleep(conf_client.for_while.status_change)
                continue

        if not is_active:
            time.sleep(0.2)
            continue

        # Отправление выделенного тектса
        if is_active and points_of_text[0] < x < points_of_text[2] and points_of_text[1] < y < points_of_text[3]:
            req = out_prim()
            if len(req) == 0 or prev_val == req:
                continue
            prev_val = req
            print('Запрос', req)
            socc.send_qw(req, 'req', another_comp)
            last_time = time.time()
            time.sleep(conf_client.for_while.wacth_time)

        # Взятие и отправка скриншота
        elif screen_image and points_of_image[0] < x < points_of_image[2] and points_of_image[1] < y < points_of_image[
            3] and is_active:
            name_sh = take_screenshot()
            if name_sh == None:
                continue
            req = txt_from_image()

            # Чтобы не отправлять случайное движение мышки через экран - такая простая проверка на кол-во обзацев
            cnt_n = req.count('\n')
            if cnt_n > 6 or len(req) < 5:
                print(cnt_n)
                continue

            print('Запрос', req)
            socc.send_qw(req, 'req', another_comp)
            last_time = time.time()
            time.sleep(conf_client.for_while.wacth_time)

        time.sleep(conf_client.for_while.wacth_time)


try:
    catch_and_send()
except:
    os.system('cvlc ./sounds/error.wav --play-and-exit')
