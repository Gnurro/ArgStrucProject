""" Utilities for survey preparation and analysis """

import json
import shutil

CORPUS_PATH = "corpus/en/"


def read_survey_texts_list(texts_list_file: str = "survey/texts_for_survey.txt") -> list:
    """
    Imports the survey text list.
    :param texts_list_file: Path to the txt list.
    :return: List of corpus text IDs.
    """
    with open(texts_list_file, 'r', encoding='utf-8') as txt_list_file:
        txt_list: list = txt_list_file.read().strip().split("\n")
    return txt_list


def copy_original_texts(original_target_dir: str = "survey/original/"):
    """
    Copy the original texts from the corpus directory to the survey directory.
    :param original_target_dir: Target directory to copy to.
    :return: None, copies files on disk.
    """
    texts_list: list = read_survey_texts_list()
    for txt_id in texts_list:
        shutil.copy(f"{CORPUS_PATH}micro_{txt_id}.txt", original_target_dir)


def copy_edited_texts(edited_target_dir: str = "survey/edited/"):
    """
    Copy the editing files from the editing directory to the survey directory.
    :param edited_target_dir: Target directory to copy to.
    :return: None, copies files on disk.
    """
    texts_list: list = read_survey_texts_list()
    second_batch: bool = False
    for txt_id in texts_list:
        if txt_id == "b050":
            second_batch = True
        if not second_batch:
            shutil.copy(f"editing/JJ/{txt_id}.txt", edited_target_dir)
        else:
            shutil.copy(f"editing/MS/{txt_id}.txt", edited_target_dir)


def survey_texts_info(text_database: dict, texts_list_file: str = "survey/texts_for_survey.txt") -> dict:
    """
    Get various information about the survey texts.
    :param text_database: Dict database of extracted corpus information.
    :return: Dict {text ID:info}.
    """
    texts_list: list = read_survey_texts_list(texts_list_file)
    texts_info: dict = dict()

    for txt_id in texts_list:
        text_info: dict = dict()
        db_info = text_database[txt_id]
        # original first/last central:
        if db_info['central_adu'][1] == "1":
            text_info['original_central'] = "first"
        else:
            text_info['original_central'] = "last"
        # topic:
        text_info['topic'] = db_info['topic']
        # stance:
        text_info['stance'] = db_info['stance']

        texts_info[txt_id] = text_info

    return texts_info


def survey_texts_frequencies(text_database: dict, texts_list_file: str = "survey/texts_for_survey.txt") -> dict:
    """
    Get frequencies of text attributes for the survey texts.
    :param text_database: Dict database of extracted corpus information.
    :return: Dict with frequencies.
    """
    survey_info = survey_texts_info(text_database, texts_list_file)

    survey_freqs: dict = {
        'total_count': len(survey_info),
        'original_central': {'first': 0, 'last': 0},
        'topic': {},
        'stance': {'pro': 0, 'con': 0, 'unknown': 0}
    }

    for txt_info in survey_info.values():
        # original central:
        survey_freqs['original_central'][txt_info['original_central']] += 1
        # stance:
        survey_freqs['stance'][txt_info['stance']] += 1
        # topics
        if txt_info['topic'] not in survey_freqs['topic']:
            survey_freqs['topic'][txt_info['topic']] = 1
        else:
            survey_freqs['topic'][txt_info['topic']] += 1

    return survey_freqs


def get_original_first(text_database: dict, texts_list_file: str = "survey/texts_for_survey.txt") -> list:
    """
    Get a list of originally central-first text IDs in the edited survey texts.
    :param text_database:
    :param texts_list_file:
    :return:
    """
    texts_info: dict = survey_texts_info(text_database, texts_list_file)

    first_text_ids: list = list()

    for txt_id, txt_info in texts_info.items():
        if txt_info['original_central'] == "first":
            first_text_ids.append(txt_id)

    return first_text_ids


def build_survey_pairs(text_database: dict, texts_list_file: str = "survey/texts_for_survey.txt") -> dict:
    """
    Create database of original and edited texts for survey.
    :return: Dict {txtID:pair}
    """
    texts_info: dict = survey_texts_info(text_database, texts_list_file)

    pairs_db: dict = dict()

    for txt_id, txt_info in texts_info.items():
        # load original text:
        with open(f"survey/original/micro_{txt_id}.txt", 'r', encoding='utf-8') as og_file:
            original_text: str = og_file.read()

        # load edited text:
        with open(f"survey/edited/{txt_id}.txt", 'r', encoding='utf-8') as edit_file:
            edited_text: str = edit_file.read()

        pair_dict: dict = dict()

        if txt_info['original_central'] == "last":
            pair_dict['claim_last'] = original_text
            pair_dict['claim_first'] = edited_text
        else:
            pair_dict['claim_last'] = edited_text
            pair_dict['claim_first'] = original_text

        pairs_db[txt_id] = pair_dict

    return pairs_db


def pairs_to_csv(text_database: dict, texts_list_file: str = "survey/texts_for_survey.txt",
                 separator: str = "\t", csv_file_name: str = "pairs"):
    """
    Create CSV file with survey text pairs.
    :param text_database:
    :param texts_list_file:
    :return:
    """
    pairs_db: dict = build_survey_pairs(text_database, texts_list_file)

    if separator in [",", ";", "\n"]:
        print(f"Given separator '{separator}' can not be used. Tabulator character will be used instead.")
        separator = "\t"

    out_list: list = list()

    for txt_id, pair in pairs_db.items():
        out_row: str = f"{txt_id}{separator}{pair['claim_last']}{separator}{pair['claim_first']}"
        out_list.append(out_row)

    out_string: str = "\n".join(out_list)

    with open(f"survey/{csv_file_name}.csv", 'w', encoding='utf-8') as csv_file:
        csv_file.write(out_string)


def pairs_to_simple_list(text_database: dict, texts_list_file: str = "survey/texts_for_survey.txt",
                        out_list_file_name: str = "pairs"):
    """
    Create simple text file with survey text pairs.
    :param text_database:
    :param texts_list_file:
    :param out_list_file_name:
    :return:
    """
    pairs_db: dict = build_survey_pairs(text_database, texts_list_file)

    out_list: list = list()

    for txt_id, pair in pairs_db.items():
        out_row: str = f"{txt_id}\n{pair['claim_last']}\n{pair['claim_first']}\n---"
        out_list.append(out_row)

    out_string: str = "\n".join(out_list)

    with open(f"survey/{out_list_file_name}.txt", 'w', encoding='utf-8') as out_list_file:
        out_list_file.write(out_string)


if __name__ == "__main__":
    # copy_original_texts()
    # copy_edited_texts()

    picked = read_survey_texts_list("survey/picked_first_ogs.txt")
    print(picked)

    """
    # load database:
    with open("extracted_db.json", 'r', encoding='utf-8') as db_file:
        database: dict = json.load(db_file)
    """
    # survey_info = survey_texts_info(database)
    # print(survey_info)

    # survey_central_first = get_original_first(database)
    # print(survey_central_first)

    # survey_freqs = survey_texts_frequencies(database)
    # print(survey_freqs)

    # survey_pairs = build_survey_pairs(database)
    # print(survey_pairs)

    # pairs_to_csv(database)
    # pairs_to_simple_list(database)
