import numpy as np
import scipy.io.wavfile


def _floatify(x):
    formula = {'uint8': lambda a: (a / 2 ** 7) - 1,
               'int16': lambda a: a / 2 ** 15,
               'int32': lambda a: a / 2 ** 31,
               }
    if 'float' in str(x.dtype):
        return x
    else:
        return formula[str(x.dtype)](x.astype('float32'))
               

class PCMArray(np.ndarray):
    def __new__(cls, f):
        sample_rate, a = scipy.io.wavfile.read(f)
        pcm = _floatify(np.transpose(a)).view(cls)
        if len(pcm.shape) == 1:
            pcm = pcm.reshape((1, -1))
        pcm.sample_rate = sample_rate
        return pcm

    def __array_finalize__(self, obj):
        if obj is None: 
            return
        self.sample_rate = getattr(obj, 'sample_rate', None)
