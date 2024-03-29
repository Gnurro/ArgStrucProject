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
in more detail. The script can be run to show the calculated statistics.  
`unit_checking.py` contains functions to identify split, sub-clause text units and anaphora, as well as some utility 
functions. While attempts to use these for automation were abandoned, this script provides further insight into the 
corpus. The script can be run to show the various features examined.  
`unit_bigram_ex.py` contains an experimental attempt at identifying inseparable unit bigrams, which was soon abandoned 
as it showed that the corpus data is too inconsistent to automate this. The script can be run to show the exploration 
for a single text (b001).  
### Text editing utilities
`shuffle_test.py` contains an attempt to automatically produce all linear order variants of a corpus text. This was 
abandoned in favor of manual inspection and preliminary exclusion of non-viable order variants. The script can be run to 
show the indiscriminately shuffled variants of a single text (b009).  
`editing_util.py` contains an utility function to quickly create plain text files with units separated into lines and 
annotations of unit indices and unit stances. These plain text files are to be used for manual rearrangement and editing. 
The script can be run to show the resulting format and reproduce the first step of the editing procedure for the survey. 
### Survey script
`survey_util.py` contains all functions used to prepare the survey and to process the raw survey replies.  
`survey_util.py` can be run to reproduce the preparation and result processing for the survey.
#### Survey script functions
Much of this script relies on raw text files that list corpus text IDs, with IDs separated by newline in the files. The 
`read_texts_list()` function reads these files and returns them as `list`.  
The functions `copy_original_texts()` and `copy_edited_texts()` are used to conveniently copy original text files from
the corpus and edited text files to the survey directories for further use.  
`survey_texts_info()` is used check the balance of originally claim-first and -last texts to be used for the survey, 
based on manually created text list files. It also provides information about the topics and main stances of the listed 
texts. `survey_texts_frequencies()` expresses the information from the former function as a `dict` of counts.  
`get_original_first()` and `get_original_last()` are utility functions used to conveniently get `list`s of text IDs 
based on their original order being claim-first or -last.  
As there were more originally claim-first texts in our initial selection of texts to edit, `create_balanced_text_list()` 
was used to assure that a selected subset of these texts stored as a text ID list file correctly matches the number of 
originally claim-last files to be edited. It also saves a text ID list file to disk when the selection is balanced.  
`build_survey_pairs()` creates a `dict` containing both the original texts and their edited versions for further 
processing. `survey_processing_pairs()` creates a similar `dict`, but also contains the number of each text on the 
survey form and table data retrieved after the survey period.  
`pairs_to_csv()` creates a CSV file with the pairs of edited and unedited texts used in the survey.  
`pairs_to_simple_list()` creates a plain text file with the pairs of edited and unedited texts, ordered as to be 
presented on the survey form. The format in the saved file allows for convenient copying of the text pairs into the 
Google Forms editing interface for quick addition of choices.  
`process_survey_answers()` processes the retrieved raw survey data from CSV to a boolean format for further processing 
and analysis. Result is returned as Pandas DataFrame.  
`survey_cross_counts()` uses the processed survey data to count participant choices, separated by edited/unedited and 
claim-first/-last. Result is returned as Pandas DataFrame.  

