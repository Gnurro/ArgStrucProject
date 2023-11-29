""" Getting central claims """

import xml.etree.ElementTree as ET
import os


CORPUS_PATH = "corpus/en/"

central_edus = list()

for file in os.listdir(CORPUS_PATH):
    if file[-4:] == ".xml":
        tree = ET.parse(f"{CORPUS_PATH}{file}")
        root = tree.getroot()

        cur_seg_dict = dict()
        cur_rel_dict = dict()

        # print(root.attrib)

        cur_topic = "individual"
        if 'topic_id' in root.attrib:
            cur_topic = root.attrib['topic_id']

        cur_main_stance = "unknown"
        if 'stance' in root.attrib:
            cur_main_stance = root.attrib['stance']

        for child in root:
            if child.tag == 'edge':
                if child.attrib['type'] == 'seg':
                    cur_seg_dict[child.attrib['src']] = child.attrib['trg']
                else:
                    cur_rel_dict[child.attrib['src']] = {'trg': child.attrib['trg'], 'type': child.attrib['type']}

        # print(cur_seg_dict)
        # print(cur_rel_dict)

        cur_adu_dict = dict()

        for child in root:
            if child.tag == 'adu':
                if child.attrib['id'] not in cur_adu_dict:
                    cur_adu_dict[child.attrib['id']] = child.attrib['type']

        cur_edus_dict = dict()

        for child in root:
            if child.tag == 'edu':
                cur_edus_dict[child.attrib['id']] = child.text
                cur_adu_id = cur_seg_dict[child.attrib['id']]

                # identify central claim EDUs by them not being the source of any edge:
                if cur_adu_id not in cur_rel_dict:
                    central_edus.append({'file': f"{file}",
                                         'edu_id': child.attrib['id'],
                                         'adu_id': cur_adu_id,
                                         'main_stance': cur_main_stance,
                                         'adu_stance': cur_adu_dict[cur_adu_id],
                                         'text': child.text,
                                         'topic': cur_topic
                                         })
        # break

        # print(cur_edus_dict)

for central_edu in central_edus:
    print(central_edu)

central_position_freqs = dict()

for central_edu in central_edus:
    cur_pos = central_edu['adu_id'][1:]
    if cur_pos not in central_position_freqs:
        central_position_freqs[cur_pos] = 1
    else:
        central_position_freqs[cur_pos] += 1

print(central_position_freqs)
