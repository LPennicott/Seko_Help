import PySimpleGUI as sg
from fix_false_onfile import process_files

sg.theme('Light Blue 2')

layout = [[sg.Text('Select csv file')],
          [sg.Input(key='-CSVFILE-'), sg.FileBrowse()],
          [sg.Text('Select xml file')],
          [sg.Input(key='-XMLFILE-'), sg.FileBrowse()],
          [sg.Text('Select save location')],
          [sg.Input(key='-SAVE_LOCATION-'), sg.FolderBrowse()],
          [sg.Submit(), sg.Cancel()]]

window = sg.Window('Select File', layout)

event, values = window.read()

csvfile = values['-CSVFILE-']
xmlfile = values['-XMLFILE-']
save_location = values['-SAVE_LOCATION-']
print(save_location)
window.close()

if csvfile.endswith('csv') and xmlfile.endswith('xml'):
    process_files(csvfile, xmlfile, save_location)
else:
    print('error')
