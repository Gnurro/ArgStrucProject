""" Exploring single file structure """

import xml.etree.ElementTree as ET

CORPUS_PATH = "corpus/en/"

inst_id = "001"

tree = ET.parse(f"{CORPUS_PATH}micro_b{inst_id}.xml")
root = tree.getroot()

"""
# show contents:
print(root.tag, root.attrib)

for child in root:
    print(child.tag, child.attrib)
    if child.text:
        print(child.text)
"""

# print(root[0].attrib)
# print(type(root[0].attrib))

"""
# text in order, with EDU tags:
full_text_edus = str()

for child in root:
    # print(child.tag, child.attrib)
    if child.tag == 'edu':
        # print(child.text)
        full_text += f"[{child.attrib['id']}]{child.text} "
    # if child.text:
    #    print(child.text)
print(full_text_edus)
"""

# ADUs to EDUs:
adu_dict = dict()

for child in root:
    if child.tag == 'adu':
        adu_dict[child.attrib['id']] = {'stance': child.attrib['type'], 'edus': []}
    elif child.tag == 'edge':
        if child.attrib['type'] == 'seg':
            adu_dict[child.attrib['trg']]['edus'].append(child.attrib['src'])

# print(adu_dict)

# EDUs to ADUs:
"""
edu_dict = dict()

for child in root:
    if child.tag == 'edu':
        edu_dict[child.attrib['id']] = {'text': child.text}
    elif child.tag == 'edge':
        if child.attrib['type'] == 'seg':
            edu_dict[child.attrib['src']]['adu'] = child.attrib['trg']

print(edu_dict)
"""
edu_list = list()

for child in root:
    if child.tag == 'edu':
        # edu_dict[child.attrib['id']] = {'text': child.text}
        edu_list.append({'id': child.attrib['id'], 'text': child.text})
    elif child.tag == 'edge':
        if child.attrib['type'] == 'seg':
            for edu in edu_list:
                if edu['id'] == child.attrib['src']:
                    edu['adu'] = child.attrib['trg']
            # edu_dict[child.attrib['src']]['adu'] = child.attrib['trg']

# print(edu_list)


# text in order with ADU tags:
full_text_adus = str()

"""
for edu_id, content in edu_dict.items():
    print(edu_id)
    print(content)
"""
"""
for idx, edu in enumerate(edu_dict.items()):
    print(idx, edu)
"""
for idx, edu in enumerate(edu_list):
    # print(idx, edu)
    full_text_adus += f"[{edu['adu']} {adu_dict[edu['adu']]['stance']}]{edu['text']}"
    """
    if idx+1<len(edu_list) and edu_list[idx+1]['adu'] == edu['adu']:
        print("same adu")
    else:
        print("different adu")
    """

# print(full_text_adus)

# iterate ADUs in order:
for idx, edu in enumerate(edu_list):
    # print(idx, edu)
    print(f"[{edu['adu']} {adu_dict[edu['adu']]['stance']}]{edu['text']}")

# stance order:
stance_list = list()
for idx, edu in enumerate(edu_list):
    # print(idx, edu)
    # full_text_adus += f"[{edu['adu']} {adu_dict[edu['adu']]['stance']}]{edu['text']}"
    stance_list.append(adu_dict[edu['adu']]['stance'])
print(stance_list)