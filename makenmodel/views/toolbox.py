"""
MakenModel toolbox view

URLS include:
/toolbox
"""

import flask
import makenmodel

@makenmodel.app.route('/toolbox/overview/')
def show_toolbox():
    '''Renders the toolbox overview view'''

    logname = flask.session['username']

    connection = makenmodel.model.get_db()

    context = {}

    context['logname'] = logname
    context['active_page'] = 'overview'

    cur = connection.execute(
        "SELECT COUNT(*) AS paint_count "
        "FROM user_paints "
        "WHERE username = ?",
        (logname,)
    )
    paint_count = cur.fetchone()['paint_count']

    if paint_count:
        context['num_paints'] = paint_count
    else:
        context['num_paints'] = 0


    cur = connection.execute(
        "SELECT COUNT(*) AS brand_count "
        "FROM user_brands "
        "WHERE username = ?",
        (logname,)
    )
    brand_count = cur.fetchone()['brand_count']

    if brand_count:
        context['num_brands'] = brand_count
    else:
        context['num_brands'] = 0

    cur = connection.execute(
        "SELECT p.paint_code, p.paint_name, p.brand, p.paint_type "
        "FROM paints p "
        "JOIN user_paints up ON p.unique_paint_identifier = up.unique_paint_identifier "
        "WHERE up.username = ? AND up.need_restock = 1",
        (logname,)
    )

    paints_needing_restock = cur.fetchall()

    context['paints_needing_restock'] = paints_needing_restock

    cur = connection.execute(
        "SELECT MAX(paint_count) as max_paint_count FROM ("
        "SELECT COUNT(up.unique_paint_identifier) as paint_count "
        "FROM user_paints up "
        "JOIN paints p ON up.unique_paint_identifier = p.unique_paint_identifier "
        "WHERE up.username = ? "
        "GROUP BY p.brand) as brand_counts",
        (logname,)
    )
    max_paint_count_row = cur.fetchone()
    max_paint_count = max_paint_count_row['max_paint_count'] if max_paint_count_row else 0

    # If there's at least one paint, identify all brands with this maximum count
    if max_paint_count and max_paint_count > 0:
        cur = connection.execute(
            "SELECT p.brand, COUNT(up.unique_paint_identifier) AS paint_count "
            "FROM user_paints up "
            "JOIN paints p ON up.unique_paint_identifier = p.unique_paint_identifier "
            "WHERE up.username = ? "
            "GROUP BY p.brand "
            "HAVING paint_count = ?",
            (logname, max_paint_count)
        )
        favorite_brands_with_counts = cur.fetchall()
        context['favorite_brands'] = [
            {'brand': row['brand'], 'paint_count': row['paint_count']}
            for row in favorite_brands_with_counts
        ]
    else:
        context['favorite_brands'] = []

    return flask.render_template('toolbox.html', **context)


@makenmodel.app.route('/toolbox/add-paints/')
def show_add_paints():
    '''Shows the tab where users add paints to their collection'''

    logname = flask.session['username']

    context = {}

    context['logname'] = logname

    return flask.render_template('add_paints.html', **context)

@makenmodel.app.route('/toolbox/your-paints')
def show_your_paints():
    '''Shows the paints the user has in their collection'''

    connection = makenmodel.model.get_db()

    logname = flask.session['username']

    context = {}

    context['logname'] = logname

    cur = connection.execute(
        "SELECT p.*, up.need_restock, up.unique_paint_identifier FROM user_paints up "
        "JOIN paints p ON up.unique_paint_identifier = p.unique_paint_identifier "
        "WHERE up.username = ?",
        (logname,)
    )
    paint_details = cur.fetchall()
    context['paint_details'] = paint_details

    return flask.render_template('your_paints.html', **context)


