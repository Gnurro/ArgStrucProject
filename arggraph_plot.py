import json
import graphviz


# load database:
with open("extracted_db.json", 'r', encoding='utf-8') as db_file:
    database: dict = json.load(db_file)

text = database['b002']
# print(text)

graph = graphviz.Digraph('arg_graph', comment='Argument Graph')

for relation in text['relations']:
    # print(relation, text['relations'][relation])
    graph.node(relation, f"[{relation}] {text['relations'][relation]['type']}")

n_units = len(text['units'])

for unit in text['units']:
    # print(unit)
    # print(unit['rel']['trg'])
    # graph.node(unit['adu_id'], f"[{unit['edu_id']}] {unit['text'][:20]}", shape="box", ordering="out")
    graph.node(unit['adu_id'], f"[{unit['edu_id']}] {unit['text'][:20]}", shape="box", ordering="in")
    # if unit['rel']:
    #    graph.edge(unit['adu_id'], unit['rel']['trg'], label=unit['rel']['type'])
    if int(unit['adu_id'][1:]) < n_units:
        # graph.edge(unit['adu_id'], f"a{int(unit['adu_id'][1:]) + 1}")
        graph.edge(unit['adu_id'], f"a{int(unit['adu_id'][1:]) + 1}", style="invisible", arrowhead="none")
    # if unit['adu_id'][1:] != "1":
        # graph.edge(unit['adu_id'], f"a{int(unit['adu_id'][1:])+1}", style="invisible")
        # graph.edge(unit['adu_id'], f"a{int(unit['adu_id'][1:])+1}")

for rel_id, rel_content in text['relations'].items():
    print(rel_id, rel_content)
    graph.edge(rel_content['src'], rel_id, arrowhead="none")
    graph.edge(rel_id, rel_content['trg'])

graph.render()

"""
dot = graphviz.Digraph('round-table', comment='The Round Table')

dot.node('A', 'King Arthur')
dot.node('B', 'Sir Bedevere the Wise')
dot.node('L', 'Sir Lancelot the Brave')

dot.edges(['AB', 'AL'])
dot.edge('B', 'L', constraint='false', label="bops")

dot.render()
"""