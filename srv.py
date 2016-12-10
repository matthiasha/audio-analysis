from flask import Flask, request, send_from_directory
import bokeh.resources
import bokeh.embed

import audio
import tools


# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='')

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route('/')
def root():
    return app.send_static_file('index.html')
    
@app.route('/upload', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['uploadfile']
        pcm = audio.PCMArray(f)[0]
        plot = tools.spectrum(pcm).plot()
        script, div = bokeh.embed.components(plot)
        return div + script
        # return bokeh.embed.file_html(plot, bokeh.resources.CDN)

if __name__ == "__main__":
    app.run(host='0.0.0.0',
            port=8080)
    