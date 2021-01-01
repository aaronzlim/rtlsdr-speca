
from dataclasses import dataclass
import PySimpleGUI as sg


"""This module defines the layout for the GUI."""

sg.theme('Blue Mono')
title_font = 'Helvetica 20'
default_font = 'Helvetica 14'
canvas_size = (600, 480) # width, height

@dataclass
class Keys:
    CANVAS_TITLE = 'text-canvas-title'
    CANVAS = 'canvas-canvas'
    COLUMN_CONTROL_PANEL = 'column-control-panel'
    TEXT_CENTER_FREQUENCY = 'text-center-frequency'
    TEXT_BANDWIDTH = 'text-bandwidth'

_control_panel_layout = [
    [
        sg.Text(text='Center Freq [MHz]', font=default_font, key=Keys.TEXT_CENTER_FREQUENCY),
        sg.InputText(default_text='80.0', font=default_font)
    ],
    [
        sg.Text(text='Bandwidth [MHz]  ', font=default_font, key=Keys.TEXT_BANDWIDTH),
        sg.InputText(default_text='1.024', font=default_font)
    ],
]

_layout = [
    [
        sg.Canvas(size=canvas_size, key=Keys.CANVAS),
        sg.Column(layout=_control_panel_layout, size=(240, canvas_size[1]), key=Keys.COLUMN_CONTROL_PANEL)
    ],
]

def layout():
    """Return the layout to be used in call to PySimpleGUI.Window()."""
    return _layout