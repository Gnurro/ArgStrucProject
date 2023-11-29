""" Exploring edges """

import xml.etree.ElementTree as ET
import os


CORPUS_PATH = "corpus/en/"

# edge_set = set()
edge_set = {'reb', 'add', 'sup', 'seg', 'und', 'exa'}

add_trg_set = set()
add_trg_type_set = set()

reb_trg_set = set()
reb_trg_type_set = set()

sup_trg_set = set()
sup_trg_type_set = set()

exa_trg_set = set()
exa_trg_type_set = set()

und_trg_set = set()
und_trg_type_set = set()

rel_freqs = dict()

# TODO: opponent/proponent correlation

for file in os.listdir(CORPUS_PATH):
    if file[-4:] == ".xml":
        tree = ET.parse(f"{CORPUS_PATH}{file}")
        root = tree.getroot()

        edges = dict()

        for child in root:
            if child.tag == 'edge':
                edge_set.add(child.attrib['type'])

                edges[child.attrib['id']] = {'type': child.attrib['type']}

                if child.attrib['type'] == 'add':
                    add_trg_set.add(child.attrib['trg'])
                    if child.attrib['trg'] in edges:
                        add_trg_type_set.add(edges[child.attrib['trg']]['type'])

                    if 'add' not in rel_freqs:
                        rel_freqs['add'] = 1
                    else:
                        rel_freqs['add'] += 1

                elif child.attrib['type'] == 'reb':
                    reb_trg_set.add(child.attrib['trg'])
                    if child.attrib['trg'] in edges:
                        reb_trg_type_set.add(edges[child.attrib['trg']]['type'])

                    if 'reb' not in rel_freqs:
                        rel_freqs['reb'] = 1
                    else:
                        rel_freqs['reb'] += 1

                elif child.attrib['type'] == 'sup':
                    sup_trg_set.add(child.attrib['trg'])
                    if child.attrib['trg'] in edges:
                        sup_trg_type_set.add(edges[child.attrib['trg']]['type'])

                    if 'sup' not in rel_freqs:
                        rel_freqs['sup'] = 1
                    else:
                        rel_freqs['sup'] += 1

                elif child.attrib['type'] == 'exa':
                    exa_trg_set.add(child.attrib['trg'])
                    if child.attrib['trg'] in edges:
                        exa_trg_type_set.add(edges[child.attrib['trg']]['type'])

                    if 'exa' not in rel_freqs:
                        rel_freqs['exa'] = 1
                    else:
                        rel_freqs['exa'] += 1

                elif child.attrib['type'] == 'und':
                    und_trg_set.add(child.attrib['trg'])
                    if child.attrib['trg'] in edges:
                        und_trg_type_set.add(edges[child.attrib['trg']]['type'])

                    if 'und' not in rel_freqs:
                        rel_freqs['und'] = 1
                    else:
                        rel_freqs['und'] += 1


rel_freqs['support'] = rel_freqs['sup'] + rel_freqs['exa']
rel_freqs['attack'] = rel_freqs['reb'] + rel_freqs['und']

print(edge_set)
print(rel_freqs)

print("sup:")
print(sup_trg_set)
print(sup_trg_type_set)

print("reb:")
print(reb_trg_set)
print(reb_trg_type_set)

print("exa:")
print(exa_trg_set)
print(exa_trg_type_set)

print("und:")
print(und_trg_set)
print(und_trg_type_set)

print("add:")
print(add_trg_set)
print(add_trg_type_set)
"""
# show contents:
print(root.tag, root.attrib)

for child in root:
    print(child.tag, child.attrib)
    if child.text:
        print(child.text)
"""