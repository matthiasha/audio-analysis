import flask
import flask_compress
import bokeh.resources
import bokeh.embed
import hashlib
import functools

import audio
import tools


app = flask.Flask(__name__)
flask_compress.Compress(app)


@app.route('/static/<path:path>')
def send_static(path):
    return flask.send_from_directory('static', path)


@app.route('/')
def root():
    return flask.send_from_directory('static', 'index.html')


def hash(f):
    d = hashlib.sha1()
    for buf in iter(functools.partial(f.read, 512), b''):
        d.update(buf)
    f.seek(0)
    return d.hexdigest()[:6]


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if flask.request.method == 'POST':
        f = flask.request.files['uploadfile']
        uid = hash(f)
        f.save(uid + '.wav')
        return '/wav/' + uid


@app.route('/wav/<uid>')
def file_info(uid):
    f = uid + '.wav'
    pcm = audio.PCMArray(f)
    return flask.render_template('wav-tpl.html', uuid=uid, channels=range(pcm.shape[0]))


@app.route('/wav/<uid>/<int:channel>/<tool>')
def tool(uid, channel, tool):
    f = uid + '.wav'
    pcm = audio.PCMArray(f)[channel]
    assert tool in ('spectrum', 'power')
    plot = getattr(tools, tool)(pcm).plot()
    return bokeh.embed.file_html(plot, bokeh.resources.CDN)


if __name__ == "__main__":
    app.run(host='0.0.0.0',
            port=8080)
