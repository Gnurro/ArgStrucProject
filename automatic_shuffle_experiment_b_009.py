#!/usr/bin/env python
# coding: utf-8

# In[6]:


import json
from random import shuffle

def shuffle_argument_components(json_data, num_variants=1):
    original_components = json_data["arggraph"]["components"]
    all_variants = []

    for _ in range(num_variants):
        shuffled_components = original_components.copy()
        shuffle(shuffled_components)

        for idx, component in enumerate(shuffled_components):
            component["id"] = f'{component["type"][0]}{idx + 1}'

        all_variants.append({"arggraph": {"id": json_data["arggraph"]["id"], "components": shuffled_components}})

    return all_variants

# Example text micro_b009 
corpus_json_data = [
    {
        "arggraph": {
            "id": "micro_b009",
            "topic_id": "cap_rent_increases",
            "stance": "pro",
            "components": [
                {"type": "edu", "id": 'e1', "text": "It is unfair and unjustifiable that new tenants have to pay a much higher rent than previous residents."},
                {"type": "edu", "id": 'e2', "text": "Clearly the landlord has to pay for some repairs before a new lease."},
                {"type": "edu", "id": 'e3', "text": "But surely these costs could be covered by a minimal increase in rent over the course of the entire lease."},
                {"type": "edu", "id": 'e4', "text": "All the more so as for an adequate profit the rental rate as compared to the base rent need not be raised for every new lease."},
                {"type": "adu", "id": 'a1', "type_attr": "pro"},
                {"type": "adu", "id": 'a2', "type_attr": "opp"},
                {"type": "adu", "id": 'a3', "type_attr": "pro"},
                {"type": "adu", "id": 'a4', "type_attr": "pro"},
            ],
            "edges": [
                {"id": "c5", "src": "e1", "trg": "a1", "type": "seg"},
                {"id": "c6", "src": "e2", "trg": "a2", "type": "seg"},
                {"id": "c7", "src": "e3", "trg": "a3", "type": "seg"},
                {"id": "c8", "src": "e4", "trg": "a4", "type": "seg"},
                {"id": "c2", "src": "a2", "trg": "a1", "type": "reb"},
                {"id": "c3", "src": "a3", "trg": "c2", "type": "und"},
                {"id": "c4", "src": "a4", "trg": "a1", "type": "sup"},
            ],
        }
    },
    
]

num_variants_per_text = 6  

for idx, json_data in enumerate(corpus_json_data):
    print(f"Original Text {idx + 1}:\n{json_data['arggraph']['components']}\n")

    shuffled_variants = shuffle_argument_components(json_data, num_variants=num_variants_per_text)

    for variant_idx, variant_data in enumerate(shuffled_variants):
        shuffled_components = variant_data['arggraph']['components']
        print(f"Shuffled Variant {variant_idx + 1}:\n{shuffled_components}\n{'=' * 40}")

       
        # with open(f"shuffled_corpus_{idx + 1}_variant_{variant_idx + 1}.json", "w", encoding="utf-8") as json_file:
        #     json.dump(variant_data, json_file, ensure_ascii=False, indent=2)


# In[8]:


# ...

for idx, json_data in enumerate(corpus_json_data):
    print(f"Original Text {idx + 1}:\n")
    for component in json_data['arggraph']['components']:
        component_id = component.get('id', '')
        component_type = component.get('type', '')
        component_text = component.get('text', '')
        print(f"    {component_id} ({component_type}): {component_text}")

    print("\nShuffled Variants:")
    shuffled_variants = shuffle_argument_components(json_data, num_variants=num_variants_per_text)

    for variant_idx, variant_data in enumerate(shuffled_variants):
        shuffled_components = variant_data['arggraph']['components']
        print(f"\nVariant {variant_idx + 1}:\n")
        for component in shuffled_components:
            component_id = component.get('id', '')
            component_type = component.get('type', '')
            component_text = component.get('text', '')
            print(f"    {component_id} ({component_type}): {component_text}")
        
        print('-' * 40)

       


# In[ ]:




