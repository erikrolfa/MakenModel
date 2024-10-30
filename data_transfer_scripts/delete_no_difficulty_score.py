# pylint: disable=C0114
# pylint: disable=C0103
# pylint: disable=W0401
# pylint: disable=W0614

import pathlib
import sqlite3

def get_db():
    """Open a new database connection."""
    root_folder = pathlib.Path(__file__).resolve().parent.parent
    DATABASE_FILENAME = root_folder / "var" / "makenmodel.sqlite3"
    connection = sqlite3.connect(str(DATABASE_FILENAME))
    connection.row_factory = dict_factory
    connection.execute("PRAGMA foreign_keys = ON")
    return connection

def dict_factory(cursor, row):
    """Convert database row objects to a dictionary keyed on column name.

    This is useful for building dictionaries which are then used to render a
    template.  Note that this would be inefficient for large queries.
    """
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}


def delete_stuff():
    connection = get_db()

    connection.execute(
        "DELETE FROM instructions WHERE difficulty_score IS NULL"
    )

    connection.commit()

    if connection is not None:
        connection.close()

if __name__ == "__main__":
    delete_stuff()