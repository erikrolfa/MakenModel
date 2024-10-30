'''Configuration file for project'''

import pathlib

APPLICATION_ROOT = '/'

SECRET_KEY = b'8\xef5f\xb1\xd1Pf]\xa6\x18G\xe3F\xaf7\x9e\x10\xbf\x12\xc5^\x81H'
SESSION_COOKIE_NAME = 'login'

MAKENMODEL_ROOT = pathlib.Path(__file__).resolve().parent.parent
UPLOAD_FOLDER = pathlib.Path('/var/uploads')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jped', 'gif', 'heic'])

MAX_CONTENT_LENGTH = 16 * 1024 * 1024

DATABASE_FILENAME = MAKENMODEL_ROOT/'var'/'makenmodel.sqlite3'
