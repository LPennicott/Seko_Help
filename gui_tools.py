import sys

import PySimpleGUI as sg


def _standard_get_folder():
    sg.theme("Light Blue 2")

    layout = [
        [sg.Text("Select folder")],
        [sg.Input(key="-FOLDER-"), sg.FolderBrowse()],
        [sg.Submit(), sg.Cancel()],
    ]

    window = sg.Window("Select folder", layout)

    event, values = window.read()

    if event in (sg.WIN_CLOSED, "Cancel"):
        sys.exit()

    folder = values["-FOLDER-"]
    window.close()
    return folder
