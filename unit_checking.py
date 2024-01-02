""" Checking permutation-related unit aspects in extracted database """

import json
import re

# load database:
with open("extracted_db.json", 'r', encoding='utf-8') as db_file:
    database: dict = json.load(db_file)

# SPLIT UNITS


def get_split_units(texts_db: dict):
    split_units: list = list()
    for inst_id, inst in texts_db.items():
        inst_units = inst['units']
        for unit in inst_units:
            if unit['text'][0].islower():
                split_units.append((inst_id, unit))
            elif unit['text'][-1] not in [".", "!", "?"]:
                split_units.append((inst_id, unit))

    return split_units


def split_clause_prior_rel_inspect():
    split_units: list = get_split_units(database)

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
    split_units: list = get_split_units(database)

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


def get_nonsplit_db(texts_db: dict) -> dict:
    """
    Get a dict of texts that have no split units.
    :return: Dict of texts that have no split units.
    """
    all_texts_set = set(texts_db.keys())
    split_unit_texts = set()
    # print(get_split_units(texts_db))
    for split_unit in get_split_units(texts_db):
        split_unit_texts.add(split_unit[0])
    # print(split_unit_texts)
    nonsplit_set = all_texts_set.difference(split_unit_texts)
    # print(nonsplit_set)
    # for text_id in nonsplit_set:
    for text_id in split_unit_texts:
        # print(text_id)
        texts_db.pop(text_id)

    return texts_db


# print(get_nonsplit_db(database))


# LINEARIZATION STRATEGIES


def get_central_first_texts(texts_db: dict) -> dict:
    central_first_texts: dict = dict()
    for inst_id, inst in texts_db.items():
        if inst['lin_strat'][0] == "c":
            central_first_texts[inst_id] = inst
    return central_first_texts


"""
for text_id, content in get_central_first_texts().items():
    print(text_id, content)
"""


def get_central_last_texts(texts_db: dict) -> dict:
    central_last_texts: dict = dict()
    for inst_id, inst in texts_db.items():
        if inst['lin_strat'][-1] == "c":
            central_last_texts[inst_id] = inst
    return central_last_texts


"""
for text_id, content in get_central_last_texts().items():
    print(text_id, content)
"""


def get_central_other_texts(texts_db: dict) -> dict:
    central_other_texts: dict = dict()
    for inst_id, inst in texts_db.items():
        cur_is_other: bool = True
        if inst['lin_strat'][0] == "c":
            cur_is_other = False
        if inst['lin_strat'][-1] == "c":
            cur_is_other = False
        if cur_is_other:
            central_other_texts[inst_id] = inst
    return central_other_texts


# UTILITY


def pretty_text(text_content):
    text_units = text_content['units']
    for text_unit in text_units:
        print(text_unit['edu_id'], text_unit['adu_stance'], text_unit['text'])


# pretty_text(database['b001'])


def pretty_text_db(text_database: dict):
    for text_id, content in text_database.items():
        print(f"Text {text_id}, {content['topic']}: {content['stance']}")
        pretty_text(content)


# Pretty-print all central-first texts without split units:
# pretty_text_db(get_nonsplit_db(get_central_first_texts(database)))
# Pretty-print all central-last texts without split units:
# pretty_text_db(get_nonsplit_db(get_central_last_texts(database)))


if __name__ == "__main__":
    # pretty_text(database['b001'])

    # Pretty-print all central-first texts:
    pretty_text_db(get_central_first_texts(database))
    # Pretty-print all central-last texts:
    # pretty_text_db(get_central_last_texts(database))

