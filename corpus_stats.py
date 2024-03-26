""" Calculating various statistics etc from extracted database """

import json


# load database:
with open("extracted_db.json", 'r', encoding='utf-8') as db_file:
    database: dict = json.load(db_file)


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


print("Topic frequencies:")
print(topic_frequencies())


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


print("Text length (in units) frequencies:")
print(length_frequencies())


def central_position_frequencies(texts_db: dict = database) -> dict:
    """
    Frequencies of central claim positions.
    :return: Dictionary with frequencies of central claim positions.
    """
    central_pos_counts: dict = dict()
    for inst_id, inst in texts_db.items():
        central_pos = inst['central_pos']
        if central_pos not in central_pos_counts:
            central_pos_counts[central_pos] = 1
        else:
            central_pos_counts[central_pos] += 1
    return central_pos_counts


print("Central claim position frequencies:")
print(central_position_frequencies())


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


print("Unit role frequencies:")
print(unit_role_frequencies())


def relation_frequencies(topic: str = "", stance: str = "") -> dict:
    """
    Relation frequencies in the corpus.
    :param topic: Limit the counts to texts with a specific topic.
    :param stance: Limit the counts to texts with a specific main stance.
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


print("Relation frequencies for all texts:")
print(relation_frequencies())
print('Relation frequencies for texts with the "waste_separation" topic:')
print(relation_frequencies(topic="waste_separation"))
print('Relation frequencies for texts with the "pro" main stance:')
print(relation_frequencies(stance="pro"))


def linear_strategy_frequencies(texts_db: dict = database) -> dict:
    """
    Frequencies of linear strategies.
    :return: Dictionary with frequencies of linear strategies.
    """
    lin_strat_counts: dict = dict()
    for inst_id, inst in texts_db.items():
        lin_strat = tuple(inst['lin_strat'])
        if lin_strat not in lin_strat_counts:
            lin_strat_counts[lin_strat] = 1
        else:
            lin_strat_counts[lin_strat] += 1
    return lin_strat_counts


print("Linearization strategy frequencies:")
print(linear_strategy_frequencies())


def abstract_lin_strat_frequencies(texts_db: dict = database) -> dict:
    """
    Frequencies of abstracted linear strategies.
    :return: Dictionary with frequencies of abstracted linear strategies.
    """
    abs_lin_strat_counts: dict = dict()
    for inst_id, inst in texts_db.items():
        cur_strat = inst['lin_strat']
        cur_abs_strat = list()
        for direction in cur_strat:
            if len(cur_abs_strat) == 0:
                cur_abs_strat.append(direction)
            else:
                if cur_abs_strat[-1] == direction:
                    cur_abs_strat[-1] = f"{direction}+"
                elif cur_abs_strat[-1] == f"{direction}+":
                    pass
                else:
                    cur_abs_strat.append(direction)

        cur_abs_strat = tuple(cur_abs_strat)

        if cur_abs_strat not in abs_lin_strat_counts:
            abs_lin_strat_counts[cur_abs_strat] = 1
        else:
            abs_lin_strat_counts[cur_abs_strat] += 1

    return abs_lin_strat_counts


print("Abstracted linearization strategy frequencies:")
print(abstract_lin_strat_frequencies())


def claim_position_frequencies(texts_db: dict = database) -> dict:
    """
    Frequencies of claim-first/last and other orders.
    :return: Dictionary with frequencies of claim-first/last and other orders.
    """
    abs_lin_strat_freqs: dict = abstract_lin_strat_frequencies(database)
    claim_pos_counts: dict = {'claim-first': 0, 'claim-last': 0, 'other': 0}
    for abs_lin_strat in abs_lin_strat_freqs:
        # print(abs_lin_strat)
        if abs_lin_strat[0] == "c":
            claim_pos_counts['claim-first'] += abs_lin_strat_freqs[abs_lin_strat]
        elif abs_lin_strat[-1] == "c":
            claim_pos_counts['claim-last'] += abs_lin_strat_freqs[abs_lin_strat]
        else:
            claim_pos_counts['other'] += abs_lin_strat_freqs[abs_lin_strat]

    return claim_pos_counts


print("Claim position frequencies:")
print(claim_position_frequencies(database))
