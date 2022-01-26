#coding:utf-8
# Клиенская часть настроек

class for_while:
    server_ip = '127.0.0.1'      # Допускается запуск и клиента, и сервера на одной машине
    server_port = 65432
    notification_time = 39       # Период проверки соединения, рекомендуется 39 с
    wacth_time = 0.2             # Для цикла, можно занулить
    status_change = 1.5          # После смены режима будет неактивно (в сек)
    get_image = True             # Допуск использования захвата изображения
    start_status_active = False   # Начальный статус

class PyScreen:
    name = 'tes.png'
    time_before_first = 3    # Время перед взятием 1 точки
    time_before_second = 3   # Время перед взятием 2 точки

if __name__ == "__main__":
    import get_and_start
