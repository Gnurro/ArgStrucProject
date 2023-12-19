""" Corpus statistics by main stance """

import json

from corpus_stats import linear_strategy_frequencies, abstract_lin_strat_frequencies
from unit_checking import get_central_first_texts, get_central_last_texts, get_central_other_texts


def get_pro_db(texts_db: dict) -> dict:
    """
    Get a dict of texts that have 'pro' main stance.
    :return: Dict of texts that have 'pro' main stance.
    """
    pro_db: dict = dict()

    for text_id, text_content in texts_db.items():
        if text_content['stance'] == "pro":
            pro_db[text_id] = text_content

    return pro_db


def get_con_db(texts_db: dict) -> dict:
    """
    Get a dict of texts that have 'con' main stance.
    :return: Dict of texts that have 'con' main stance.
    """
    con_db: dict = dict()

    for text_id, text_content in texts_db.items():
        if text_content['stance'] == "con":
            con_db[text_id] = text_content

    return con_db


def stance_lin_strat_comparison(texts_db: dict):
    pro_texts = get_pro_db(texts_db)
    pro_lin_strats = linear_strategy_frequencies(pro_texts)
    pro_abs_lin_strats = abstract_lin_strat_frequencies(pro_texts)

    con_texts = get_con_db(texts_db)
    con_lin_strats = linear_strategy_frequencies(con_texts)
    con_abs_lin_strats = abstract_lin_strat_frequencies(con_texts)

    comp_lin_strats: dict = dict()
    all_lin_strats: set = set(pro_lin_strats.keys())
    for lin_strat in con_lin_strats.keys():
        all_lin_strats.add(lin_strat)
    for lin_strat in all_lin_strats:
        if lin_strat not in comp_lin_strats:
            cur_lin_strat: dict = dict()
            if lin_strat in pro_lin_strats:
                cur_lin_strat['pro'] = pro_lin_strats[lin_strat]
            else:
                cur_lin_strat['pro'] = 0
            if lin_strat in con_lin_strats:
                cur_lin_strat['con'] = con_lin_strats[lin_strat]
            else:
                cur_lin_strat['con'] = 0
            comp_lin_strats[lin_strat] = cur_lin_strat

    comp_abs_lin_strats: dict = dict()
    all_abs_lin_strats: set = set(pro_abs_lin_strats.keys())
    for abs_lin_strat in con_abs_lin_strats.keys():
        all_abs_lin_strats.add(abs_lin_strat)
    for abs_lin_strat in all_abs_lin_strats:
        if abs_lin_strat not in comp_abs_lin_strats:
            cur_abs_lin_strat: dict = dict()
            if abs_lin_strat in pro_abs_lin_strats:
                cur_abs_lin_strat['pro'] = pro_abs_lin_strats[abs_lin_strat]
            else:
                cur_abs_lin_strat['pro'] = 0
            if abs_lin_strat in con_abs_lin_strats:
                cur_abs_lin_strat['con'] = con_abs_lin_strats[abs_lin_strat]
            else:
                cur_abs_lin_strat['con'] = 0
            comp_abs_lin_strats[abs_lin_strat] = cur_abs_lin_strat

    return comp_lin_strats, comp_abs_lin_strats


def stance_central_comparison(texts_db: dict):
    pro_texts = get_pro_db(texts_db)
    con_texts = get_con_db(texts_db)

    pro_central_first = get_central_first_texts(pro_texts)
    pro_central_last = get_central_last_texts(pro_texts)
    pro_central_other = get_central_other_texts(pro_texts)

    con_central_first = get_central_first_texts(con_texts)
    con_central_last = get_central_last_texts(con_texts)
    con_central_other = get_central_other_texts(con_texts)

    stance_centrals: dict = dict(counts=dict(pro=len(pro_texts), con=len(con_texts)),
                                 first=dict(pro=len(pro_central_first), con=len(con_central_first)),
                                 last=dict(pro=len(pro_central_last), con=len(con_central_last)),
                                 other=dict(pro=len(pro_central_other), con=len(con_central_other)))

    return stance_centrals


if __name__ == "__main__":
    # load database:
    with open("extracted_db.json", 'r', encoding='utf-8') as db_file:
        database: dict = json.load(db_file)
    """
    print("pro texts:")
    pro_texts = get_pro_db(database)
    pro_lin_strats = linear_strategy_frequencies(pro_texts)
    print(pro_lin_strats)
    pro_abs_lin_strats = abstract_lin_strat_frequencies(pro_texts)
    print(pro_abs_lin_strats)

    print("con texts:")
    con_texts = get_con_db(database)
    con_lin_strats = linear_strategy_frequencies(con_texts)
    print(con_lin_strats)
    con_abs_lin_strats = abstract_lin_strat_frequencies(con_texts)
    print(con_abs_lin_strats)
    """

    stance_lin_strats = stance_lin_strat_comparison(database)
    full_lin_strats = stance_lin_strats[0]
    # print(full_lin_strats)
    abs_lin_strats = stance_lin_strats[1]
    print(abs_lin_strats)

    print(stance_central_comparison(database))
