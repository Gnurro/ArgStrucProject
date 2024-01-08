""" Utilities for microtext editing """

import json
from unit_checking import get_central_first_texts, get_central_last_texts


def editable_text(text_content):
    text_units = text_content['units']
    units_list = [f"{text_unit['edu_id']} {text_unit['adu_stance']} {text_unit['text']}" for text_unit in text_units]
    out_text = "\n".join(units_list)

    return out_text


def create_editing_files(text_database, sub_dir: str):
    """
    Creates text files ready for editing from the passed text database in the passed subdirectory.
    :param text_database: Dict database with texts and extracted information.
    :param sub_dir: Subdirectory to save created files to.
    :return: None, files written to disk.
    """
    dir_path = f"editing/{sub_dir}/"
    for text_id, content in text_database.items():
        with open(f"{dir_path}{text_id}.txt", 'w', encoding='utf-8') as out_file:
            out_file.write(f"Central claim unit: {content['central_adu']}\nOriginal order:\n")
            out_file.write(editable_text(content))


if __name__ == "__main__":
    # load database:
    with open("extracted_db.json", 'r', encoding='utf-8') as db_file:
        database: dict = json.load(db_file)
    
    # edit_test = editable_text(database['b001'])
    # print(edit_test)
    """
    create_editing_files(get_central_first_texts(database), "JJ")
    create_editing_files(get_central_last_texts(database), "JJ")
    """

