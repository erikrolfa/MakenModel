# NEED:
# parts / page
# paints / parts

# HAVE:
# scale score
from database_transfer import *

def build_scores(id, parts, num_paints, num_pages, nb_score):
    """Iterate through all pdfs in this function?"""
    diff_scores = {}
    scale_scores = get_scale_score_dict()
    max_score = -999
    min_score = 999
    for pdf in pdfs:
        diff_score = calculate_diff_score(pdf['parts'], pdf['num_paints'], pdf['num_pages'],
                                          scale_scores[pdf['link']], pdf['nb_score'])
        diff_scores[pdf['link']] = diff_score
        if diff_score > max_score:
            max_score = diff_score
        if diff_score < min_score:
            min_score = diff_score
    for pdf in diff_scores.keys():
        diff_scores[pdf] = (diff_scores[pdf] - min_score) / (max_score - min_score)

    # Now transfer dict to database somehow



def calculate_diff_score(parts, num_paints, num_pages, scale_score, naive_bayes_score):
    params = [0.3, 0.3, 0.4]
    num_parts = len(parts)
    if not num_pages > 0:
        parts_per_page = 0
    else:
        parts_per_page = len(parts) / num_pages
    if not num_parts > 0:
        paints_per_part = 0
    else:
        paints_per_part = num_paints / num_parts
    num_parts = num_parts
    diff_score = params[0] * paints_per_part + params[1] * (parts_per_page * scale_score) + params[2] * naive_bayes_score

    return diff_score

def get_scale_score(scale):
    ratings = {}
    with open('data/scale_ratings.txt', 'r', encoding='utf-8') as fin:
        for line in fin.readlines():
            line = line.split()
            ratings[line[0]] = float(line[1])
    known_scales = ratings.keys()
    # If model scale is not in our list, find the closest existing scale
    if ':' in scale:
        if scale not in ratings.keys() and scale.split(':')[1].isdigit():
            scale_denom = int(scale.split(':')[1])
            closest_scale_key = ''
            closest_scale_val = 999

            for key in known_scales:
                curr_diff = abs(scale_denom - int(key.split(':')[1]))
                if curr_diff < closest_scale_val:
                    closest_scale_key = key
                    closest_scale_val = curr_diff
            scale = closest_scale_key

    return ratings.get(scale, 0.5)

def get_scale_score_dict():
    model_ratings = {}
    with open("data/model_specs.output", 'r', encoding='utf-8') as specs:
        for line in specs.readlines():
            line = line.split('\t')
            pdf = line[1]
            pdf = get_pdf_name(pdf)
            curr_score = get_scale_score(line[3].strip())
            model_ratings[pdf] = curr_score
    return model_ratings