@makenmodel.app.route('/toolbox/add-paints/', methods=['POST'])
def add_paints():
    '''Route to add paint to database'''
    context = {}

    connection = makenmodel.model.get_db()

    logname = flask.session['username']
    context['logname'] = logname

    brand = flask.request.form['brand']
    paint_info = flask.request.form['paint']

    context['brand'] = brand

    # print(paint_info)
    paint_info = paint_info.split(' ')

    print('ball', paint_info)

    paint_code = paint_info[0]


    paint_type = paint_info[-1]

    paint_info.pop(0)
    paint_info.pop(-1)
    # paint_info.clear()

    paint_name = ' '.join(paint_info)
    # slice off the ()
    paint_code = paint_code[1:-1]

    # slice off the ()
    paint_type = paint_type[1:-1]

    print('ball', paint_code, paint_name, paint_type, brand)

    if paint_type != 'null':
        cur = connection.execute(
            "SELECT unique_paint_identifier FROM paints "
            "WHERE brand = ? AND paint_code = ? AND paint_name = ? AND paint_type = ?",
            (brand, paint_code, paint_name, paint_type)
        )
    else:
        cur = connection.execute(
            "SELECT unique_paint_identifier FROM paints "
            "WHERE brand = ? AND paint_code = ? AND paint_name = ?",
            (brand, paint_code, paint_name)
        )

    identifier = cur.fetchone()['unique_paint_identifier']

    cur = connection.execute(
        "SELECT * FROM user_paints "
        "WHERE username = ? AND unique_paint_identifier = ?",
        (logname, identifier)
    )
    exists = cur.fetchone()

    if exists:
        context['repeat_color'] = "This paint is already in your collection!"

    # Inserting username and identifier into db
    connection.execute(
        "INSERT OR IGNORE INTO user_paints (username, unique_paint_identifier, need_restock) "
        "VALUES (?, ?, ?)",
        (logname, identifier, False)
    )
    connection.commit()

    if not exists:
        context['success_message'] = 'Paint added to your collection!'

    cur = connection.execute(
        "SELECT unique_brand_identifier FROM brands "
        "WHERE brand = ?",
        (brand,)
    )

    brand_identifier = cur.fetchone()['unique_brand_identifier']

    connection.execute(
        "INSERT OR IGNORE INTO user_brands (username, unique_brand_identifier) "
        "VALUES (?, ?)",
        (logname, brand_identifier)
    )

    connection.commit()

    return flask.render_template('add_paints.html', **context)



@makenmodel.app.route('/toolbox/getting_low', methods=['POST'])
def mark_getting_low():
    '''Updates getting low status for user paints'''
    data = flask.request.json

    connection = makenmodel.model.get_db()

    logname = flask.session['username']

    unique_paint_identifier = data.get('id')
    getting_low_status = data.get('getting_low')

    connection.execute(
        "UPDATE user_paints SET need_restock = ? "
        "WHERE unique_paint_identifier = ? AND username = ?",
        (getting_low_status, unique_paint_identifier, logname)
    )

    connection.commit()

    return flask.redirect(flask.url_for('show_your_paints'))

@makenmodel.app.route('/toolbox/remove_from_getting_low', methods=['POST'])
def remove_from_getting_low():
    '''Removes a paint from getting low'''

    connection = makenmodel.model.get_db()

    logname = flask.session['username']

    data = flask.request.json

    paint_brand = data.get('paint-brand')
    paint_code = data.get('paint-code')
    getting_low_status = 0

    cur = connection.execute(
        "SELECT unique_paint_identifier "
        "FROM paints WHERE brand = ? AND paint_code = ?",
        (paint_brand, paint_code)
    )

    unique_paint_identifier = cur.fetchone()['unique_paint_identifier']

    connection.execute(
        "UPDATE user_paints SET need_restock = ? "
        "WHERE unique_paint_identifier = ? AND username = ?",
        (getting_low_status, unique_paint_identifier, logname)
    )

    connection.commit()

    return flask.redirect(flask.url_for('show_toolbox'))




@makenmodel.app.route('/toolbox/getting_low/', methods=['GET'])
def show_getting_low():
    '''Shows the user what paints are getting low'''
    connection = makenmodel.model.get_db()

    logname = flask.session['username']

    context = {}

    context['logname'] = logname

    cur = connection.execute(
        "SELECT p.paint_code, p.paint_name, p.brand, p.paint_type "
        "FROM paints p "
        "JOIN user_paints up ON p.unique_paint_identifier = up.unique_paint_identifier "
        "WHERE up.username = ? AND up.need_restock = 1",
        (logname,)
    )

    paints_needing_restock = cur.fetchall()

    context['need_restock'] = paints_needing_restock

    return flask.render_template('getting_low.html', **context)