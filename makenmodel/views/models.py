"""
MakenModel find_models view

URLS include:

"""

import flask
import makenmodel


@makenmodel.app.route('/models/')
def show_find_models():
    logname = flask.session.get('username')


    context = {}

    context['logname'] = logname

    return flask.render_template('models.html', **context)


@makenmodel.app.route('/models/find/')
def find_model_identifiers_by_paint_availability():
    logname = flask.session.get('username')
    connection = makenmodel.model.get_db()

    cur = connection.execute(
        "SELECT unique_paint_identifier FROM user_paints "
        "WHERE username = ?",
        (logname,)
    )
    user_paints = [item['unique_paint_identifier'] for item in cur.fetchall()]

    model_identifiers_by_missing_count = {0: [], 1: [], 2: [], 3: [], 'more': []}

    missing_dict = {}

    if not user_paints:
        cur_more = connection.execute("""
            SELECT unique_instruction_identifier FROM instructions
            ORDER BY unique_instruction_identifier
            LIMIT 20
        """)
        model_identifiers_by_missing_count['more'] = [row['unique_instruction_identifier'] for row in cur_more.fetchall()]
    else:
        model_set = set()

        for paint_id in user_paints:
        # Fetch all instruction identifiers that use the paint
            cur = connection.execute(
                "SELECT unique_instruction_identifier FROM instructions_to_paints WHERE unique_paint_identifier = ?",
                (paint_id,)
            )
            # Add each instruction identifier to the set to ensure uniqueness
            paint_models = {item['unique_instruction_identifier'] for item in cur.fetchall()}
            model_set.update(paint_models)


        for model in model_set:
            missing_dict[model] = 0

        for model in missing_dict:
            cur = connection.execute(
                "SELECT unique_paint_identifier "
                "FROM instructions_to_paints "
                "WHERE unique_instruction_identifier = ?",
                (model,)
            )
            all_paints = [row['unique_paint_identifier'] for row in cur.fetchall()]

            for paint_id in all_paints:
                if paint_id not in user_paints:
                    missing_dict[model] = missing_dict.get(model, 0) + 1

    for model, num_missing in missing_dict.items():
        if num_missing == 0:
            model_identifiers_by_missing_count[0].append(model)
        if num_missing == 1:
            model_identifiers_by_missing_count[1].append(model)
        if num_missing == 2:
            model_identifiers_by_missing_count[2].append(model)
        if num_missing == 3:
            model_identifiers_by_missing_count[3].append(model)
        if num_missing > 3:
            model_identifiers_by_missing_count['more'].append(model)

    context = {'exact_match': [], 'missing_one': [], 'missing_two': [], 'missing_three': [], 'missing_more': []}

    context['logname'] = logname

    # Assuming model_identifiers_by_missing_count is a list or a dictionary with lists of model identifiers

    # Exact matches
    for model in model_identifiers_by_missing_count[0]:
        cur = connection.execute(
            "SELECT * FROM instructions "
            "WHERE unique_instruction_identifier = ?",
            (model,)
        )
        info = cur.fetchone()
        context['exact_match'].append(info)

    # Missing one paint
    for model in model_identifiers_by_missing_count[1]:
        cur = connection.execute(
            "SELECT * FROM instructions "
            "WHERE unique_instruction_identifier = ?",
            (model,)
        )
        info = cur.fetchone()
        context['missing_one'].append(info)

    # Missing two paints
    for model in model_identifiers_by_missing_count[2]:
        cur = connection.execute(
            "SELECT * FROM instructions "
            "WHERE unique_instruction_identifier = ?",
            (model,)
        )
        info = cur.fetchone()
        context['missing_two'].append(info)

    # Missing three paints
    for model in model_identifiers_by_missing_count[3]:
        cur = connection.execute(
            "SELECT * FROM instructions "
            "WHERE unique_instruction_identifier = ?",
            (model,)
        )
        info = cur.fetchone()
        context['missing_three'].append(info)  # Adjusted here from 'missing_two' to 'missing_three'

    # Missing more paints
    for model in model_identifiers_by_missing_count['more']:

        cur = connection.execute(
            "SELECT * FROM instructions "
            "WHERE unique_instruction_identifier = ?",
            (model,)
        )
        info = cur.fetchone()
        context['missing_more'].append(info)

    context['exact_match'] = sorted(context['exact_match'], key=lambda x: x['difficulty_score'])
    context['missing_one'] = sorted(context['missing_one'], key=lambda x: x['difficulty_score'])
    context['missing_two'] = sorted(context['missing_two'], key=lambda x: x['difficulty_score'])
    context['missing_three'] = sorted(context['missing_three'], key=lambda x: x['difficulty_score'])
    context['missing_more'] = sorted(context['missing_more'], key=lambda x: x['difficulty_score'])


    lower_threshold_items = [item for item in context['missing_more'] if item['difficulty_score'] <= 0.142]
    middle_threshold_items = [item for item in context['missing_more'] if 0.142 < item['difficulty_score'] < 0.177]
    higher_threshold_items = [item for item in context['missing_more'] if item['difficulty_score'] > 0.177]

    # Limit to top 5 from each category based on the difficulty score
    context['missing_more'] = (sorted(lower_threshold_items, key=lambda x: x['difficulty_score'])[:5] +
                            sorted(middle_threshold_items, key=lambda x: x['difficulty_score'])[:5] +
                            sorted(higher_threshold_items, key=lambda x: x['difficulty_score'])[:5])

    return flask.render_template('find_models.html', **context)