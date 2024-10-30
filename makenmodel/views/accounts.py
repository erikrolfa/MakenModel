"""
MakenModel login view

URLS include:
/accounts/login
/accounts/create_account

"""

import flask
import makenmodel
import hashlib
import uuid
import pathlib
import os
from werkzeug.utils import secure_filename



@makenmodel.app.route('/accounts/login/')
def show_login():
    '''Shows login page'''
    context = {}

    return flask.render_template('login.html', **context)


@makenmodel.app.route('/accounts/create-account/')
def show_create_account():
    '''Shows create account page'''
    context = {}

    return flask.render_template('create_account.html', **context)

@makenmodel.app.route('/accounts/logout/', methods=['POST'])
def logout():
    '''Logs user out'''
    if 'username' in flask.session:
        flask.session.pop('username', None)
    return flask.redirect(flask.url_for('show_index'))

@makenmodel.app.route('/accounts/login/', methods=['POST'])
def login():
    username = flask.request.form['username']
    submitted_password = flask.request.form['password']

    connection = makenmodel.model.get_db()

    cur = connection.execute(
        "SELECT password FROM users WHERE username = ?",
        (username,)
    )
    user_data = cur.fetchone()

    context = {}

    if user_data:

        stored_password = user_data['password']

        hash_algo, salt, stored_hash = stored_password.split('$')

        hasher = hashlib.new(hash_algo)

        hasher.update((salt + submitted_password).encode('utf-8'))

        hashed_password = hasher.hexdigest()

        if hashed_password == stored_hash:
            flask.session['username'] = username
            return flask.redirect(flask.url_for('show_index'))

        # If username is in database, but password is wrong
        context['wrong_password'] = 'Incorrect Password'

    # If username is not found in database
    else:
        context['wrong_username'] = 'Sorry, we can\'t find that username in our system'

    return flask.render_template('login.html', **context)


@makenmodel.app.route('/accounts/create-account/', methods=['POST'])
def create_account():
    '''This route accepts post requests and makes an account in the database'''

    connection = makenmodel.model.get_db()

    context = {}

    username = flask.request.form['username']
    email = flask.request.form['email']
    password = flask.request.form['password']

    # Checking if user provided a profile picture
    if 'profile_pic_filename' in flask.request.files:
        profile_pic_object = flask.request.files['profile_pic_filename']
        profile_pic_filename = profile_pic_object.filename
        context['profile_pic_filename'] = profile_pic_filename

    # TODO: remove this shit
    context['username'] = username
    context['password'] = password
    context['email'] = email

    cur = connection.execute(
        "SELECT COUNT(*) AS count FROM users WHERE username = ?",
        (username,)
    )
    count = cur.fetchone()['count']

    if count > 0:
        context['username_error'] = 'Sorry, that username has already been taken'

    cur = connection.execute(
        "SELECT COUNT(*) AS count FROM users WHERE email = ?",
        (email,)
    )
    count = cur.fetchone()['count']

    if count > 0:
         context['email_error'] = 'You already have an account associated with that email'

    # If there are no conflicting emails or usernames in input
    if 'username_error' not in context and 'email_error' not in context:

        # Encrypting password
        algorithm = 'sha512'
        salt = uuid.uuid4().hex
        hash_obj = hashlib.new(algorithm)
        password_salted = salt + password
        hash_obj.update(password_salted.encode('utf-8'))
        password_hash = hash_obj.hexdigest()
        password_db_string = '$'.join([algorithm, salt, password_hash])

        # Making profile_pic filename
        try:
            if profile_pic_filename:
                profile_pic_filename = secure_filename(profile_pic_object.filename)

                unique_filename = str(uuid.uuid4()) + pathlib.Path(profile_pic_filename).suffix

                upload_folder = makenmodel.app.config['UPLOAD_FOLDER']

                filepath = os.path.join(upload_folder, unique_filename)

                print('upload folder: ', upload_folder)
                print('filepath: ', filepath)

                profile_pic_object.save(filepath)

            else:
                # If a user doesn't input a profile picture
                unique_filename = 'default_profileasffaskf348728458234.jpg'
        except IOError as e:
            print(f"IOError: Failed to save file. Error: {e}")

        cur = connection.execute(
            "INSERT INTO users "
            "(username, password, email, profile_pic_filename) "
            "VALUES (?, ?, ?, ?)",
            (username, password_db_string, email, unique_filename)
        )

        connection.commit()
        print(password_db_string)
        flask.session['username'] = username

        return flask.redirect(flask.url_for('show_index'))

    # If there is a username or email conflict
    return flask.render_template('create_account.html', **context)
