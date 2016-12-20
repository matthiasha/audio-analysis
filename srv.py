import flask
import flask_compress
import bokeh.resources
import bokeh.embed
import bokeh.palettes
import hashlib
import functools

import audio
import tools


app = flask.Flask(__name__)
flask_compress.Compress(app)
filenames = {}


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
        filenames[uid] = f.filename
        f.save(uid + '.wav')
        return uid


@app.route('/wav/<uids_str>')
def file_info(uids_str):
    uids = uids_str.strip(',').split(',')
    num_channels = [audio.PCMArray(uid + '.wav').shape[0] for uid in uids]
    if len(set(num_channels)) != 1:
        return 'Comparing files only with same amount of channels. Given numbers of channels: %s' % num_channels
    return flask.render_template('wav-tpl.html',
                                 names=[filenames.get(uid, uid) for uid in uids],
                                 uuid=uids_str,
                                 channels=range(num_channels[0]))


@app.route('/wav/<uids_str>/<int:channel>/<tool>')
def tool(uids_str, channel, tool):
    assert tool in ('spectrum', 'power')
    fig = None
    uids = uids_str.strip(',').split(',')
    pcms = [audio.PCMArray(uid + '.wav')[channel] for uid in uids]
    palette = bokeh.palettes.brewer['Set1'][max(len(uids), 3)][:len(uids)]
    for uid, pcm, color in zip(uids, pcms, palette):
        legend = '%s ch%i' % (filenames.get(uid, uid), channel)
        fig = getattr(tools, tool)(pcm).plot(fig=fig, legend=legend, color=color)
    return bokeh.embed.file_html(fig, bokeh.resources.CDN)


if __name__ == "__main__":
    app.run(host='0.0.0.0',
            port=8080)
