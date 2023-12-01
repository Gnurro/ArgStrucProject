""" Calculating various statistics etc from extracted database """

import json

# load database:
with open("extracted_db.json", 'r', encoding='utf-8') as db_file:
    database: dict = json.load(db_file)

# print(database)
# print(database['b001'])


def topic_frequencies() -> dict:
    """
    Texts per topic.
    :return: Dictionary with topic keys.
    """
    topic_counts: dict = dict()
    for inst_id, inst in database.items():
        if inst['topic'] not in topic_counts:
            topic_counts[inst['topic']] = 1
        else:
            topic_counts[inst['topic']] += 1
    return topic_counts


# print(topic_frequencies())

def length_frequencies() -> dict:
    """
    Frequencies of text lengths in units.
    :return: Dictionary with frequencies of text lengths.
    """
    length_counts: dict = dict()
    for inst_id, inst in database.items():
        inst_len = len(inst['units'])
        if inst_len not in length_counts:
            length_counts[inst_len] = 1
        else:
            length_counts[inst_len] += 1
    return length_counts


# print(length_frequencies())


def central_position_frequencies() -> dict:
    """
    Frequencies of central claim positions.
    :return: Dictionary with frequencies of central claim positions.
    """
    central_pos_counts: dict = dict()
    for inst_id, inst in database.items():
        central_pos = inst['central_pos']
        if central_pos not in central_pos_counts:
            central_pos_counts[central_pos] = 1
        else:
            central_pos_counts[central_pos] += 1
    return central_pos_counts


# print(central_position_frequencies())


def unit_role_frequencies() -> dict:
    """
    Frequencies of unit roles and opponent positions.
    :return: Dictionary with frequencies of unit roles and opponent positions.
    """
    unit_role_counts: dict = dict()
    opp_pos_counts: dict = dict()
    for inst_id, inst in database.items():
        inst_roles = inst['unit_roles']
        for idx, role in enumerate(inst_roles):
            if role not in unit_role_counts:
                unit_role_counts[role] = 1
            else:
                unit_role_counts[role] += 1
            if role == "opp":
                if idx+1 not in opp_pos_counts:
                    opp_pos_counts[idx+1] = 1
                else:
                    opp_pos_counts[idx+1] += 1

    return {'frequencies': unit_role_counts, 'opp_positions': opp_pos_counts}


# print(unit_role_frequencies())


def relation_frequencies(topic: str = "", stance: str = "") -> dict:
    """
    Relation frequencies in the corpus.
    :param topic:
    :param stance:
    :return: Dictionary with type and category frequencies.
    """
    rel_counts: dict = dict()
    for inst_id, inst in database.items():
        if topic:
            if not inst['topic'] == topic:
                continue
        if stance:
            if not inst['stance'] == stance:
                continue
        cur_rels: dict = inst['relations']
        for cur_rel in cur_rels.values():
            if cur_rel['type'] not in rel_counts:
                rel_counts[cur_rel['type']] = 1
            else:
                rel_counts[cur_rel['type']] += 1

    if 'sup' in rel_counts and 'exa' in rel_counts:
        rel_counts['support'] = rel_counts['sup'] + rel_counts['exa']
    else:
        rel_counts['support'] = rel_counts['sup']
    rel_counts['attack'] = rel_counts['reb'] + rel_counts['und']

    return rel_counts


# print(relation_frequencies())
# print(relation_frequencies(topic="waste_separation"))
# print(relation_frequencies(stance="pro"))
