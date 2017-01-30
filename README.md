# audio-analysis
Python 3 toolbox for analysing PCM audio, providing an API and a web interface.

## Easy web interface setup using docker
```
docker run -d -p 8080:8080 python:3 bash -c "python -mvenv venv && venv/bin/pip install git+git://github.com/matthiasha/audio-analysis && venv/bin/audio-analysis-server"
```

## Set up web interface using existing Python3 installation
```
python3 -mvenv venv
venv/bin/pip install git+git://github.com/matthiasha/audio-analysis
venv/bin/audio-analysis-server
```
