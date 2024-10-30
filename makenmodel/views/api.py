"""
MakenModel api routes

URLS include:
/api/brands
/api/paints
"""

import flask
import makenmodel



@makenmodel.app.route('/api/brands/', methods=['GET'])
def get_brands():
    '''Returns all brands'''

    connection = makenmodel.model.get_db()

    search_term = flask.request.args.get('term', '')

    cur = connection.execute(
        "SELECT brand FROM brands WHERE brand LIKE ?",
        ('%' + search_term + '%',)
    )

    brands = [row['brand'] for row in cur.fetchall()]

    return flask.jsonify(brands)

@makenmodel.app.route('/api/paints/', methods=['GET'])
def get_paints():
    '''Returns paints from database'''

    connection = makenmodel.model.get_db()

    brand = flask.request.args.get('brand', '')
    term = flask.request.args.get('term', '')
    exact_match = flask.request.args.get('exactMatch', '') == 'true'

    # brand = 'Tamiya'
    # term = 'Black'
    like_term = f'%{term}%'

    if exact_match:
        cur = connection.execute(
            "SELECT paint_name, paint_code, paint_type FROM paints "
            "WHERE brand = ? AND (paint_name LIKE ? OR paint_code == ?)",
            (brand, like_term, term)
        )

    else:
        cur = connection.execute(
            "SELECT paint_name, paint_code, paint_type FROM paints "
            "WHERE brand = ? AND (paint_name LIKE ? OR paint_code LIKE ?)",
            (brand, like_term, like_term)
        )

    paint_matches = cur.fetchall()

    paint_matches = [(row['paint_name'], row['paint_code'], row['paint_type']) for row in paint_matches]

    results = [{'paint_name': paint_name, 'paint_code': paint_code, 'paint_type': paint_type } for paint_name, paint_code, paint_type in paint_matches]

    return flask.jsonify(results)
