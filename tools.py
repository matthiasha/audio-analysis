import scipy.signal
import numpy as np
import bokeh.plotting


class Data2D(object):
    def __init__(self, x, xlabel, y, ylabel):
        self.x = x
        self.y = y
        self.xlabel = xlabel
        self.ylabel = ylabel
        
    def plot(self):
        fig = bokeh.plotting.figure(x_axis_label=self.xlabel,
                                    y_axis_label=self.ylabel)
        fig.line(self.x, self.y)
        return fig


def spectrum(pcm, nfft=None):
    if nfft is None:
        nfft = 1
        while nfft * 2 < pcm.sample_rate and nfft * 2 < len(pcm):
            nfft *= 2
    f, l = scipy.signal.csd(pcm, pcm, pcm.sample_rate, 
                            nperseg=nfft, scaling='spectrum')
    return Data2D(f, 'frecuency [Hz]', l, 'level [dBFS]')