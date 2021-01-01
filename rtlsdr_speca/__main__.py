#!/usr/bin/env python

import tkinter
root = tkinter.Tk()
dpi = root.winfo_fpixels('1i')
root.destroy()


from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, FigureCanvasAgg
from matplotlib.figure import Figure
import numpy as np
from numpy.fft import fftshift, fftfreq
import PySimpleGUI as sg
from rtlsdr import RtlSdr

from rtlsdr_speca import layout
from rtlsdr_speca.layout import Keys
from rtlsdr_speca.spectrum_analyzer import SpectrumAnalyzer


def init_figure():
    fig = Figure()
    w, h = layout.canvas_size
    fig.set_figwidth(w/dpi)
    fig.set_figheight(h/dpi)
    ax = fig.add_subplot(111)
    ax.set_xlabel("Frequency [kHz]")
    ax.set_ylabel("Log Mag [dBFS]")
    ax.set_ylim((-90, 10))
    ax.grid()
    return fig, ax


def draw_figure(canvas, figure, loc=(0, 0)):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


def reset_axis(ax, ylim: tuple = (-90, 10)):
    ax.cla()
    ax.set_xlabel('Frequency [kHz]')
    ax.set_ylabel('Log Mag [dBFS]')
    ax.set_ylim(ylim)
    ax.grid()


if __name__ == '__main__':

    window = sg.Window('RTL-SDR Spectrum Analyzer', layout.layout(), finalize=True)

    canvas = window[Keys.CANVAS]
    canvas = canvas.TKCanvas

    fig, ax = init_figure()
    fig_agg = draw_figure(canvas, fig)

    canvas_width, canvas_height = layout.canvas_size

    sa = SpectrumAnalyzer()
    if sa.connected:
        f = fftshift(fftfreq(sa.points, d=1/sa.bandwidth)) / 1e3 # kHz
    else:
        f = np.linspace(-0.5, 0.5, sa.points)
        ax.set_xlim((-0.5, 0.5))

    while True:
        event, values = window.read(timeout=1)
        if event == sg.WIN_CLOSED:
            break

        if sa.connected:
            reset_axis(ax)
            power_spectrum = sa.capture()
            ax.plot(f, power_spectrum)
            fig_agg.draw()

        else:
            sa.connect()

    window.close()