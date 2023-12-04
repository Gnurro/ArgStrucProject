""" Checking permutation-related unit aspects in extracted database """

import json
import re

# load database:
with open("extracted_db.json", 'r', encoding='utf-8') as db_file:
    database: dict = json.load(db_file)

# SPLIT UNITS


def get_split_units():
    split_units: list = list()
    for inst_id, inst in database.items():
        inst_units = inst['units']
        for unit in inst_units:
            if unit['text'][0].islower():
                split_units.append((inst_id, unit))
            elif unit['text'][-1] not in [".", "!", "?"]:
                split_units.append((inst_id, unit))

    return split_units


def split_clause_prior_rel_inspect():
    split_units: list = get_split_units()

    for split_unit in split_units:
        # print(split_unit)
        # print(split_unit[1]['text'])
        if split_unit[1]['attach_dist'] == -1 and split_unit[1]['text'][0].islower():
            prior_text = database[split_unit[0]]['units'][int(split_unit[1]['edu_id'][1:]) - 2]['text']
            # print(prior_text)
            # print(prior_text, split_unit[1]['text'])
            # print(split_unit[1]['rel']['type'])
            print(f"{prior_text}[<-{split_unit[1]['rel']['type']}]{split_unit[1]['text']}")


# split_clause_prior_rel_inspect()


def split_clause_follow_rel_inspect():
    split_units: list = get_split_units()

    for split_unit in split_units:
        # print(split_unit)
        # print(split_unit[1]['text'])
        if split_unit[1]['attach_dist'] == 1 and split_unit[1]['text'][-1] not in [".", "!", "?"]:
            follow_text = database[split_unit[0]]['units'][int(split_unit[1]['edu_id'][1:])]['text']
            # print(prior_text)
            # print(prior_text, split_unit[1]['text'])
            # print(split_unit[1]['rel']['type'])
            print(f"{split_unit[1]['text']}[{split_unit[1]['rel']['type']}->]{follow_text}")


# split_clause_follow_rel_inspect()


# ANAPHORA

PRONOUN_PATTERN = r'\b(he|she|it|they|him|her|them|his|hers|its|theirs)\b'
PRONOUN_PATTERN_2 = r'\b(this|these|that|those|former|latter|who|whom|whose|what|which)\b'


def get_pronoun_units():
    pronoun_units: list = list()
    for inst_id, inst in database.items():
        inst_units = inst['units']
        for unit in inst_units:
            pronouns = re.findall(PRONOUN_PATTERN, unit['text'], re.IGNORECASE)
            pronouns += re.findall(PRONOUN_PATTERN_2, unit['text'], re.IGNORECASE)
            # print(pronouns)
            if pronouns:
                pronoun_units.append((inst_id, pronouns, unit))
        # break

    return pronoun_units


"""
pronoun_units = get_pronoun_units()
for pronoun_unit in pronoun_units:
    print(pronoun_unit)
"""

# COMBINED FEATURES SETS


def get_simple_set() -> set:
    """
    Get the set of texts that have no pronouns and no split units.
    :return: Set of texts that have no pronouns and no split units.
    """
    all_texts_set = set(database.keys())
    split_unit_texts = set()
    for split_unit in get_split_units():
        split_unit_texts.add(split_unit[0])
    pronoun_unit_texts = set()
    for pronoun_unit in get_pronoun_units():
        pronoun_unit_texts.add(pronoun_unit[0])
    bad_unit_texts = split_unit_texts.union(pronoun_unit_texts)
    simple_set = all_texts_set.difference(bad_unit_texts)
    return simple_set


# print(get_simple_set())


# LINEARIZATION STRATEGIES


def get_central_first_texts() -> dict:
    central_first_texts: dict = dict()
    for inst_id, inst in database.items():
        if inst['lin_strat'][0] == "c":
            central_first_texts[inst_id] = inst
    return central_first_texts


"""
for text_id, content in get_central_first_texts().items():
    print(text_id, content)
"""


def get_central_last_texts() -> dict:
    central_last_texts: dict = dict()
    for inst_id, inst in database.items():
        if inst['lin_strat'][-1] == "c":
            central_last_texts[inst_id] = inst
    return central_last_texts


"""
for text_id, content in get_central_last_texts().items():
    print(text_id, content)
"""

# UTILITY


def pretty_text(text_content):
    text_units = text_content['units']
    for text_unit in text_units:
        print(text_unit['edu_id'], text_unit['text'])


# pretty_text(database['b001'])


def pretty_text_db(text_database: dict):
    for text_id, content in text_database.items():
        print(f"Text {text_id}")
        pretty_text(content)


pretty_text_db(get_central_first_texts())
