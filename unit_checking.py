""" Checking permutation-related unit aspects in extracted database """

import json

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


split_clause_follow_rel_inspect()
