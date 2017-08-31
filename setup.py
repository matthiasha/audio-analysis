import os
import setuptools


here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md')) as f:
    long_description = f.read()

setuptools.setup(
    name='audio-analysis',
    use_scm_version=True, #version='0.1',
    install_requires=['numpy', 'scipy', 'bokeh', 'flask', 'flask-compress', 'pandas'],
    setup_requires=['setuptools_scm',],
    description='Tools for analyzing and audio files and plotting the results.',
    long_description=long_description,
    url='https://github.com/matthiasha/audio-analysis',
    author='Matthias Hafner',
    author_email='hafner87@gmail.com',
    packages=['audio_analysis'],
    include_package_data=True,
    entry_points={'console_scripts': 
                    ['audio-analysis-server=audio_analysis.server:_cli'],
                  },
)

