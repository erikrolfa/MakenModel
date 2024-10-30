'''These are functions that transfer the scraped data to the database'''
import os
import sys
import sqlite3
import json


# pylint: disable=C0103

data_folder = 'scraping_data'

def get_db():
    '''Connects to sqlite database'''
    db_folder = 'var'
    db_filename = 'makenmodel.sqlite3'

    db_filename = os.path.join(db_folder, db_filename)

    database = sqlite3.connect(str(db_filename))

    database.execute("PRAGMA foreign_keys = ON")

    return database


def transfer_paint_data():
    '''Transfers scraped paint info to database'''

    connection = get_db()

    paint_filename = 'paint_scrape_data.json'

    paint_path = os.path.join(data_folder, paint_filename)

    with open(paint_path, 'r', encoding='utf-8') as data:
        paint_data = json.load(data)


    cursor = connection.cursor()

    for brand in paint_data.keys():
        cursor.execute("INSERT OR IGNORE INTO brands (brand) VALUES (?)", (brand,))

    tamiya_list = ["Tamiya", "Tamiya Color Lacquer Paint", "Tamiya Paint Markers", "Tamiya Polycarb Marker"]

    for brand, paints in paint_data.items():
        for paint in paints:
            paint_code, paint_name, background_color, shine_type, paint_type = paint
            paint_code = paint_code.replace('-', '')
            cursor.execute(
                "INSERT INTO paints(brand, paint_name, paint_code, background_color, shine_type, paint_type) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (brand, paint_name, paint_code, background_color, shine_type, paint_type)
                )

    connection.commit()


    if connection is not None:
        connection.close()


def main():

    transfer_paint_data()


if __name__ == '__main__':
    main()
