import PySimpleGUI as sg
import pandas


def params(minE, maxE, step):
    res = []
    c = 0
    for i in range(minE, maxE, step):
        res.append(minE + c)
        c += step
    return res


def popup_select(the_list):
    layout = [[sg.Text("Выберите состояние", font=elements_font),
               sg.Combo(the_list, key='_LIST_', background_color="#F0E68C", font=elements_font,
                        button_background_color="#F0E68C", size=(45, 55), auto_size_text=True), sg.OK()]]
    window = sg.Window('Изменить состояние', layout=layout)
    event, values = window.read()
    window.close()
    del window
    return values['_LIST_']


def read_data(name_file):
    data = pandas.read_csv(name_file, encoding='utf-8', delimiter=",")
    return data


def create_device_elements(device):
    devices = []
    for i in range(len(device)):
        on = "Off"
        colorB = '#CD5C5C'
        if device["status"][i]:
            on = "On"
            colorB = '#6B8E23'
        devices.append([sg.Text(device["device"][i], background_color="#F0E68C", font=elements_font),
                        sg.Text(device['param_name'][i] + ":", background_color="#F0E68C", font=elements_font),
                        sg.Text(device['param_value'][i], background_color="#F0E68C", font=elements_font,
                                key="P" + device['ID'][i]),
                        sg.Button(button_text="Изменить",
                                  font=slider_font,
                                  tooltip='Изменить состояние устройства', key=device['ID'][i]),
                        sg.Button(button_text=on,
                                  font=slider_font, key=device["device"][i],
                                  button_color=colorB)])
    return devices


def create_sensor_elements(sensor):
    sensors = []
    for i in range(len(sensor)):
        colorB = '#CD5C5C'
        if (sensor["param_value"][i] <= sensor["max_value"][i]) and (
                sensor["param_value"][i] >= sensor["min_value"][i]):
            colorB = '#F0E68C'
        sensors.append([sg.Text(sensor["sensor"][i], background_color=colorB, font=elements_font),
                        sg.Text(sensor['param_name'][i] + ":", background_color=colorB, font=elements_font),
                        sg.Text(sensor['param_value'][i], background_color=colorB, font=elements_font,
                                key=sensor['ID'][i]),
                        ])
    return sensors


def Sensors(window_sensors):
    window_sensors.keep_on_top_set()
    window_sensors.AlphaChannel = 1
    while True:
        event, values = window_sensors.read()
        if event == 'Устройства':
            window_sensors.AlphaChannel = 0
            window_sensors.keep_on_top_clear()
            return 1
        if event == "Обновить":
            new_sensor = read_data("New_sensors.csv")
            colorP = '#F0E68C'
            for i in range(len(new_sensor)):
                if new_sensor['param_value'][i] != sensor['param_value'][i]:
                    if (new_sensor['param_value'][i] > new_sensor['max_value'][i]) or (
                            new_sensor['param_value'][i] < new_sensor['min_value'][i]):
                        colorP = '#CD5C5C'
                    window_sensors[sensor['ID'][i]].update(new_sensor['param_value'][i], colorP)
        if event == 'Выйти' or event == sg.WINDOW_CLOSED:
            return 0


def Warning(sensor):
    sen = "False"
    for i in range(len(sensor)):
        if (sensor['param_value'][i] > sensor['max_value'][i]) or (
                    sensor['param_value'][i] < sensor['min_value'][i]):
            sen = sensor['sensor'][i]
    layout = [[sg.Text("Внимание! "+sen+" вышел из зоны допустимых значений", font=elements_font)],
              [sg.OK()]]
    if sen != "False":
        window = sg.Window('Датчик', layout=layout)
        event, values = window.read()
        window.close()
        del window



sg.theme('Kayak')
header_font = ("Arial", 30)
button_font = ("Arial", 16)
elements_font = ("Arial", 14)
slider_font = ("Arial", 12)

device = read_data("New_devices.csv")
sensor = read_data("New_sensors.csv")

device_elements = create_device_elements(device)
sensor_elements = create_sensor_elements(sensor)

Dev = [[sg.Frame('', [
    [sg.Text('Подключенные устройства', justification='center', size=(22, 1), font=header_font), sg.Text('')],
    [sg.Frame('', device_elements, background_color="#F0E68C", expand_x=True), sg.Text('')],
    [sg.Button('Выйти', font=button_font, size=(6, 1)),
     sg.Button('Датчики', font=button_font, size=(7, 1))
     ]], key="Device", visible=True, expand_y=True)]]

Sen = [[sg.Frame('', [
    [sg.Text('Подключенные датчики', justification='center', size=(22, 1), font=header_font), sg.Text('')],
    [sg.Frame('', sensor_elements, background_color="#F0E68C", expand_x=True), sg.Text('')],
    [sg.Button('Выйти', font=button_font, size=(10, 1)), sg.Button('Обновить', font=button_font, size=(8, 1)),
     sg.Button('Устройства', font=button_font, size=(10, 1))
     ]], key="Sensor", expand_y=True)]]

window_sensors = sg.Window('Sensors', Sen, finalize=True, alpha_channel=0, keep_on_top=False)
window_dev = sg.Window('Devices', Dev, finalize=True, keep_on_top=False)
k = 1
n=0
while k == 1:
    if n == 0:
        Warning(sensor)
        n+=1
    event, values = window_dev.read()
    window_dev.AlphaChannel = 1
    if event == 'Датчики':
        window_dev.AlphaChannel = 0
        window_dev.keep_on_top_clear()
        k = Sensors(window_sensors)
        window_dev.keep_on_top_set()
        window_dev.AlphaChannel = 1
    if (event != 'Выйти') and event != sg.WINDOW_CLOSED:
        for i in range(len(device)):
            if event == device['device'][i]:
                if device['status'][i] == 1:
                    input_text = 'Off'
                    device['status'][i] = 0
                    colorB = '#CD5C5C'
                else:
                    input_text = 'On'
                    device['status'][i] = 1
                    colorB = '#6B8E23'
                window_dev[device['device'][i]].update(input_text, colorB)
            if event == device['ID'][i]:
                key = "P" + device['ID'][i]
                window_dev.keep_on_top_clear()
                param = params(device['min_value'][i], device['max_value'][i], device['step'][i])
                nbr = popup_select(param)
                window_dev.keep_on_top_set()
                window_dev[key].update(nbr)
                device['param_value'][i] = nbr
    else:
        break

device.to_csv("New_devices.csv", encoding='utf-8', index=False)
