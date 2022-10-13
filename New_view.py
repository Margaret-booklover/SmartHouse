import PySimpleGUI as sg
import pandas

def params(minE, maxE):
    res = []
    c = 0
    for i in range(minE, maxE):
        res.append(minE + c)
        c += 1
    return res

sg.theme('Kayak')
header_font = ("Arial", 30)
button_font = ("Arial", 16)
elements_font = ("Arial", 14)
slider_font = ("Arial", 12)

data = pandas.read_csv("devices.csv", encoding='cp1251', delimiter=";")

frame_elements = []
for i in range(len(data)):
    on = "Off"
    colorB = '#CD5C5C'
    param = params(data['min'][i], data['max'][i])
    if data["on"][i]:
        on = "On"
        colorB = '#6B8E23'
    frame_elements.append([sg.Text(data["device"][i], background_color="#F0E68C", font=elements_font),
                           sg.Combo(param, default_value=data['default'][i], background_color="#F0E68C",
                                    font=elements_font),
                           sg.Button(button_text=on,
                                     font=slider_font,
                                     tooltip='Изменить состояние устройства', key=data["device"][i],
                                     button_color=colorB)])

layout = [
    [sg.Text('Подключенные устройства', justification='center', size=(22, 1), font=header_font)
     ],
    [sg.Text('')],
    [sg.Frame('', frame_elements, background_color="#F0E68C", expand_x=True)],
    [sg.Text('')],
    [sg.Button('Exit', font=button_font, size=(6, 1))]
]
window = sg.Window('Smart House', layout)
while True:  # The Event Loop
    event, values = window.read()
    if event != 'Exit':
        for i in range(len(data)):
            if event == data['device'][i]:
                if data['on'][i] == 1:
                    input_text = 'Off'
                    data['on'][i] = 0
                    colorB = '#CD5C5C'
                else:
                    input_text = 'On'
                    data['on'][i] = 1
                    colorB = '#6B8E23'
                window[data['device'][i]].update(input_text, colorB)
    else:
        break
