import sqlite3
import os
import re

def get_db():
    '''Connects to sqlite database'''
    db_folder = 'var'
    db_filename = 'makenmodel.sqlite3'

    db_filename = os.path.join(db_folder, db_filename)

    database = sqlite3.connect(str(db_filename))

    database.execute("PRAGMA foreign_keys = ON")

    return database

def remove_exact_suffix(filename):
    # Define the pattern to match 'instructions-0' and replace with 'instructions'
    pattern = r'(instructions)-0\b'
    new_filename = re.sub(pattern, r'\1', filename)
    if filename[-1] != 's':
        filename = filename[:-2]

    return new_filename

def get_pdf_name(path):

    split_path = path.split('/')

    part = split_path[-1]

    split_part = part.split('.')

    name = split_part[0]

    name = remove_exact_suffix(name)

    return name

def transfer_instruction_to_paint_database(path, paints, overwrite=False):

    pdf_name = get_pdf_name(path)

    if overwrite == True:

        with open('instruction_to_paint.txt', 'a', encoding='utf-8') as file:
            file.write(f'{pdf_name}\t{paints}\n')

    connection = get_db()

    cur = connection.execute(
        "SELECT unique_instruction_identifier FROM instructions "
        "WHERE pdf_name = ?",
        (pdf_name,)
    )
    instruction_identifier = cur.fetchone()[0]

    for paint in paints:

        cur = connection.execute(
            "SELECT unique_paint_identifier FROM paints "
            "WHERE paint_code = ?",
            (paint,)
        )

        paint_identifier = cur.fetchone()[0]

        connection.execute(
            "INSERT OR IGNORE INTO instructions_to_paints (unique_instruction_identifier, unique_paint_identifier) "
            "VALUES (?, ?)",
            (instruction_identifier, paint_identifier)
        )
        connection.commit()

    if connection is not None:
        connection.close()
