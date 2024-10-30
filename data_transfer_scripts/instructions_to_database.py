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

def get_pdf_name(path):

    split_path = path.split('/')

    part = split_path[-1]

    split_part = part.split('.')

    name = split_part[0]

    return name

def transfer_instruction_data():

    instruction_path = "data/model_specs.output"

    connection = get_db()

    with open(instruction_path, 'r', encoding='utf-8') as specs:

        for line in specs:
            line = line.strip()

            parts = line.split('\t')

            if len(parts) == 4:

                base_link = "https://www.scalemates.com"

                model_page_link = base_link + parts[0]
                model_pdf_link = base_link + parts[1]
                model_name = parts[2]
                model_scale = parts[3]

                pdf_name = get_pdf_name(parts[1])


                connection.execute(
                    "INSERT INTO instructions (model_name, scale, model_page_link, model_pdf_link, pdf_name) "
                    "VALUES (?, ?, ?, ?, ?)",
                    (model_name, model_scale, model_page_link, model_pdf_link, pdf_name)
                )

                connection.commit()

    if connection is not None:
        connection.close()

if __name__ == "__main__":
    transfer_instruction_data()
