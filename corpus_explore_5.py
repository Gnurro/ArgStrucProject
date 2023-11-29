""" Checking EDU->ADU match """

import xml.etree.ElementTree as ET
import os


CORPUS_PATH = "corpus/en/"

# central_edus = list()

for file in os.listdir(CORPUS_PATH):
    if file[-4:] == ".xml":
        tree = ET.parse(f"{CORPUS_PATH}{file}")
        root = tree.getroot()

        cur_seg_dict = dict()
        cur_rel_dict = dict()

        # print(root.attrib)

        for child in root:
            if child.tag == 'edge':
                if child.attrib['type'] == 'seg':
                    cur_seg_dict[child.attrib['src']] = child.attrib['trg']
                    src_id = child.attrib['src']
                    trg_id = child.attrib['trg']
                    if trg_id != f"a{src_id[1:]}":
                        print("mismatch", src_id, trg_id)
                else:
                    cur_rel_dict[child.attrib['src']] = {'trg': child.attrib['trg'], 'type': child.attrib['type']}
            elif child.tag == 'joint':
                print(child)

        # print(cur_seg_dict)
        # print(cur_rel_dict)

