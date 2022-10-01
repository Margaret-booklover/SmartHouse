import PySimpleGUI as sg

sg.theme('Kayak')
header_font = ("Arial", 30)
button_font = ("Arial", 16)
elements_font = ("Arial", 14)
slider_font = ("Arial", 12)
frame_elements = [
    [sg.Text('    Чайник', background_color="#F0E68C", font=elements_font),
     sg.Slider(range=(0, 1), default_value=0, size=(6, 15), orientation='h', font=slider_font,
               tooltip='Изменить состояние устройства', disable_number_display=True)],
    [sg.Text('    Утюг', background_color="#F0E68C", font=elements_font),
     sg.Slider(range=(0, 1), default_value=0, size=(6, 15), orientation='h', font=slider_font,
               tooltip='Изменить состояние устройства', disable_number_display=True)],
        [sg.Text('    Мультиварка', background_color="#F0E68C", font=elements_font),
     sg.Slider(range=(0, 1), default_value=0, size=(6, 15), orientation='h', font=slider_font,
               tooltip='Изменить состояние устройства', disable_number_display=True)],
    [sg.Text('    Робот-пылесос', background_color="#F0E68C", font=elements_font),
     sg.Slider(range=(0, 1), default_value=0, size=(6, 15), orientation='h', font=slider_font,
               tooltip='Изменить состояние устройства', disable_number_display=True)]
]
layout = [
    [sg.Text('Подключенные устройства', justification='center', size=(22, 1), font=header_font)
     ],
    [sg.Text('')],
    [sg.Frame('', frame_elements, background_color="#F0E68C", expand_x=True)],
    # [sg.Sizer(150,150)],
    [sg.Text('')],
    [sg.Button('Exit', font=button_font, size=(6, 1))]
]
window = sg.Window('Smart House', layout)
while True:  # The Event Loop
    event, values = window.read()
    # print(event, values) #debug
    if event in (None, 'Exit'):
        break
