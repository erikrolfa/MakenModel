"""
MakenModel index (main) view

URLS include:
/
"""

import flask
import arrow
import makenmodel


@makenmodel.app.route('/')
def show_index():
    '''Route for '/' url'''

    logname = flask.session.get('username')


    context = {"logname": logname}

    return flask.render_template("index.html", **context)
