import math
import threading
import time

import PySimpleGUI as sg
import numpy as np
import pandas

kill_thread = False


def params(minE, maxE, step):
    res = []
    c = 0
    for i in range(minE, maxE, step):
        res.append(minE + c)
        c += step
    return res


def popup_select(the_list):
    """
    Интерфейс изменения значения функции.
    :param the_list:
    """
    layout = [[sg.Text("Выберите состояние", font=elements_font),
               sg.Combo(the_list, key='_LIST_',
                        background_color="#F0E68C",
                        font=elements_font,
                        button_background_color="#F0E68C",
                        size=(45, 55), auto_size_text=True),
               sg.OK()]]
    window = sg.Window('Изменить состояние', layout=layout)
    event, values = window.read()
    window.close()
    del window
    return int(values['_LIST_'])


def read_data(name_file):
    """
    Извлечение данных из файла
    :param name_file: имя файла для извлечения
    """
    data = pandas.read_csv(name_file, encoding='utf-8', delimiter=",")
    return data


def create_device_elements(device):
    """
    Формирует массив из девайсов.
    :param sensor:
    :return:
    """
    devices = []
    for i in range(len(device)):
        on = "Off"
        colorB = '#CD5C5C'
        vis = False
        if device["status"][i]:
            on = "On"
            colorB = '#6B8E23'
            vis = True
        devices.append([sg.Text(device["device"][i],
                                background_color="#F0E68C",
                                font=elements_font),
                        sg.Text(device['param_name'][i] + ":",
                                background_color="#F0E68C",
                                font=elements_font),
                        sg.Text(device['param_value'][i],
                                background_color="#F0E68C",
                                font=elements_font,
                                key="P" + device['ID'][i]),
                        sg.Button(button_text=on,
                                  font=slider_font, key=device["device"][i],
                                  button_color=colorB),
                        sg.Button(button_text="Изменить",
                                  font=slider_font,
                                  tooltip='Изменить состояние устройства', key=device['ID'][i], visible=vis)
                        ])
    return devices


def create_sensor_elements(sensor):
    """
    Формирует массив из сенсоров.
    :param sensor:
    :return:
    """
    sensors = []
    for i in range(len(sensor)):
        colorB = '#F0E68C'
        colorD = '#CD5C5C'
        if (sensor["param_value"][i] <= sensor["max_value"][i]) and (
                sensor["param_value"][i] >= sensor["min_value"][i]):
            colorD = '#F0E68C'
        sensors.append(
            [sg.Text(sensor["sensor"][i],
                     background_color=colorB,
                     font=elements_font,
                     key=sensor["sensor"][i]),
             sg.Text(sensor['param_name'][i] + ":",
                     background_color=colorB,
                     font=elements_font,
                     key=sensor["param_name"][i]),
             sg.Text(sensor['param_value'][i],
                     background_color=colorD,
                     font=elements_font,
                     key=sensor['ID'][i]),
             ])
    return sensors


def create_device_window(device_elements):
    Dev = [[sg.Frame('', [
        [sg.Text('Подключенные устройства',
                 justification='center',
                 size=(22, 1),
                 font=header_font), sg.Text('')],
        [sg.Frame('',
                  device_elements,
                  background_color="#F0E68C",
                  expand_x=True), sg.Text('')],
        [sg.Button('Выйти',
                   font=button_font,
                   size=(6, 1)),
         sg.Button('Датчики',
                   font=button_font,
                   size=(7, 1))
         ]], key="Device", visible=True, expand_y=True)]]
    return Dev


def create_sensor_window(sensor_elements):
    """
    Создаёт окно с информацией о текущих покзаниях сенсоров.
    :param sensor_elements:
    :return:
    """
    Sen = [[sg.Frame('', [
        [sg.Text('Подключенные датчики',
                 justification='center',
                 size=(22, 1),
                 font=header_font), sg.Text('')],
        [sg.Frame('',
                  sensor_elements,
                  background_color="#F0E68C",
                  expand_x=True), sg.Text('')],
        [sg.Button('Выйти', font=button_font,size=(10, 1)),
            sg.Button('Обновить', font=button_font, size=(8, 1)),
            sg.Button('Устройства',font=button_font, size=(10, 1))]],
        key="Sensor",
        expand_y=True)]]
    return Sen


