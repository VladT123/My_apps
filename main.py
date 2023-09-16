import PySimpleGUI as sg
from bs4 import BeautifulSoup as bs
import requests
from googletrans import Translator, constants

translator = Translator()

def get_weather_data(location):
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
    url = f'https://www.google.com/search?q=weather+in+{location}'
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    html = session.get(url)
    soup = bs(html.text, 'html.parser')
    name = soup.find('span', attrs={'class': 'BBwThe'}).text
    time = soup.find('div', attrs={'id': 'wob_dts'}).text
    weather = soup.find('span', attrs={'id': 'wob_dc'}).text
    temp = soup.find('span', attrs={'id': 'wob_tm'}).text
    translation = translator.translate(weather)
    print(f"{translation.origin} ({translation.src}) --> {translation.text} ({translation.dest})")

    return name, time, weather, temp, translation.text

    # print(time)
    # print(weather)
    # print(temp)

sg.theme('darkpurple')
image_col = sg.Column([[sg.Image(key='-IMAGE-', background_color='#FFFFFF')]])

info_col = sg.Column([
    [sg.Text('', key='-LOCATION-', font='Papyrus 30', pad=0, visible=False)],
    [sg.Text('', key='-TIME-', font='Papyrus 16', pad=0, visible=False)],
    [sg.Text('', key='-TEMP-', font='Papyrus 16',
             pad=(0, 10), justification='center', visible=False)]
    ],key='-RIGHT-')


layout = [
    [sg.Input(expand_x=True, key='-INPUT-'), sg.Button('Enter', button_color='#000000', border_width=0)],
    [image_col, info_col]
]

window = sg.Window('Weather App', layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break

    if event == 'Enter':
        name, time, weather, temp, translation = get_weather_data(values['-INPUT-'])
        window['-LOCATION-'].update(name, visible=True)
        window['-TIME-'].update(time.split(' ')[0], visible=True)
        window['-TEMP-'].update(f' {temp} \u2103 ({weather})', visible=True)
        print(translation)
        # sun
        if translation in ('Sun', 'Sunny', 'Clear', 'Clear with periodic clouds', 'Mostly sunny', 'Advantage sunny', 'Sure'):
            window['-IMAGE-'].update('symbols/sun.png')

        # part sun
        if translation in ('Partly Sunny', 'Mostly Sunny', 'Partly cloudy', 'Mostly cloudy', 'Cloudy', 'Overcast'):
            window['-IMAGE-'].update('symbols/part sun.png')

        # rain
        if translation in ('Rain', 'Chance of Rain', 'Light Rain', 'Showers', 'Scattered Showers', 'Rain and Snow', 'Hail'):
            window['-IMAGE-'].update('symbols/rain.png')

        # thunder
        if translation in ('Scattered Thunderstorms', 'Chance of Storm', 'Storm', 'Thunderstorm', 'Chance of TStorm'):
            window['-IMAGE-'].update('symbols/thunder.png')

        # foggy
        if translation in ('Mist', 'Dust', 'Fog', 'Smoke', 'Haze', 'Flurries'):
            window['-IMAGE-'].update('symbols/fog.png')

        # snow
        if translation in ('Freezing Drizzle', 'Chance of Snow', 'Sleet', 'Snow', 'Icy', 'Snow Showers'):
            window['-IMAGE-'].update('symbols/snow.png')


window.close()
