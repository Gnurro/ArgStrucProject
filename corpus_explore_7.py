""" Checking for JOINTs """

import xml.etree.ElementTree as ET
import os


CORPUS_PATH = "corpus/en/"

tag_set = set()

for file in os.listdir(CORPUS_PATH):
    if file[-4:] == ".xml":
        with open(f"{CORPUS_PATH}{file}", 'r', encoding='utf-8') as raw_file:
            cur_file = raw_file.read()
            print(cur_file)

        if "joint" in cur_file:
            print(cur_file)
