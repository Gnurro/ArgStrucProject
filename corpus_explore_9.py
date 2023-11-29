""" Exploring attachment distances and patterns """

import xml.etree.ElementTree as ET
import os
from copy import deepcopy

CORPUS_PATH = "corpus/en/"

attach_dist_dict = dict()

linear_strats = list()

for file in os.listdir(CORPUS_PATH):
    if file[-4:] == ".xml":
        # print(file)
        tree = ET.parse(f"{CORPUS_PATH}{file}")
        root = tree.getroot()

        cur_seg_dict = dict()
        cur_rel_dict = dict()

        for child in root:
            if child.tag == 'edge':
                # print(child.attrib)
                if child.attrib['type'] == 'seg':
                    cur_seg_dict[child.attrib['src']] = child.attrib['trg']
                else:
                    cur_rel_dict[child.attrib['id']] = {'src': child.attrib['src'],
                                                        'trg': child.attrib['trg'],
                                                        'type': child.attrib['type']}

        # print(cur_seg_dict)
        # print(cur_rel_dict)

        cur_adu_dist_dict = dict()

        for child in root:
            if child.tag == 'adu':
                cur_adu_id = child.attrib['id']
                if cur_adu_id not in cur_adu_dist_dict:
                    cur_adu_dist_dict[cur_adu_id] = 0

        # print(cur_adu_dist_dict)

        cur_chains = list()
        cur_open_chains = list()

        for rel in cur_rel_dict:
            # print(rel, cur_rel_dict[rel])
            if cur_rel_dict[rel]['trg'][0] == "c":
                # print(f"{rel} targets other edge {cur_rel_dict[rel]['trg']}")
                # print(f"{cur_rel_dict[cur_rel_dict[rel]['trg']]['trg']}")
                # print(f"which targets {cur_rel_dict[cur_rel_dict[rel]['trg']]['trg']}")
                cur_open_chains.append((cur_rel_dict[rel]['src'], cur_rel_dict[rel]['trg']))
            else:
                cur_chains.append((cur_rel_dict[rel]['src'], cur_rel_dict[rel]['trg']))

        # print(cur_open_chains)

        for idx, open_chain in enumerate(cur_open_chains):
            # print(open_chain)
            # print(open_chain[1])

            if open_chain[1][0] == "c":
                # print(cur_rel_dict[open_chain[1]])
                # print()
                cur_open_chains.append((open_chain[0], cur_rel_dict[open_chain[1]]['src']))
            else:
                cur_chains.append(open_chain)

        # print(cur_open_chains)

        # print(cur_chains)

        for chain in cur_chains:
            # print(chain)
            distance = int(chain[1][1:]) - int(chain[0][1:])
            # print(distance)
            if distance not in attach_dist_dict:
                attach_dist_dict[distance] = 1
            else:
                attach_dist_dict[distance] += 1

            cur_adu_dist_dict[chain[0]] = distance

        # print(cur_adu_dist_dict)

        cur_linear_strat = ["f" if dist > 0 else "b" if dist < 0 else "c" for dist in cur_adu_dist_dict.values()]

        # print(cur_linear_strat)

        linear_strats.append(
            {'file': file, 'linear_strat': cur_linear_strat}
        )


# print(attach_dist_dict)
# for linear_strat in linear_strats:
#    print(linear_strat)

lin_strat_freqs = dict()

for linear_strat in linear_strats:
    # print(linear_strat)
    cur_strat = str(linear_strat['linear_strat'])
    if cur_strat not in lin_strat_freqs:
        lin_strat_freqs[cur_strat] = {'count': 1, 'where': [linear_strat['file']]}
    else:
        lin_strat_freqs[cur_strat]['count'] += 1
        lin_strat_freqs[cur_strat]['where'].append(linear_strat['file'])


# for linear_strat in lin_strat_freqs:
#    print(linear_strat, lin_strat_freqs[linear_strat])

abs_linear_strat_list = list()

for linear_strat in linear_strats:
    cur_strat = deepcopy(linear_strat['linear_strat'])
    # print(cur_strat)
    cur_abs_strat = list()
    # cur_abs_strat = []

    for direction in cur_strat:
        if len(cur_abs_strat) == 0:
            cur_abs_strat.append(direction)
            # print(cur_abs_strat)
        else:
            if cur_abs_strat[-1] == direction:
                cur_abs_strat[-1] = f"{direction}+"
                # print(cur_abs_strat)
            elif cur_abs_strat[-1] == f"{direction}+":
                # print(cur_abs_strat)
                pass
            else:
                cur_abs_strat.append(direction)
                # print(cur_abs_strat)

    # print(cur_strat)
    # print(cur_strat)

    abs_linear_strat_list.append(
        {'file': linear_strat['file'], 'abs_strat': cur_abs_strat}
    )

    # break
    # print()

# for abs_linear_strat in abs_linear_strat_list:
#    print(abs_linear_strat)

abs_lin_strat_freqs = dict()

for abs_linear_strat in abs_linear_strat_list:
    # print(linear_strat)
    cur_strat = str(abs_linear_strat['abs_strat'])
    if cur_strat not in abs_lin_strat_freqs:
        abs_lin_strat_freqs[cur_strat] = {'count': 1, 'where': [abs_linear_strat['file']]}
    else:
        abs_lin_strat_freqs[cur_strat]['count'] += 1
        abs_lin_strat_freqs[cur_strat]['where'].append(abs_linear_strat['file'])

for abs_linear_strat in abs_lin_strat_freqs:
    print(abs_linear_strat, abs_lin_strat_freqs[abs_linear_strat])
