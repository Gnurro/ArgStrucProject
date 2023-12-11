""" Extracting various analytic information from the corpus """

import xml.etree.ElementTree as ET
import os
import json
from copy import deepcopy

CORPUS_PATH = "corpus/en/"

# database dict to hold all instances:
database = dict()

for file_name in os.listdir(CORPUS_PATH):
    if file_name[-4:] == ".xml":
        cur_instance_id = file_name.replace(".xml", "").replace("micro_", "")

        # dict to hold data of current instance:
        cur_inst_data = dict()

        arggraph_tree = ET.parse(f"{CORPUS_PATH}{file_name}")
        arggraph_root = arggraph_tree.getroot()

        # get arggraph/current text info:
        cur_topic = "individual"  # default fallback topic
        if 'topic_id' in arggraph_root.attrib:
            cur_topic = arggraph_root.attrib['topic_id']
        cur_topic_stance = "unknown"  # default fallback topic stance
        if 'stance' in arggraph_root.attrib:
            cur_topic_stance = arggraph_root.attrib['stance']

        cur_inst_data['topic'] = cur_topic
        cur_inst_data['stance'] = cur_topic_stance

        # get edge info first, as it's needed for handling units later
        # dictionaries holding edge information of current file:
        cur_seg_dict: dict = dict()  # EDU -> ADU segmentation; {EDU-id: ADU-id, ... }
        cur_rel_dict: dict = dict()
        cur_adu_rel_dict: dict = dict()  # ADU relations; {source-id: {'trg': target-id, 'type': relation-type}, ...}

        for element in arggraph_root:
            if element.tag == 'edge':
                # EDU -> ADU segmentation edges:
                if element.attrib['type'] == 'seg':
                    cur_seg_dict[element.attrib['src']] = element.attrib['trg']
                # relation edges:
                else:
                    cur_adu_rel_dict[element.attrib['src']] = {'id': element.attrib['id'],
                                                               'trg': element.attrib['trg'],
                                                               'type': element.attrib['type']}
                    cur_rel_dict[element.attrib['id']] = {'src': element.attrib['src'],
                                                          'trg': element.attrib['trg'],
                                                          'type': element.attrib['type']}

        # print("cur_seg_dict:", cur_seg_dict)
        # print("cur_rel_dict:", cur_rel_dict)
        # print("cur_adu_rel_dict:", cur_adu_rel_dict)

        cur_inst_data['relations'] = cur_rel_dict

        # get EDUs and ADUs, using edge info to properly connect them
        # dictionaries holding unit information of current file:
        cur_edu_dict = dict()
        # {EDU-id: {'text': EDU-text, 'adu_id': ADU-id, 'rel': {'type': rel-type, 'trg': rel-trg-id}} ... }
        cur_adu_dict = dict()  # {ADU-id: ADU-stance, ... }

        cur_central_adu = str()
        cur_central_pos = int()

        for element in arggraph_root:
            if element.tag == 'edu':
                # add current EDU and its text to dict:
                cur_edu_dict[element.attrib['id']] = {'text': element.text}
                # get the ADU ID for current EDU:
                cur_adu_id = cur_seg_dict[element.attrib['id']]
                # all EDU IDs in the corpus match their ADU's ID
                # this allows to just switch 'e' and 'a' in the ID string to get the corresponding unit
                # BUT using cur_seg_dict is always safe, and will work in case the extended corpus is different
                cur_edu_dict[element.attrib['id']]['adu_id'] = cur_adu_id
                # current unit's relation target and type:
                cur_rel_trg: dict = {}  # {'type': relation-type, 'trg': relation-target-id}
                if cur_adu_id in cur_adu_rel_dict:
                    cur_rel_trg = {'id': cur_adu_rel_dict[cur_adu_id]['id'],
                                   'type': cur_adu_rel_dict[cur_adu_id]['type'],
                                   'trg': cur_adu_rel_dict[cur_adu_id]['trg']}
                else:
                    cur_central_adu = cur_adu_id
                    cur_central_pos = int(cur_adu_id[1:])
                cur_edu_dict[element.attrib['id']]['rel'] = cur_rel_trg
            elif element.tag == 'adu':
                # add current ADU and its stance to dict:
                if element.attrib['id'] not in cur_adu_dict:
                    cur_adu_dict[element.attrib['id']] = element.attrib['type']

        # print("cur_edu_dict", cur_edu_dict)
        # print("cur_adu_dict", cur_adu_dict)

        cur_inst_data['unit_roles'] = list(cur_adu_dict.values())

        cur_inst_data['central_adu'] = cur_central_adu
        cur_inst_data['central_pos'] = cur_central_pos

        # relation connection chains:
        # ADUs that have a relation to a relation ('reb'uttal/'und'ercut/'add'ing linked support) are assumed to have
        # a connection to the source of the relation they have a relation to which needs to be resolved recursively
        cur_chains: list = list()  # resolved ADU->ADU connection chains
        cur_open_chains: list = list()  # open/unresolved ADU->EDGE connection chains

        for rel in cur_rel_dict:
            # get open chains by checking for targets that are relations
            if cur_rel_dict[rel]['trg'][0] == "c":  # relation IDs always start with "c"
                # add open chains to list to be recursively resolved later:
                cur_open_chains.append((cur_rel_dict[rel]['src'], cur_rel_dict[rel]['trg']))
            else:
                # add direct ADU->ADU relations, which don't need to be resolved, to list:
                cur_chains.append((cur_rel_dict[rel]['src'], cur_rel_dict[rel]['trg']))

        # print(cur_open_chains)

        # untangle relation connection chains:
        for open_chain in cur_open_chains:
            # if the open chain ends with a relation:
            if open_chain[1][0] == "c":
                # add an open chain ending with the target of the relation to list:
                cur_open_chains.append((open_chain[0], cur_rel_dict[open_chain[1]]['src']))
                # this intentionally appends ADU->ADU chains
            else:
                # if the 'open' chain does not end with a relation, it ends with an ADU and is resolved:
                cur_chains.append(open_chain)

        # print("cur_open_chains", cur_open_chains)
        # print("cur_chains", cur_chains)

        # combine extracted unit data:
        cur_units = list()

        for edu_id, content in cur_edu_dict.items():
            cur_unit = dict()
            cur_unit['edu_id'] = edu_id
            cur_unit['adu_id'] = content['adu_id']
            cur_unit['text'] = content['text']
            cur_unit['rel'] = content['rel']
            cur_unit['adu_stance'] = cur_adu_dict[content['adu_id']]

            attach = ""
            for chain in cur_chains:
                if chain[0] == content['adu_id']:
                    attach = chain[1]
            cur_unit['attach'] = attach

            attach_dist = 0
            if attach:
                attach_dist = int(attach[1:]) - int(content['adu_id'][1:])
            cur_unit['attach_dist'] = attach_dist

            cur_units.append(cur_unit)

        cur_inst_data['units'] = cur_units

        # graph tracing:
        for unit in cur_units:
            cur_unit_branch = list()
            # print("current unit:", unit['adu_id'])
            cur_unit_branch.append(unit['adu_id'])

            if unit['rel']:
                # print("current unit relation:", unit['rel'])
                cur_unit_branch.append(unit['rel']['id'])
                cur_unit_branch.append(unit['rel']['trg'])

            while cur_unit_branch[-1] != cur_inst_data['central_adu']:
                cur_last_branch = deepcopy(cur_unit_branch[-1])

                if cur_last_branch != cur_inst_data['central_adu']:
                    # print("current last branch element:", cur_last_branch)
                    if cur_last_branch[0] == "c":
                        # print("relation target")
                        # print("relation:", cur_rel_dict[cur_last_branch])
                        cur_unit_branch.append(cur_rel_dict[cur_last_branch]['trg'])
                    elif cur_unit_branch[-1][0] == "a":
                        # print("adu target")
                        # print("target adu relation:", cur_adu_rel_dict[cur_last_branch])
                        cur_unit_branch.append(cur_adu_rel_dict[cur_last_branch]['id'])
                        cur_unit_branch.append(cur_adu_rel_dict[cur_last_branch]['trg'])
                # print(cur_inst_data['central_adu'])
            # print("full unit arg graph trace:", cur_unit_branch)
            cur_unit_depth = len(cur_unit_branch)-1
            # print("current unit arg graph depth:", cur_unit_depth)
            unit['depth'] = cur_unit_depth
            # get intermediate trace:
            if cur_unit_depth >= 2:
                inter_trace = cur_unit_branch[1:-1]
                # print("intermediate trace:", inter_trace)
                unit['arg_trace'] = inter_trace
            # print()

        cur_lin_strat = list()

        for unit in cur_units:
            if unit['attach_dist'] > 0:
                cur_lin_strat.append("f")
            elif unit['attach_dist'] < 0:
                cur_lin_strat.append("b")
            else:
                cur_lin_strat.append("c")

        cur_inst_data['lin_strat'] = cur_lin_strat

        # print("cur_inst_data", cur_inst_data)

        database[cur_instance_id] = cur_inst_data

        # break

# print(database)
""""""
db_json = json.dumps(database, indent=2)

with open("extracted_db.json", 'w', encoding='utf-8') as out_file:
    out_file.write(db_json)

