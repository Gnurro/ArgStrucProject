#!/usr/bin/env python
# coding: utf-8

# In[2]:


import os
import xml.etree.ElementTree as ET
from lxml import etree


# In[3]:


# Specify the folder path containing your XML files
folder_path = 'C:\\Users\\myrto\\CorpusRS'

# Create an empty list to store parsed XML data
xml_data = []

# Iterate over each file in the folder

for filename in os.listdir(folder_path):
    if filename.endswith(".xml"):
        file_path = os.path.join(folder_path, filename)
        
        # Parse the XML file
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        # Append the parsed XML data to the list
        xml_data.append(root)


# In[6]:


def validate_xml(xml_file, xsd_file):
    schema = etree.XMLSchema(etree.parse(xsd_file))
    xml_parser = etree.XMLParser(schema=schema)

    try:
        etree.parse(xml_file, xml_parser)
        return True  # XML is valid against the schema
    except etree.XMLSyntaxError as e:
        print(f"Error in XML file {xml_file}: {e}")
        return False

# Specify the folder path containing your XML files
folder_path = 'C:\\Users\\myrto\\CorpusRS'

# Specify the path to your XML schema file
xsd_file = 'C:\\Users\\myrto\\CorpusRS'

# Iterate over each file in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".xml"):
        xml_file_path = os.path.join(folder_path, filename)

        # Validate XML against the schema
        if validate_xml(xml_file_path, xsd_file):
            print(f"XML file {filename} is valid against the schema.")

            # Analyze the XML content
            analyze_xml(xml_file_path)
        else:
            print(f"XML file {filename} is not valid against the schema.")


# In[12]:


import os
import xml.etree.ElementTree as ET

# Specify the folder path containing your XML files
folder_path = 'C:\\Users\\myrto\\CorpusRS'

# Iterate over each file in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".xml"):
        xml_file_path = os.path.join(folder_path, filename)

        # Parse the XML file
        tree = ET.parse(xml_file_path)
        root = tree.getroot()

        # Iterate over elements in the XML tree
        for element in root.iter():
            # Check if the element represents an edge
            if element.tag == 'edge':
                edge_type = element.get('type', '').lower()
                source_node = element.get('src', '')
                target_node = element.get('trg', '')

                # Check for deviations from the XML definition
                if edge_type == 'add' and 'sup' in target_node:
                    print(f"Warning: 'add' edge connected to 'sup' node in {filename}")
                elif edge_type == 'reb':
                    print(f"Warning: 'reb' edge found in {filename}")


# In[8]:


# Specify the folder path containing your XML files
folder_path = 'C:\\Users\\myrto\\CorpusRS'

# Iterate over each file in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".xml"):
        xml_file_path = os.path.join(folder_path, filename)

        # Parse the XML file
        tree = ET.parse(xml_file_path)
        root = tree.getroot()

        # Identify ADU elements 
        adu_elements = root.findall('.//adu')

        # Iterate over elements in the XML tree
        for element in root.iter():
            # Check if the element represents an "add" edge
            if element.tag == 'edge' and element.get('type', '').lower() == 'add':
                source_node = element.get('src', '')
                target_node = element.get('trg', '')

                # Check if the connected nodes are ADUs
                if source_node in adu_elements and target_node in adu_elements:
                    print(f"'add' edge between ADUs found in {filename}")


# In[ ]:




