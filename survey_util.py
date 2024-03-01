""" Utilities for survey preparation and analysis """

import json
import shutil
import pandas

CORPUS_PATH = "corpus/en/"


def read_texts_list(texts_list_file: str = "survey/texts_for_survey.txt") -> list:
    """
    Imports a txt corpus text ID list.
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
    texts_list: list = read_texts_list()
    for txt_id in texts_list:
        shutil.copy(f"{CORPUS_PATH}micro_{txt_id}.txt", original_target_dir)


def copy_edited_texts(edited_target_dir: str = "survey/edited/", cutoff_text_id: str = "b050",
                      first_annotator_tag: str = "JJ", second_annotator_tag: str = "MS"):
    """
    Copy the editing files from the editing directory to the survey directory. Loads edited texts from to different
    annotator/editor batches based on a cutoff corpus text ID.
    :param edited_target_dir: Target directory to copy to.
    :param cutoff_text_id: First corpus text ID of the second annotator's batch of edited texts.
    :param first_annotator_tag: Tag of the first batch annotator and name of directory containing their edited texts.
    :param second_annotator_tag: Tag of the second batch annotator and name of directory containing their edited texts.
    :return: None, copies files on disk.
    """
    texts_list: list = read_texts_list()
    second_batch: bool = False
    for txt_id in texts_list:
        if txt_id == cutoff_text_id:
            second_batch = True
        if not second_batch:
            shutil.copy(f"editing/{first_annotator_tag}/{txt_id}.txt", edited_target_dir)
        else:
            shutil.copy(f"editing/{second_annotator_tag}/{txt_id}.txt", edited_target_dir)


def survey_texts_info(text_database: dict, texts_list_file: str = "survey/texts_for_survey.txt") -> dict:
    """
    Get various information about the survey texts.
    :param text_database: Dict database of extracted corpus information.
    :param texts_list_file: Path of the txt list file with all texts edited for the survey.
    :return: Dict {text ID:info}.
    """
    texts_list: list = read_texts_list(texts_list_file)
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
    :param texts_list_file: Path of the txt list file with all texts edited for the survey.
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
    :param text_database: Dict database of extracted corpus information.
    :param texts_list_file: Path of the txt list file with all texts edited for the survey.
    :return:
    """
    texts_info: dict = survey_texts_info(text_database, texts_list_file)

    first_text_ids: list = list()

    for txt_id, txt_info in texts_info.items():
        if txt_info['original_central'] == "first":
            first_text_ids.append(txt_id)

    return first_text_ids


def get_original_last(text_database: dict, texts_list_file: str = "survey/texts_for_survey.txt") -> list:
    """
    Get a list of originally central-last text IDs in the edited survey texts.
    :param text_database: Dict database of extracted corpus information.
    :param texts_list_file: Path of the txt list file with all edited texts edited for the survey.
    :return:
    """
    texts_info: dict = survey_texts_info(text_database, texts_list_file)

    last_text_ids: list = list()

    for txt_id, txt_info in texts_info.items():
        if txt_info['original_central'] == "last":
            last_text_ids.append(txt_id)

    return last_text_ids


def create_balanced_text_list(text_database: dict, texts_list_file: str = "survey/texts_for_survey.txt",
                              selected_og_first_file: str = "survey/picked_first_ogs.txt",
                              final_list_file_name: str = "final_texts_list") -> list:
    """
    Create a list of corpus text IDs that is balanced between originally claim-first and originally claim-last texts,
    and save it as a txt list. Since there are more originally claim-first texts in the edited texts, a manual
    selection of them is defined in a separate list txt file which is loaded to build the final list of texts to be
    used in the survey.
    :param text_database: Dict database of extracted corpus information.
    :param texts_list_file: Path of the txt list file with all texts edited for the survey.
    :param selected_og_first_file: Path of the txt list file with selected originally claim-first texts edited for the
    survey.
    :param final_list_file_name: Name for the final texts list txt file.
    :return: Balanced list of text IDs.
    """
    # get the IDs of the originally central-last texts:
    survey_central_last = get_original_last(text_database, texts_list_file)
    central_last_count = len(survey_central_last)
    # get the list of selected originally claim-first texts:
    picked = read_texts_list(selected_og_first_file)
    central_first_count = len(picked)
    # check that there are the same number of texts each:
    assert central_last_count == central_first_count, (f"Imbalanced number of original central positions! "
                                                       f"{central_last_count} central-last and "
                                                       f"{central_first_count} central-first texts.")
    # combine and sort balanced texts:
    balanced_texts = survey_central_last + picked
    balanced_texts = sorted(balanced_texts)
    # convert to newline-separated string list:
    balanced_list_str = "\n".join(balanced_texts)
    # save to disk:
    with open(f"survey/{final_list_file_name}.txt", 'w', encoding='utf-8') as out_list_file:
        out_list_file.write(balanced_list_str)

    return balanced_texts


def build_survey_pairs(text_database: dict, texts_list_file: str = "survey/texts_for_survey.txt") -> dict:
    """
    Create database of original and edited texts for survey.
    :param text_database: Dict database of extracted corpus information.
    :param texts_list_file: Path of the txt list file with selected texts edited for the survey.
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


def survey_processing_pairs(text_database: dict, texts_list_file: str = "survey/texts_for_survey.txt") -> dict:
    """
    Create database of original and edited texts for survey.
    :param text_database: Dict database of extracted corpus information.
    :param texts_list_file: Path of the txt list file with selected texts edited for the survey.
    :return: Dict {txtID:pair}
    """
    texts_info: dict = survey_texts_info(text_database, texts_list_file)

    pairs_db: dict = dict()

    form_text_number: int = 1

    for txt_id, txt_info in texts_info.items():
        # load original text:
        with open(f"survey/original/micro_{txt_id}.txt", 'r', encoding='utf-8') as og_file:
            original_text: str = og_file.read()

        # load edited text:
        with open(f"survey/edited/{txt_id}.txt", 'r', encoding='utf-8') as edit_file:
            edited_text: str = edit_file.read()

        pair_dict: dict = dict()

        pair_dict['form_text_id'] = f"Text {form_text_number}"

        if txt_info['original_central'] == "last":
            pair_dict['claim_last'] = {'text': original_text, 'edited': False}
            pair_dict['claim_first'] = {'text': edited_text, 'edited': True}
        else:
            pair_dict['claim_last'] = {'text': edited_text, 'edited': True}
            pair_dict['claim_first'] = {'text': original_text, 'edited': False}

        pairs_db[txt_id] = pair_dict
        form_text_number += 1

    return pairs_db


def pairs_to_csv(text_database: dict, texts_list_file: str = "survey/texts_for_survey.txt",
                 separator: str = "\t", csv_file_name: str = "pairs"):
    """
    Create CSV file with survey text pairs.
    :param text_database: Dict database of extracted corpus information.
    :param texts_list_file: Path of the txt file with the final list of edited texts for the survey.
    :param separator: Separator string for CSV.
    :param csv_file_name: Name for the CSV file saved to disk.
    :return: None, file saved to disk.
    """
    pairs_db: dict = build_survey_pairs(text_database, texts_list_file)
    # check for potential separators that occur in the text:
    if separator in [",", ";", "\n"]:
        print(f"Given separator '{separator}' can not be used. Tabulator character will be used instead.")
        separator = "\t"
    # format rows:
    out_list: list = list()
    for txt_id, pair in pairs_db.items():
        out_row: str = f"{txt_id}{separator}{pair['claim_last']}{separator}{pair['claim_first']}"
        out_list.append(out_row)
    # join rows:
    out_string: str = "\n".join(out_list)
    # write to disk:
    with open(f"survey/{csv_file_name}.csv", 'w', encoding='utf-8') as csv_file:
        csv_file.write(out_string)


def pairs_to_simple_list(text_database: dict, texts_list_file: str = "survey/texts_for_survey.txt",
                         out_list_file_name: str = "pairs"):
    """
    Create simple text file with survey text pairs.
    :param text_database: Dict database of extracted corpus information.
    :param texts_list_file: Path of the txt file with the final list of edited texts for the survey.
    :param out_list_file_name: Name for the file saved to disk.
    :return: None, file saved to disk.
    """
    pairs_db: dict = build_survey_pairs(text_database, texts_list_file)

    out_list: list = list()

    for txt_id, pair in pairs_db.items():
        out_row: str = f"{txt_id}\n{pair['claim_last']}\n{pair['claim_first']}\n---"
        out_list.append(out_row)

    out_string: str = "\n".join(out_list)

    with open(f"survey/{out_list_file_name}.txt", 'w', encoding='utf-8') as out_list_file:
        out_list_file.write(out_string)


def process_survey_answers(text_database: dict, texts_list_file: str = "survey/texts_for_survey.txt",
                           answers_csv: str = "survey/survey_answers.csv"):
    """
    Process raw survey answer data into usable pandas.DataFrame with
    [original text id, #claim-last choices, #claim-first choices, #edited choices, #unedited choices].
    :param text_database: Dict database of extracted corpus information.
    :param texts_list_file: Path of the txt file with the final list of edited texts for the survey.
    :param answers_csv: Path to the raw survey answers CSV file.
    :return: A pandas.DataFrame with the processed answer counts.
    """
    # read the raw CSV into a DataFrame:
    answers_df: pandas.DataFrame = pandas.read_csv(answers_csv)
    # get a dict db with processing info:
    processing_db: dict = survey_processing_pairs(text_database, texts_list_file)
    # create list to collect results:
    results_list: list = list()
    # iterate over texts:
    for txt_id, pair_data in processing_db.items():
        # create dict to collect individual text results:
        txt_result_dict: dict = dict()
        txt_result_dict['txt_id'] = txt_id
        txt_result_dict['claim_last'] = 0
        txt_result_dict['claim_first'] = 0
        txt_result_dict['edited'] = 0
        txt_result_dict['unedited'] = 0
        # iterate over chosen answers:
        for answer in answers_df[pair_data['form_text_id']]:
            if answer == pair_data['claim_last']['text']:
                txt_result_dict['claim_last'] += 1
                if pair_data['claim_last']['edited']:
                    txt_result_dict['edited'] += 1
                else:
                    txt_result_dict['unedited'] += 1
            else:
                txt_result_dict['claim_first'] += 1
                if pair_data['claim_first']['edited']:
                    txt_result_dict['edited'] += 1
                else:
                    txt_result_dict['unedited'] += 1
        # collect results:
        results_list.append(txt_result_dict)
    # create DataFrame from results list:
    results_df = pandas.DataFrame(results_list)

    return results_df


if __name__ == "__main__":
    # load database:
    with open("extracted_db.json", 'r', encoding='utf-8') as db_file:
        database: dict = json.load(db_file)
    # get and show information about the texts edited for the survey:
    # survey_info = survey_texts_info(database)
    # print(survey_info)
    # calculate and show variable value frequencies in the texts edited for the survey:
    # survey_freqs = survey_texts_frequencies(database)
    # print(survey_freqs)
    # create a list with a balanced number of originally claim-first and originally claim-last texts:
    # balanced_texts_list = create_balanced_text_list(database)
    # print(balanced_texts_list)
    # create a dict {textID:{claim-last, claim-first}} based on a txt list of texts selected for the survey.
    # survey_pairs = build_survey_pairs(database, "survey/final_texts_list.txt")
    # print(survey_pairs)

    # save a CSV with the final survey data to disk:
    # pairs_to_csv(database, "survey/final_texts_list.txt")
    # save a txt with the final survey data in easily copy-able format to disk:
    # pairs_to_simple_list(database, "survey/final_texts_list.txt")
    """
    to_cull = read_texts_list("survey/20_cull.txt")
    tested_list = read_texts_list("survey/final_texts_list.txt")
    remaining = [txt_id for txt_id in tested_list if txt_id not in to_cull]
    print(remaining)
    txt_not_culled = False
    for txt_id in to_cull:
        if txt_id in remaining:
            print(txt_id)
            txt_not_culled = True
    if txt_not_culled:
        print("text not culled!")
    else:
        print("texts culled!")

    new_list_txt = "\n".join(remaining)

    with open("survey/new_final_texts_list.txt", 'w', encoding="utf-8") as outfile:
        outfile.write(new_list_txt)

    new_freqs = survey_texts_frequencies(database, "survey/new_final_texts_list.txt")
    print(new_freqs)
    """

    # print(survey_texts_frequencies(database, "survey/final_30.txt"))
    # print(get_original_first(database, "survey/final_30.txt"))
    """
    earlier = get_original_last(database, "survey/final_texts_list.txt")
    now = get_original_last(database, "survey/final_30.txt")
    overlap = [txt_id for txt_id in earlier if not txt_id in now]
    print(overlap)
    """
    # pairs_to_simple_list(database, "survey/final_30.txt", out_list_file_name="30_pairs")

    # survey_pairs_db = survey_processing_pairs(database, "survey/final_30.txt")
    # print(survey_pairs_db)

    survey_results_df = process_survey_answers(database, "survey/final_30.txt",
                                               "survey/survey_answers_raw_010324.csv")
    # print(survey_results_df)

    # print(survey_results_df['claim_last'])

    claim_last_sum = sum(survey_results_df['claim_last'])
    claim_first_sum = sum(survey_results_df['claim_first'])
    print("claim last:", claim_last_sum, "claim first:", claim_first_sum)

    edited_sum = sum(survey_results_df['edited'])
    unedited_sum = sum(survey_results_df['unedited'])
    print("edited:", edited_sum, "unedited:", unedited_sum)
