""" Extracting various analytic information from the corpus """

import xml.etree.ElementTree as ET
import os

CORPUS_PATH = "corpus/en/"

for file_name in os.listdir(CORPUS_PATH):
    if file_name[-4:] == ".xml":
        arggraph_tree = ET.parse(f"{CORPUS_PATH}{file_name}")
        arggraph_root = arggraph_tree.getroot()

        # get arggraph/current text info:
        cur_topic = "individual"  # default fallback topic
        if 'topic_id' in arggraph_root.attrib:
            cur_topic = arggraph_root.attrib['topic_id']
        cur_topic_stance = "unknown"  # default fallback topic stance
        if 'stance' in arggraph_root.attrib:
            cur_topic_stance = arggraph_root.attrib['stance']

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
                    cur_adu_rel_dict[element.attrib['src']] = {'trg': element.attrib['trg'],
                                                               'type': element.attrib['type']}
                    cur_rel_dict[element.attrib['id']] = {'src': element.attrib['src'],
                                                          'trg': element.attrib['trg'],
                                                          'type': element.attrib['type']}

        print("cur_seg_dict:", cur_seg_dict)
        print("cur_adu_rel_dict:", cur_adu_rel_dict)

        # get EDUs and ADUs, using edge info to properly connect them
        # dictionaries holding unit information of current file:
        cur_edu_dict = dict()
        # {EDU-id: {'text': EDU-text, 'adu_id': ADU-id, 'rel': {'type': rel-type, 'trg': rel-trg-id}} ... }
        cur_adu_dict = dict()  # {ADU-id: ADU-stance, ... }

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
                    cur_rel_trg = {'type': cur_adu_rel_dict[cur_adu_id]['type'], 'trg': cur_adu_rel_dict[cur_adu_id]['trg']}
                cur_edu_dict[element.attrib['id']]['rel'] = cur_rel_trg
            elif element.tag == 'adu':
                # add current ADU and its stance to dict:
                if element.attrib['id'] not in cur_adu_dict:
                    cur_adu_dict[element.attrib['id']] = element.attrib['type']

        print("cur_edu_dict", cur_edu_dict)
        print("cur_adu_dict", cur_adu_dict)

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

        print("cur_open_chains", cur_open_chains)
        print("cur_chains", cur_chains)

        """
        for chain in cur_chains:
            # print(chain)
            distance = int(chain[1][1:]) - int(chain[0][1:])
            # print(distance)
            if distance not in attach_dist_dict:
                attach_dist_dict[distance] = 1
            else:
                attach_dist_dict[distance] += 1

            cur_adu_dist_dict[chain[0]] = distance
        """

        break