""" Experimenting with automated unit bigram handling """

import json


# load database:
with open("extracted_db.json", 'r', encoding='utf-8') as db_file:
    database: dict = json.load(db_file)

# inst_id = "b009"
inst_id = "b001"
instance = database[inst_id]

# print(instance)


def sublist_match(main_list, sub_list) -> bool:
    if not sub_list:
        return False
    first_idx: int = int()
    for item_idx, item in enumerate(main_list):
        if item == sub_list[0]:
            first_idx = item_idx
            break
    if main_list[first_idx:first_idx+len(sub_list)] == sub_list:
        return True
    else:
        return False


# print(sublist_match(['a','b','c','d'], ['b','c']))
# print(sublist_match(['a','b','c','d'], ['b','d']))


""""""
for unit_idx, unit in enumerate(instance['units']):
    print(unit)
    """
    if unit['attach_dist'] == -1:
        # if instance['units'][unit_idx-1]['arg_trace'] in unit['arg_trace']:
        if sublist_match(unit['arg_trace'], instance['units'][unit_idx-1]['arg_trace']):
            print(f"relation overlap with prior unit {unit_idx}")
    if unit['attach_dist']:
        # if instance['units'][unit_idx-1]['arg_trace'] in unit['arg_trace']:
        if sublist_match(unit['arg_trace'], instance['units'][unit_idx+unit['attach_dist']]['arg_trace']):
            print(f"relation overlap with unit {unit_idx}")
    """
    for other_unit_idx, other_unit in enumerate(instance['units']):
        if other_unit_idx != unit_idx:
            if sublist_match(unit['arg_trace'], other_unit['arg_trace']):
                print(f"relation overlap with unit {other_unit['adu_id']}")