def Sensors(window_sensors, name_file):
    window_sensors.keep_on_top_set()
    window_sensors.AlphaChannel = 1
    while True:
        event, values = window_sensors.read()
        if event == 'Устройства':
            window_sensors.AlphaChannel = 0
            window_sensors.keep_on_top_clear()
            return 1
        if event == "Обновить":
            if sensor is None:
                new_sensor = read_data(name_file)
            else:
                new_sensor = sensor
            for i in range(len(new_sensor)):
                if (new_sensor['param_value'][i] > new_sensor['max_value'][i]) or\
                        (new_sensor['param_value'][i] < new_sensor['min_value'][i]):
                    print(new_sensor['sensor'][i])
                    colorP = '#CD5C5C'
                else:
                    colorP = '#F0E68C'
                window_sensors[sensor['ID'][i]].update(new_sensor['param_value'][i], colorP)
        if event == 'Выйти' or event == sg.WINDOW_CLOSED:
            window_sensors.alpha_channel = 0
            return 0


def devices(window_dev, window_sensors, device: pandas.DataFrame, sensor, sensor_file):
    def emul_func_device(start: int, end: int, how_many_itter: int, num: int, key: str):
        """
        Эмуляция постепенного изменения значения температуры device
        :param start:
        :param end:
        :param how_many_itter:
        :return:
        """
        start = sensor['param_value'][0]
        global kill_thread

        def em_func(x: float):
            return np.cbrt(x - 1) / 2 + 0.5

        for i in np.linspace(0, 2, how_many_itter):
            sensor['param_value'][0] = int(start + em_func(i) * (end - start))
            while (device['status'][num] == 0):
                if kill_thread:
                    print('Thread is kill')
                    return
                else:
                    time.sleep(0.1)
            # device['param_value'][num] = int(start + em_func(i) * (end - start))  # change state
            device['param_value'][num] = end
            time.sleep(0.1)
            colorP = 0
            window_dev[key].update(int(device['param_value'][num]))
            if (sensor['param_value'][0] > sensor['max_value'][0]) or \
                    (sensor['param_value'][0] < sensor['min_value'][0]):
                # print(new_sensor['sensor'][i])
                colorP = '#CD5C5C'
            else:
                colorP = '#F0E68C'
            window_sensors[sensor['ID'][0]].update(sensor['param_value'][0], colorP)
            if kill_thread:
                return

    k = 1
    n = 0
    global kill_thread
    threads = []
    window_dev.keep_on_top_set()
    window_dev.AlphaChannel = 1
    while k == 1:
        if n == 0:
            window_dev.keep_on_top_clear()
            Warning(sensor)
            window_dev.keep_on_top_set()
            n += 1
        event, values = window_dev.read()

        if event == 'Датчики':
            window_dev.AlphaChannel = 0
            window_dev.keep_on_top_clear()
            k = Sensors(window_sensors, sensor_file)
            window_dev.keep_on_top_set()
            window_dev.AlphaChannel = 1

        if (event != 'Выйти') and event != sg.WINDOW_CLOSED:
            for i in range(len(device)):
                if event == device['device'][i]:
                    if device['status'][i] == 1:
                        input_text = 'Off'
                        device['status'][i] = 0
                        colorB = '#CD5C5C'
                        vis = False
                    else:
                        input_text = 'On'
                        device['status'][i] = 1
                        colorB = '#6B8E23'
                        vis = True
                    window_dev[device['device'][i]].update(input_text, colorB)
                    window_dev[device['ID'][i]].update(visible=vis)

                if event == device['ID'][i]:
                    key = "P" + device['ID'][i]
                    window_dev.keep_on_top_clear()
                    param = params(device['min_value'][i],
                                   device['max_value'][i],
                                   device['step'][i])
                    end_value = popup_select(param)
                    window_dev.keep_on_top_set()
                    if end_value != '':
                        # --------------------------------------
                        # print('key = {}, i = {}, start={}'.format(key, i, device['param_value'][i]))
                        # kill_thread = True
                        # print(f'K-th = {kill_thread}')
                        # time.sleep(1)
                        for t in threads:
                            # kill_thread=
                            t.join()
                        # threads = []
                        # kill_thread = False

                        start_value = int(device['param_value'][i])
                        change_thread = threading.Thread(target=emul_func_device,
                                                         args=(start_value,
                                                               end_value, 80 + 6 * abs(end_value - start_value),
                                                               int(i), key)
                                                         )
                        threads.append(change_thread)

                        change_thread.start()
        else:
            window_dev.alpha_channel = 0
            return device
    window_dev.alpha_channel = 0
    return device


