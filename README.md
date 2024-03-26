# Exploring linear order effects based on data of the Potsdam Argumentative Microtext corpus
This repository accompanies the semester project by M. Sideri and J. Jordan for the project module course 'Mining Opinions and Argument' 
held at the University of Potsdam in the winter semester 2023/24.
## Content
Edited texts are located in the `editing` directory, separated into subdirectories by annotator. The individual 
subdirectories also contain plain text files listing text IDs of texts used for the survey.  
Prepared survey data, and raw and processed survey replies are located in the `survey` directory.
## Setup
### Corpus
This project requires the [Potsdam Argumentative Microtext Corpus](https://angcl.ling.uni-potsdam.de/resources/argmicro.html).  
The required corpus files are available at https://github.com/peldszus/arg-microtexts.  
Download the `corpus` directory found in the linked repository and place it in the root directory of this project.  
This project's code is written with the assumption that the corpus data accessible under the path `corpus/`.
### Requirements
Python library requirements are listed in `requirements.txt`.
## Scripts
### Corpus extraction
As the first step, run `corpus_extractor.py`. This script extracts various information from the corpus and creates a 
JSON file, `extracted_db.json`, allowing easy access to this information for further use. Among others, it contains 
abstracted linearization strategies (as described in [Peldszus & Stede 2015](https://peldszus.github.io/files/eca2015-preprint.pdf)), 
central claim positions and argGraph node depths. See comments in `corpus_extractor.py` for specifics.  

All further scripts use `extracted_db.json`.
### Corpus Exploration
`corpus_stats.py` calculates and prints various frequency statistics, mainly reproducing those presented in [Peldszus & Stede 2015](https://peldszus.github.io/files/eca2015-preprint.pdf).  
`by_stance.py` calculates linearization strategy statistics, separated by text main stance, reproducing [Peldszus & Stede 2015](https://peldszus.github.io/files/eca2015-preprint.pdf) 
in more detail.  
`unit_checking.py` contains functions to identify split, sub-clause text units and anaphora, as well as some utility 
functions. While attempts to use these for automation were abandoned, this script provides further insight into the 
corpus.  
`unit_bigram_ex.py` contains an experimental attempt at identifying inseparable unit bigrams, which was soon abandoned 
as it showed that the corpus data is too inconsistent to automate this.  
### Text editing utilities
`shuffle_test.py` contains an attempt to automatically produce all linear order variants of a corpus text. This was 
abandoned in favor of manual inspection and preliminary exclusion of non-viable order variants.  
`editing_util.py` contains an utility function to quickly create plain text files with units separated into lines and 
annotations of unit indices and unit stances. These plain text files are to be used for manual rearrangement and editing.
### Survey scripts
`survey_util.py` contains all functions used to prepare the survey and to process the raw survey replies.  
TODO: explain the parts and steps, as it's a lot