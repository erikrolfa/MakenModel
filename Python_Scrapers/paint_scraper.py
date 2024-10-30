from bs4 import BeautifulSoup
import requests
import os
import json

# pylint: disable=C0103

# INPUT:
# page_url: url of an individual brands page (string)

# OUTPUT:
# brand: name of the paint brand (string)
# paint_list: contains a list of all paint details (list(list))
#             [[paint_code, paint_color, background_color, shine_type,
#               type_paint], ...]
def get_page_paints(page_url):
    """Get paints for an individual paints page."""

    page = requests.get(page_url)
    soup = BeautifulSoup(page.text, features='html.parser')

    brand = soup.find('h1')
    brand = brand.text
    divs = soup.find_all('div', class_='ac dg bgl cc pr mt4')

    paint_list = []
    avoid_dupes = set()

    for div in divs:
        style_attr = div.find('div', style=True)
        style_list = style_attr['style'].split(';') if style_attr else None

        background_color = None

        if style_list:
            for style in style_list:
                if style.startswith('background:'):
                    background_color = style.split(':')[-1]
                    break

        paint_code = div.find('span', class_='bgb nw')
        paint_code = paint_code.text if paint_code else None

        a_tags = div.find_all('a')

        paint_color = None

        for a_tag in a_tags:
            span = a_tag.find('span')
            if span:
                paint_color = ''.join(text for text in a_tag.stripped_strings if text != span.get_text(strip=True))

        shine_type = div.find('div', class_='ccf center dib nw bgn')
        type_paint = div.find('div', class_='cct center dib nw bgg')

        if not type_paint:
            type_paint = div.find('div', class_='cct center dib nw bgb')
        if not type_paint:
            type_paint = div.find('div', class_='cct center dib nw bgo')

        shine_type = shine_type.text if shine_type else None
        type_paint = type_paint.text if type_paint else None

        if paint_code and paint_color:
            # This is a group that makes sure we don't add same paint to data twice
            # gets rid of uppercase and spaces to make sure that these don't distinguish duplicates
            paint_code_style_gone = paint_code.lower().replace(' ', '')
            paint_color_style_gone = paint_color.lower().replace(' ', '')

            dupe_criteria = (paint_code_style_gone, paint_color_style_gone, shine_type, type_paint)

            if dupe_criteria not in avoid_dupes:
                data = [paint_code, paint_color, background_color, shine_type,
                        type_paint]
                paint_list.append(data)
                avoid_dupes.add(dupe_criteria)

    return brand, paint_list

def main():
    url = 'https://www.scalemates.com/colors/?ranges=all'
    base_url = 'https://www.scalemates.com'

    base_page = requests.get(url)
    base_soup = BeautifulSoup(base_page.text, features='html.parser')

    links = base_soup.find_all('a', class_='pf')
    pure_pf_links = [a for a in links if a.get('class') == ['pf']]

    url_list = []

    for link in pure_pf_links:
        href = link.get('href')
        full_url = base_url + href
        if full_url not in url_list:
            url_list.append(full_url)

    brands_to_paints = {}
    for url in url_list:
        brand, paint_list = get_page_paints(url)
        brands_to_paints[brand] = paint_list

    data_folder = 'scraping_data'
    output_filename = 'paint_scrape_data.json'
    output_path = os.path.join(data_folder, output_filename)

    # Clearing the output file if it is not empty
    if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
        open(output_path, 'w', encoding='utf-8').close()

    with open(output_path, 'w', encoding='utf-8') as output:
        json.dump(brands_to_paints, output, ensure_ascii=False)

    print(f'Final Output file size: {os.path.getsize(output_path)}\n')

if __name__ == "__main__":
    main()
