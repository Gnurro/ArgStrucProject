""" Exploring stance structure """

import xml.etree.ElementTree as ET
import os


CORPUS_PATH = "corpus/en/"

stance_orders_list = list()

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

        main_stance = "unknown"
        if 'stance' in root.attrib:
            main_stance = root.attrib['stance']

        for child in root:
            if child.tag == 'edge':
                if child.attrib['type'] == 'seg':
                    cur_seg_dict[child.attrib['src']] = child.attrib['trg']
                else:
                    cur_rel_dict[child.attrib['src']] = {'trg': child.attrib['trg'], 'type': child.attrib['type']}

        # print(cur_seg_dict)
        # print(cur_rel_dict)

        cur_edus_dict = dict()

        cur_stance_list = list()

        for child in root:
            if child.tag == 'adu':
                cur_adu_id = child.attrib['id']
                cur_stance = child.attrib['type']

                cur_stance_list.append(cur_stance)

        # break

        # print(cur_stance_list)

        stance_orders_list.append({
            'file': file,
            'main_stance': main_stance,
            'stance_order': cur_stance_list
        })

# for stance_order in stance_orders_list:
#    print(stance_order)

stance_orders_freqs = dict()

for stance_order in stance_orders_list:
    cur_order = stance_order['stance_order']
    # print(cur_order)
    cur_order = str(cur_order)
    if cur_order not in stance_orders_freqs:
        stance_orders_freqs[cur_order] = 1
    else:
        stance_orders_freqs[cur_order] += 1


print("ADU stance orders and frequencies:")
for stance_order in stance_orders_freqs:
    print(stance_order, stance_orders_freqs[stance_order])


opp_pos_freqs = dict()

for stance_order in stance_orders_list:
    cur_order = stance_order['stance_order']
    # print(cur_order)
    for idx, stance in enumerate(cur_order):
        # print(idx, stance)
        if stance == "opp":
            if idx+1 not in opp_pos_freqs:
                opp_pos_freqs[idx+1] = 1
            else:
                opp_pos_freqs[idx+1] += 1

print("'opp' ADU position frequencies:")
print(opp_pos_freqs)
