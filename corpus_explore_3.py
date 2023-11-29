""" Exploring split clause units """

import xml.etree.ElementTree as ET
import os


CORPUS_PATH = "corpus/en/"

lower_edus = list()

for file in os.listdir(CORPUS_PATH):
    if file[-4:] == ".xml":
        tree = ET.parse(f"{CORPUS_PATH}{file}")
        root = tree.getroot()

        cur_seg_dict = dict()
        cur_rel_dict = dict()

        for child in root:
            if child.tag == 'edge':
                if child.attrib['type'] == 'seg':
                    cur_seg_dict[child.attrib['src']] = child.attrib['trg']
                else:
                    cur_rel_dict[child.attrib['src']] = {'trg': child.attrib['trg'], 'type': child.attrib['type']}

        # print(cur_seg_dict)
        # print(cur_rel_dict)

        cur_edus_dict = dict()

        for child in root:
            if child.tag == 'edu':
                cur_edus_dict[child.attrib['id']] = child.text
                cur_adu_id = cur_seg_dict[child.attrib['id']]
                if child.text[0].islower():

                    cur_rel_trg = {}
                    cur_prior_rel = "-"

                    if cur_adu_id in cur_rel_dict:
                        cur_rel_trg = {'type': cur_rel_dict[cur_adu_id]['type'], 'trg': cur_rel_dict[cur_adu_id]['trg']}
                        # print(cur_rel_dict[cur_adu_id])
                        # print(cur_rel_dict[cur_adu_id]['trg'])
                        # print(cur_adu_id)
                        # print(f"a{int(child.attrib['id'][1:])-1}")
                        if cur_rel_dict[cur_adu_id]['trg'] == f"a{int(child.attrib['id'][1:])-1}":
                            # print(cur_rel_dict[cur_adu_id])
                            cur_prior_rel = cur_rel_dict[cur_adu_id]['type']
                            # print(cur_rel)

                    lower_edus.append({'file': f"{file}",
                                       'edu_id': child.attrib['id'],
                                       'adu_id': cur_adu_id,
                                       'text': child.text,
                                       'prior_text': cur_edus_dict[f"e{int(child.attrib['id'][1:])-1}"],
                                       'prior_rel': cur_prior_rel,
                                       'rel': cur_rel_trg})


        # break

        # print(cur_edus_dict)
        # break

# print(f"{len(lower_edus)} EDUs starting with lowercase letter.")

# for lower_edu in lower_edus:
#    print(lower_edu)

first_word_freqs = dict()

for lower_edu in lower_edus:
    # print(lower_edu)
    first_word = lower_edu['text'].split()[0]
    # print(first_word)
    if first_word not in first_word_freqs:
        first_word_freqs[first_word] = {'count': 1, 'where': [{'file': lower_edu['file'],
                                                               'edu_id': lower_edu['edu_id'],
                                                               'adu_id': lower_edu['adu_id'],
                                                               'text': lower_edu['text'],
                                                               'prior_text': lower_edu['prior_text'],
                                                               'prior_rel': lower_edu['prior_rel'],
                                                               'rel': lower_edu['rel']
                                                               }]}
    else:
        first_word_freqs[first_word]['count'] += 1
        first_word_freqs[first_word]['where'].append({'file': lower_edu['file'],
                                                      'edu_id': lower_edu['edu_id'],
                                                      'adu_id': lower_edu['adu_id'],
                                                      'text': lower_edu['text'],
                                                      'prior_text': lower_edu['prior_text'],
                                                      'prior_rel': lower_edu['prior_rel'],
                                                      'rel': lower_edu['rel']
                                                      })

# print(first_word_freqs)

# for first_word, freq in first_word_freqs.items():
#    print(first_word, freq['count'])


def con_prior_rel_check(connective: str, verbose: bool = False):
    con_edus = first_word_freqs[connective]
    # print(f"{con_edus['count']} EDUs starting with '{connective}'.")

    rel_freqs = dict()

    for con_edu_where in con_edus['where']:
        cur_rel = con_edu_where['prior_rel']
        if verbose:
            print(f"{con_edu_where['prior_text']}|{cur_rel}|{con_edu_where['text']}")
        if cur_rel != '-':
            if cur_rel not in rel_freqs:
                rel_freqs[cur_rel] = 1
            else:
                rel_freqs[cur_rel] += 1

    # print(rel_freqs)
    # print(f"Relations to prior ADU: {rel_freqs}")
    print(f"{con_edus['count']} EDUs starting with '{connective}'. Relations to directly preceding ADU: {rel_freqs}")


# for first_word in first_word_freqs:
#    con_prior_rel_check(first_word)

# con_prior_rel_check("but")
# con_prior_rel_check("as")
# con_prior_rel_check("and")

BASIC_CONNECTIVES = ["and", "but", "as", "since", "for", "although", "even"]

# for connective in BASIC_CONNECTIVES:
#    con_prior_rel_check(connective)

for bla in first_word_freqs['although']['where']:
    print(bla)

# for bla in first_word_freqs['and']['where']:
#    print(bla)


def con_all_rel_check(connective: str, verbose: bool = False):
    con_edus = first_word_freqs[connective]
    # print(f"{con_edus['count']} EDUs starting with '{connective}'.")

    rel_freqs = dict()

    for con_edu_where in con_edus['where']:
        cur_rel = con_edu_where['rel']
        if verbose:
            print(f"{con_edu_where['adu_id']} {cur_rel['type']} to {cur_rel['trg']}")

        if cur_rel['type'] not in rel_freqs:
            rel_freqs[cur_rel['type']] = 1
        else:
            rel_freqs[cur_rel['type']] += 1

    # print(rel_freqs)
    # print(f"Relations to prior ADU: {rel_freqs}")
    print(f"{con_edus['count']} EDUs starting with '{connective}'. Relation type counts: {rel_freqs}")


# con_all_rel_check("although", True)
# con_all_rel_check("and", True)

# for connective in BASIC_CONNECTIVES:
#    con_all_rel_check(connective)


def con_rel_dist_check(connective: str, verbose: bool = False):
    con_edus = first_word_freqs[connective]
    # print(f"{con_edus['count']} EDUs starting with '{connective}'.")

    rel_dist_freqs = dict()

    for con_edu_where in con_edus['where']:
        cur_rel = con_edu_where['rel']
        # print(cur_rel)

        # ignore edge-target relations:
        if cur_rel['trg'][0] == "c":
            continue

        # print("self", con_edu_where['adu_id'])
        own_idx = con_edu_where['adu_id'][1:]
        # print(own_idx)
        # print("target", cur_rel['trg'])
        trg_idx = cur_rel['trg'][1:]
        # print(trg_idx)

        distance = int(trg_idx) - int(own_idx)
        # print(distance)

        # if verbose:
        #    print(f"{con_edu_where['adu_id']} {cur_rel['type']} to {cur_rel['trg']}")

        if cur_rel['type'] not in rel_dist_freqs:
            rel_dist_freqs[cur_rel['type']] = dict()

        if distance not in rel_dist_freqs[cur_rel['type']]:
            rel_dist_freqs[cur_rel['type']][distance] = 1
        else:
            rel_dist_freqs[cur_rel['type']][distance] += 1

        # break

    # print(rel_dist_freqs)
    print(f"'{connective}' ADU distance frequency by relation: {rel_dist_freqs}")


# con_rel_dist_check("although", "reb")
# con_rel_dist_check("but", "reb")
# con_rel_dist_check("and", "reb")

# for connective in BASIC_CONNECTIVES:
#    con_rel_dist_check(connective)
