import os
from audio_analysis import tools
from audio_analysis import audio
import numpy as np
import pytest

here = os.path.abspath(os.path.dirname(__file__))

TOLERANCE_DB = 0.1  # TODO: decrease
FILES = {'1000Hz_-3dBFS_3s.wav': (1000, -3),
         '1000Hz_-6dBFS_3s.wav': (1000, -6),
         '440Hz_-6dBFS_3s.wav': (440, -6),
         '2345Hz_-14dBFS_3s.wav': (2345, -14),
         '5600Hz_-10dBFS_3s.wav': (5600, -10),
        }


def lin(dbfs):
    return 10 ** (dbfs / 20)


@pytest.mark.parametrize('file', FILES.keys())
def test_pcmarray(file):
    hz, dbfs = FILES[file]
    ch = 0
    pcm = audio.PCMArray(os.path.join(here, file))[ch]
    assert min(abs(pcm)) < lin(TOLERANCE_DB)
    assert abs(max(pcm) - lin(dbfs)) < TOLERANCE_DB
    

@pytest.mark.parametrize('file', FILES.keys())
def test_spectrum(file):
    TOLERANCE_DB = 1.5  # TODO: decrease
    hz, dbfs = FILES[file]
    ch = 0
    pcm = audio.PCMArray(os.path.join(here, file))[ch]
    s = tools.spectrum(pcm)
    assert abs(s.interp(hz) - dbfs) < TOLERANCE_DB
    
    
@pytest.mark.parametrize('file', FILES.keys())
def test_power(file):
    hz, dbfs = FILES[file]
    ch = 0
    pcm = audio.PCMArray(os.path.join(here, file))[ch]
    p = tools.power(pcm, window=1023)
    assert all(abs(p - dbfs) < TOLERANCE_DB + .1)
    assert abs(p.mean() - dbfs) < TOLERANCE_DB
    
