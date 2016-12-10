import flask
import bokeh.resources
import bokeh.embed

import audio
import tools


# set the project root directory as the static folder, you can set others.
app = flask.Flask(__name__, static_url_path='')

@app.route('/static/<path:path>')
def send_static(path):
    return flask.send_from_directory('static', path)

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/upload/<int:channel>/<tool>', methods = ['GET', 'POST'])
def upload_file(channel, tool):
    if flask.request.method == 'POST':
        f = flask.request.files['uploadfile']
        pcm = audio.PCMArray(f)[channel]
        assert tool in ('spectrum', 'power')
        plot = getattr(tools, tool)(pcm).plot()
        return bokeh.embed.file_html(plot, bokeh.resources.CDN)

if __name__ == "__main__":
    app.run(host='0.0.0.0',
            port=8080)
    