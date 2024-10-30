'''Init file for project'''

import flask

app = flask.Flask(__name__)

app.config.from_object('makenmodel.config')

app.config.from_envvar('MAKENMODEL_SETTINGS', silent=True)


import makenmodel.views # noqa: E402  pylint: disable=wrong-import-position
import makenmodel.model # noqa: E402  pylint: disable=wrong-import-position

@app.route('/uploads/<path:filename>')
def serve_uploads(filename):
    """Serves files from uploads"""
    return flask.send_from_directory(app.config['UPLOAD_FOLDER'], filename)
