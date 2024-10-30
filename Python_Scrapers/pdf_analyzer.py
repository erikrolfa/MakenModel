# pylint: disable=C0114
# pylint: disable=C0103
# pylint: disable=W0401
#pylint: disable=W0614

import os
import json
import pathlib
import sqlite3
from classifier_paint_part import *
from text_preprocessor import *
from database_transfer import *
from classifier_difficulty import *

EXTRACTED_JSON_FOLDER = "json_extracted/"

def retrieve_json(file_path):
    """Retrieve JSON from files."""
    with open(file_path, "r", encoding="iso-8859-1") as file:
        try:
            json_file = json.load(file)
        except json.JSONDecodeError as e:
            print(f"Error retrieving JSON: {file_path}")
            print(f'Error Description {e}')
            return None
        return json_file

def get_info_from_json(json_pages):
    """Retrieve translated languages from JSON"""
    languages = set()
    num_pages = json_pages[-1]["pageNumber"]
    for pages in json_pages:
        if "detectedLanguages" in pages.keys():
            detected_langs = pages["detectedLanguages"]
            for lang in detected_langs:
                lang_code = lang["languageCode"]
                if lang_code != "en":
                    languages.add(lang_code)
    return languages, num_pages

def unlabeled_csv_to_score():
    label_data = {}
    with open("data/result.csv", 'r') as f:
        f.readline()
        content = f.readlines()
        for line in content:
            vals = line.strip().split(",")
            # print(vals)
            id = vals[0][:-2]
            label = vals[1]
            threshold_score = 0
            if label == 'easy':
                threshold_score = 0.3
            elif label == 'medium':
                threshold_score = 0.6
            else:
                threshold_score = 0.9
            label_data[id] = threshold_score
    return label_data

def main():
    """Analyze extracted PDF text"""
    instruction_texts = {}

    # Build scale:score dictionary
    scale_scores = get_scale_score_dict()

    # Set original max/min difficulty scores
    max_diff_score = -999
    min_diff_score = 999

    # Create pdf:difficulty dictionary
    diff_scores = {}

    id_score = unlabeled_csv_to_score()
    # print(id_score)

    folder_path = os.path.join(EXTRACTED_JSON_FOLDER, "unlabeled")
    json_directory = os.listdir(EXTRACTED_JSON_FOLDER)
    json_directory = os.listdir(folder_path)
    score_list = []
    for path in json_directory:
        clasy = {}
        json_path = os.path.join(folder_path, path)
        json_data = retrieve_json(json_path)
        if json_data:
            # print(json_path)
            json_path2 = json_path[:-5]
            json_text = json_data["text"]
            text_langs, num_pages = get_info_from_json(json_data["pages"])
            paint_set, non_unique_paint_counter, item_parts, cleaned_list = get_parts_and_paints_from_instructions(json_text)
            # NOTE: paint_set = set of paints used in model
            # NOTE: non_unique_paint_counter = number of paints NOT UNIQUE
            # NOTE: item_parts = [set of all parts in instructions ] UNDERESTIMATE
            # NOTE: cleaned_list = [array of tokens of json_text without model_parts and paints ] NOT CLEANED
            # EXAMPLE: ['this', 'is', 'an', 'example']


            # TBR
            processed_text = get_en_text(cleaned_list, text_langs)
            # TBR

            '''
            nb_score = ""
            json_path2 = json_path[:-5]
            clasy[json_path] = {}
            clasy[json_path]["text"] = processed_text
            nb_score = testNaiveBayes2(processed_text, class_prob, tf, vocab_size, totalwords)
            nb_score = testNaiveBayes(clasy[json_path], out1, out2, out3, totalwords)
            print(nb_score)
            if nb_score == 'easy':
                threshold_score = 0.3
            elif nb_score == 'medium':
                threshold_score = 0.6
            else:
                threshold_score = 0.9
            '''

            path2 = path[:-5]
            # Get difficulty score
            curr_scale_score = scale_scores[remove_exact_suffix(path2)]
            curr_diff_score = calculate_diff_score(item_parts, non_unique_paint_counter,num_pages, curr_scale_score, id_score[remove_exact_suffix(path2)])
            # print("DEBUG:", curr_diff_score)
            score_list.append(curr_diff_score)
            # if curr_diff_score > max_diff_score:
            #     max_diff_score = curr_diff_score
            # if curr_diff_score < min_diff_score:
            #     min_diff_score = curr_diff_score

            # Add raw difficulty score to dictionary
            diff_scores[remove_exact_suffix(path2)] = curr_diff_score
            # id_score.append((json_path,threshold_score))
            # break
    min_diff_score = min(score_list)
    max_diff_score = max(score_list)
    for pdf in diff_scores.keys():
        diff_scores[pdf] = (diff_scores[pdf] - min_diff_score) / (max_diff_score - min_diff_score)

    filename = "id_score.txt"
    with open(filename, 'w') as f:
        for id_score in diff_scores:
            print(f"{id_score} {diff_scores[id_score]}\n")
    # NOTE: This maps a unique_instruction_identifier to a unique_paint_identifer for all paints a model requires
    # transfer_instruction_to_paint_database(path, paint_set)
    return None

if __name__ == "__main__":
    main()
