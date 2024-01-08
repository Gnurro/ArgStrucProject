""" Utilities for survey preparation and analysis """

import json
import shutil

CORPUS_PATH = "corpus/en/"


def read_survey_texts_list(texts_list: str = "survey/texts_for_survey.txt") -> list:
    """
    Imports the survey text list.
    :param texts_list: Path to the txt list.
    :return: List of corpus text IDs.
    """
    with open(texts_list, 'r', encoding='utf-8') as txt_list_file:
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


def survey_texts_original_central(text_database: dict) -> dict:
    """
    Gets the original central unit first/last position based on a txt with a text ID per line.
    :param text_database: Dict database of extracted corpus information.
    :return: Dict {text ID:first/last}.
    """
    texts_list: list = read_survey_texts_list()
    original_central: dict = dict()
    for txt_id in texts_list:
        if text_database[txt_id]['central_adu'][1] == "1":
            original_central[txt_id] = "first"
        else:
            original_central[txt_id] = "last"
    return original_central


if __name__ == "__main__":
    """
    # load database:
    with open("extracted_db.json", 'r', encoding='utf-8') as db_file:
        database: dict = json.load(db_file)

    survey_texts_original_central(database)
    """
    # copy_original_texts()
    copy_edited_texts()