def Warning(sensor):
    """
    Функция проверяет sensor на соответствие нормальному
    диапозону работы. Диапозон задаётся в csv файле.
    :param sensor: массив с данными о сенсорах.
    """
    sen = "False"
    for i in range(len(sensor)):
        if (sensor['param_value'][i] > sensor['max_value'][i]) or (
                sensor['param_value'][i] < sensor['min_value'][i]):
            sen = sensor['sensor'][i]
    layout = [[sg.Text("Внимание! " + sen + " вышел из зоны допустимых значений",
                       font=elements_font)],
              [sg.OK()]]
    if sen != "False":
        window = sg.Window('Датчик', layout=layout)
        event, values = window.read()
        window.close()
        del window


def warning_incorrect_login():
    """
    Выводит окно с ошибкой авторизации (Логин).
    """
    layout = [
        [sg.Text("Пользователя с данным логином не существует. Пожалуйста, повторите опытку",
                 font=elements_font)],
        [sg.OK()]]
    window = sg.Window('Ошибка', layout=layout)
    event, values = window.read()
    window.close()
    del window


def warning_incorrect_password():
    """
    Выводит окно с ошибкой авторизации (пароль).
    """
    layout = [[sg.Text("Неверный пароль. Пожалуйста, повторите опытку",
                       font=elements_font)], [sg.OK()]]
    window = sg.Window('Ошибка', layout=layout)
    event, values = window.read()
    window.close()
    del window


def warning_not_data():
    """
    Выводит окно с ошибкой заполнения.
    """
    layout = [[sg.Text("Не все поля заполнены. Пожалуйста, введите данные",
                       font=elements_font), sg.OK()]]
    window = sg.Window('Ошибка', layout=layout)
    event, values = window.read()
    window.close()
    del window

sg.theme('Kayak')
header_font = ("Arial", 30)
button_font = ("Arial", 16)
elements_font = ("Arial", 14)
slider_font = ("Arial", 12)
back_ground_color = "#F0E68C"
users = read_data("user.csv")

Log_in = [[sg.Frame('', [
    [sg.Text('Добро пожаловать',
             justification='center',
             size=(21, 1),
             font=header_font), sg.Text('')],
    [sg.Frame('', [[sg.Text("Имя пользователя",
                            background_color=back_ground_color,
                            font=elements_font)],
                   [sg.InputText("",
                                 font=elements_font,
                                 key='user_name')],
                   [sg.Text("Пароль",
                            background_color=back_ground_color,
                            font=elements_font)],
                   [sg.InputText("",
                                 password_char="*",
                                 font=elements_font,
                                 key='password')]],
              expand_y=True, background_color=back_ground_color)],
    [sg.Button('Закрыть',
               font=button_font,
               size=(10, 1)),
     sg.Button('Войти', font=button_font, size=(8, 1))
     ]], expand_y=True)]]

window_log = sg.Window('Log in', Log_in,
                       finalize=True,
                       keep_on_top=True,
                       alpha_channel=1)
k = 1
n = 0
flag = 0
while True:
    event, values = window_log.read()
    if event == 'Войти':
        flag = 0
        for i in range(len(users)):
            if users['username'][i] == values['user_name']:
                if users['password'][i] == values['password']:
                    device = pandas.DataFrame()
                    device = read_data(users['device_file'][i])
                    global sensor
                    sensor = None
                    sensor = read_data(users['sensor_file'][i])
                    device_elements = create_device_elements(device)
                    sensor_elements = create_sensor_elements(sensor)
                    Dev = create_device_window(device_elements)
                    Sen = create_sensor_window(sensor_elements)
                    window_log.alpha_channel = 0
                    window_sensors = sg.Window('Sensors', Sen,
                                               finalize=True,
                                               alpha_channel=0,
                                               keep_on_top=False)
                    window_dev = sg.Window('Devices', Dev,
                                           finalize=True,
                                           keep_on_top=False,
                                           alpha_channel=0)
                    new_device = devices(window_dev, window_sensors,
                                         device, sensor,
                                         users['sensor_file'][i])
                    window_log.alpha_channel = 1
                    window_log.keep_on_top_set()
                    new_device.to_csv(users['device_file'][i], encoding='utf-8', index=False)
                    flag = -1
                    break
                else:
                    flag = 1
                    break
        if (values['user_name'] == '' or
                values['password'] == ''):
            flag = 2
        if flag == 1:
            window_log.keep_on_top_clear()
            warning_incorrect_password()
            window_log.keep_on_top_set()
        elif flag == 0:
            window_log.keep_on_top_clear()
            warning_incorrect_login()
            window_log.keep_on_top_set()
        elif flag == 2:
            window_log.keep_on_top_clear()
            warning_not_data()
            window_log.keep_on_top_set()
    if (event == 'Закрыть') or event == sg.WINDOW_CLOSED:
        break
