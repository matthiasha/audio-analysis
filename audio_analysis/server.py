import sys
import os
import argparse
import hashlib
import functools
import flask
import flask_compress
import bokeh.resources
import bokeh.embed
import bokeh.palettes
from . import audio
from . import tools

here = os.path.abspath(os.path.dirname(__file__))
app = flask.Flask(__name__, root_path=here)
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

    def num_ch(uid):
        return audio.PCMArray(uid + '.wav').shape[0]

    return flask.render_template('wav-tpl.html',
                                 elements=[{'uid': uid, 'name': filenames.get(uid, uid), 'ch': ch}
                                           for uid in uids for ch in range(num_ch(uid))]
                                 )


@app.route('/plot')
def plot():
    tool = flask.request.args['tool']
    assert tool in ('spectrum', 'power')
    fig = None
    elements = [el.split('-') for el in flask.request.args.getlist('e')]
    if not len(elements):
        return 'Please make a selection. <a href="javascript:history.back()">Go back</a>'
    palette = bokeh.palettes.brewer['Set1'][max(len(elements), 3)][:len(elements)]
    for (uid, ch), color in zip(elements, palette):
        ch = int(ch)
        pcm = audio.PCMArray(uid + '.wav')[ch]
        legend = '%s ch%i' % (filenames.get(uid, uid), ch)
        fig = getattr(tools, tool)(pcm).plot(fig=fig, legend=legend, color=color)
    return bokeh.embed.file_html(fig, bokeh.resources.CDN)


def main(argv):
    parser = argparse.ArgumentParser(description='Run the web server.',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--ip', default='0.0.0.0',
                        help='set an IP adress to listen on')
    parser.add_argument('--port', type=int, default='8080', 
                        help='set a port to listen on')
    args = parser.parse_args(argv)
    app.run(host=args.ip, port=args.port)


def _cli():
    main(sys.argv[1:])


if __name__ == "__main__":
    _cli()

