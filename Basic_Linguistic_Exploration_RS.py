#!/usr/bin/env python
# coding: utf-8

# In[19]:


import os
import re
import xml.etree.ElementTree as ET
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk import sent_tokenize



# Specify the folder path containing your XML files
folder_path = 'C:\\Users\\myrto\\CorpusRS'

# List to store all text content from the corpus
all_text_content = []

#pronouns
extracted_pronouns=[]

pronoun_pattern= r'\b(he|she|it|they|him|her|them|his|hers|its|theirs)\b'

#List to store POS tagged tokens
#all_pos_tags = []

#stance types
stance_counts= {'pro':0, 'opp':0, 'unclear':0}

#frequency of arg.types and subtypes

argument_counts={'type':{'pro':0, 'opp':0, 'unclear':0}, 'subtype':{'seg': 0, 'sup': 0, 'exa': 0, 'add': 0, 'reb': 0, 'und': 0}} 

# Iterate over each file in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".xml"):
        xml_file_path = os.path.join(folder_path, filename)

        # Parse the XML file
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
        
        stance = root.get('stance')
        
        if stance in stance_counts:
            stance_counts[stance] +=1

        # Process each edu element and extract text content
        for edu_element in root.findall('.//edu'):
            edu_text = edu_element.text
            if edu_text:
                all_text_content.append(edu_text)
                pronouns = re.findall(pronoun_pattern, edu_text, re.IGNORECASE)
                extracted_pronouns.extend(pronouns)

#print(extracted_pronouns)
#print(stance_counts)


# In[ ]:





# In[10]:


# Combine all text content into a single string
corpus_text = ' '.join(all_text_content)

# Tokenize the text
tokens = word_tokenize(corpus_text)
#print(tokens)

# Remove stopwords
stop_words = set(stopwords.words('english'))
filtered_tokens = [word.lower() for word in tokens if word.isalnum() and word.lower() not in stop_words]
#print(filtered_tokens)

# Calculate word frequencies
fdist = FreqDist(tokens)
#print(fdist)


# In[11]:


# Access the most common words and their frequencies
common_words = fdist.most_common(20)
#print(common_words)


# In[ ]:





# In[ ]:




