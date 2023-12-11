""" Randomly shuffling units for exploration """

import json
from itertools import permutations


# load database:
with open("extracted_db.json", 'r', encoding='utf-8') as db_file:
    database: dict = json.load(db_file)


def shuffled_variants(text_id: str) -> list:
    """
    Creates list of all possible permutations of units in a text.
    :param text_id: Corpus microtext ID.
    :return: List[Tuple[unit permutation]]
    """
    # get the units list of the given microtext:
    units: list = database[text_id]['units']
    # create all possible permutations:
    all_variants: list = list(permutations(units))
    return all_variants


def pretty_units(text_units: list):
    """
    Pretty-prints a readable version of a text unit list.
    :param text_units: List of text unit dicts.
    :return: None, prints to console.
    """
    for text_unit in text_units:
        print(text_unit['edu_id'], text_unit['adu_stance'], text_unit['text'])


def show_shuffled_variants(text_id: str):
    """
    Shows all possible shuffled variants for a given microtext.
    :param text_id: Corpus microtext ID.
    :return: None, prints to console.
    """
    variants = shuffled_variants(text_id)
    for var_idx, variant in enumerate(variants):
        if var_idx == 0:
            print(f"Original text:")
        else:
            print(f"Variant {var_idx}:")
        pretty_units(variant)


if __name__ == "__main__":
    show_shuffled_variants('b009')
