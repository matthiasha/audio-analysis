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
                                    y_axis_label=self.ylabel, 
                                    sizing_mode='stretch_both')
        fig.line(self.x, self.y)
        return fig
        
    def __getitem__(self, key):
        return np.interp(key, self.x, self.y)


def spectrum(pcm, nfft=None):
    assert len(pcm.shape) == 1, 'only applicable to 1D data'
    if nfft is None:
        nfft = 1
        while nfft * 2 < pcm.sample_rate and nfft * 2 < len(pcm):
            nfft *= 2
    f, l = scipy.signal.csd(pcm, pcm, pcm.sample_rate, 
                            nperseg=nfft, scaling='spectrum')
    l = 10 * np.log10(l * 2)  # +3dB, dBFS sine scaling
    return Data2D(f, 'frequency [Hz]', 
                  l, 'level [dBFS sine]')
                  