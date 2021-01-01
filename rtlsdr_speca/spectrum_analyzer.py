
import numpy as np
from numpy.fft import fft, fftshift
from rtlsdr import RtlSdr
from rtlsdr.rtlsdr import BaseRtlSdr

DEFAULT_FC = BaseRtlSdr.DEFAULT_FC
DEFAULT_RS = BaseRtlSdr.DEFAULT_RS
DEFAULT_READ_SIZE = BaseRtlSdr.DEFAULT_READ_SIZE

VALID_TRACE_MODES = ('CLEAR_WRITE', 'MAX HOLD', 'MIN HOLD')

class SpectrumAnalyzer:

    def __init__(self, center_freq: float = DEFAULT_FC, bandwidth: float = DEFAULT_RS,
                 points: int = DEFAULT_READ_SIZE, trace_mode: str = 'CLEAR WRITE'):

        self._points = points
        self._trace_mode = trace_mode

        try:
            self._sdr = RtlSdr()
            self._sdr.sample_rate = bandwidth
            self._sdr.bandwidth = 0 # auto
            self._sdr.center_freq = center_freq
            self._sdr.freq_correction = 60 # ppm
            self._sdr.gain = 'auto'
            self._connected = True
        except:
            self._sdr = None
            self._connected = False

    @property
    def bandwidth(self) -> float:
        return self._sdr.sample_rate

    @bandwidth.setter
    def bandwidth(self, bw: float) -> None:
        self._sdr.sample_rate = float(bw)

    @property
    def center_freq(self) -> float:
        return self._sdr.center_freq

    @center_freq.setter
    def center_freq(self, cf: float) -> None:
        self._sdr.center_freq = float(cf)

    def connect(self, device_index: int = 0):
        try:
            self._sdr = RtlSdr(device_index=device_index)
            self._connected = True
        except:
            self._sdr = None
            self._connected = False

    @property
    def connected(self) -> bool:
        return self._connected

    @property
    def points(self) -> int:
        return self._points

    @points.setter
    def points(self, p: int):
        self._points = int(p)

    @property
    def trace_mode(self) -> str:
        return self._trace_mode

    @trace_mode.setter
    def trace_mode(self, tm: str):
        tm = tm.upper()
        if tm in VALID_TRACE_MODES:
            self._trace_mode = tm

    @property
    def sdr(self) -> RtlSdr:
        return self._sdr

    def capture(self) -> np.ndarray:
        if not self.connected:
            return np.ndarray(np.zeros(self.points))
        iq = self._sdr.read_samples(self.points)
        return 20 * np.log10(np.abs(fftshift(fft(iq)/len(iq))))




