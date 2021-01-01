
from dataclasses import dataclass
import PySimpleGUI as sg


"""This module defines the layout for the GUI."""

title_font = 'Helvetica 20'
default_font = 'Helvetica 14'
canvas_size = (840, 480) # width, height

@dataclass
class keys:
    CANVAS_TITLE = 'text-canvas-title'
    CANVAS = 'canvas-canvas'

_layout = [
    [sg.Text(text='RTL-SDR Spectrum Analyzer', font=title_font, key=keys.CANVAS_TITLE)],
    [sg.Canvas(size=canvas_size, key=keys.CANVAS)],
]

def layout():
    """Return the layout to be used in call to PySimpleGUI.Window()."""
    return _layout