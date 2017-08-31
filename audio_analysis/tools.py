import scipy.signal
import numpy as np
import bokeh.plotting
import bokeh.models
import pandas


def new_data(x, xlabel, y, ylabel):
    return Data2D(y, index=pandas.Index(x, name=xlabel), name=ylabel)


class Data2D(pandas.Series):
    _metadata = '_x2_factor _x2_label'.split()
    
    @property
    def _constructor(self):
        return Data2D
    
    def plot(self, fig=None, legend=None, color=None):
        # TODO: factor might be different plotting twice in same figure - how to check?
        if fig is None:
            fig = bokeh.plotting.figure(x_axis_label=self.index.name,
                                        y_axis_label=self.name,
                                        sizing_mode='stretch_both')
            # increase the limit for sci. notation on x-axis
            fig.xaxis.formatter = bokeh.models.BasicTickFormatter(power_limit_high=6)
            if self._x2_factor is not None:
                x2_ax = bokeh.models.LinearAxis(axis_label=self._x2_label)
                js_code = "return Math.round(tick * %f * 100) / 100" % self._x2_factor
                x2_ax.formatter = bokeh.models.FuncTickFormatter(code=js_code)
                fig.add_layout(x2_ax, 'above')
        fig.line(self.index, self, legend=legend, line_color=color)
        return fig
        
    def add_x_axis(self, factor, label):
        assert self._x2_factor is None, 'only 2 x-axis possible' 
        self._x2_factor = factor
        self._x2_label = label


def _dbfs(sq):
    return 10 * np.log10(sq * 2)  # +3dB, dBFS sine scaling


def spectrum(pcm, nfft=None):
    assert len(pcm.shape) == 1, 'only applicable to 1D data'
    if nfft is None:
        nfft = 1
        while nfft * 2 < pcm.sample_rate and nfft * 2 < len(pcm):
            nfft *= 2
    f, l_sq = scipy.signal.csd(pcm, pcm, pcm.sample_rate, 
                            nperseg=nfft, scaling='spectrum')
    l = _dbfs(l_sq) 
    return new_data(f, 'frequency [Hz]', 
                    l, 'level [dBFS sine]')
        
                  
def power(pcm, window=1023):
    assert len(pcm.shape) == 1, 'only applicable to 1D data'
    if len(pcm) % window:
        # truncate samples to be multiple of window
        pcm = pcm[:-(len(pcm) % window)]
    reshaped = pcm.reshape(-1, window)
    i = np.arange(len(pcm)).reshape(-1, window).mean(1)
    # calculate power per window
    p = _dbfs(np.mean(reshaped ** 2, 1)) 
    d2d = new_data(i, 'samples', 
                   p, 'level [dBFS sine]')
    d2d.add_x_axis(1 / pcm.sample_rate, 'time [s]')
    return d2d
    
