#!/usr/bin/env python

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, FigureCanvasAgg
from matplotlib.figure import Figure
import numpy as np
from numpy.fft import fft, fftshift, fftfreq
import PySimpleGUI as sg
from rtlsdr import RtlSdr

from rtlsdr_speca import layout
from rtlsdr_speca.layout import keys


def draw_figure(canvas, figure, loc=(0, 0)):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


if __name__ == '__main__':

    window = sg.Window('RTL-SDR Spectrum Analyzer', layout.layout(), finalize=True)

    canvas = window[keys.CANVAS]
    canvas = canvas.TKCanvas

    fig = Figure()
    ax = fig.add_subplot(111)
    ax.set_xlabel("Frequency [Hz]")
    ax.set_ylabel("Log Mag [dBFS]")
    ax.grid()
    fig_agg = draw_figure(canvas, fig)

    canvas_width, canvas_height = layout.canvas_size

    while True:
        event, values = window.read(timeout=10)
        if event == sg.WIN_CLOSED:
            break

        ax.cla()
        ax.grid()
        # TODO Read samples from rtlsdr and take fft
        ax.plot(np.random.randn(10)) # DEBUG
        fig_agg.draw()

    window.close()