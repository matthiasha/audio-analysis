import numpy as np
import scipy.io.wavfile


class PCMArray(np.ndarray):
    def __new__(cls, f):
        sample_rate, a = scipy.io.wavfile.read(f)
        # import pdb;pdb.set_trace()
        obj = np.transpose(a).view(cls)
        # set the new 'info' attribute to the value passed
        obj.sample_rate = sample_rate
        # Finally, we must return the newly created object:
        return obj

    def __array_finalize__(self, obj):
        if obj is None: 
            return
        self.sample_rate = getattr(obj, 'sample_rate', None)
