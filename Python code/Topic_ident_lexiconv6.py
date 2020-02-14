"""
Author: Sam Jackson
Thanks to Nancy McCracken for assistance.

This file uses a lexicon to identify topics and document features based on keywords in documents.

The lexicon should be xml-formatted, with top categories, sub categories, and keywords.

The script builds two dictionaries out of this lexicon: one contains unigrams, the other contains (n>=2)grams. It tests
 the items in the unigram dictionary differently than the items in the ngram dictionary.
Both dictionaries are sorted alphabetically first by main topic, then by subtopic.

The script creates an output csv file. It initially writes a header line, then a line for each input file (described
 below). This csv file can be exported as an excel file, then filtered as needed.

The script recursively searches through a specified directory for .html files and .txt files to tag based on the
 lexicon.
 The script is built around the directory structure for this project, which has subfolders for the OK main site, the OK
  blog, Rhodes's blog, and video transcripts.
  If a file is an html file, the script uses BeautifulSoup to extract text from specified div classes.
  If a file is an html file, the script extracts all text except where lines begin with '##'.

The script looks for matches in the unigram dictionary and the ngram dictionary in each file, working through topics
 alphabetically and subtopics alphabetically.
 The script looks to match unigram dictionary entries against tokens in the text for each file. It only identifies
  unigrams that are exact matches. This allows me to include acronyms and other short strings in my lexicon without
  getting false positives where those short strings appear in the middle of words.
 The script looks to find ngram dictionary entries as strings in the text for each file. Thus, partial word matches are
  possible.

The script writes a line of output for each input file. That line contains the site that contained the file, the file
 name, and a cell for each topic:subtopic. If a subtopic does not appear in a file, that file has a blank cell for that
 subtopic. If a subtopic does appear in a file, that file has a cell containing the lexicon entries for that subtopic in
 the cell corresponding to that subtopic.

This script only works with .txt files. To run on Word files, must save them as plain text files: BE SURE TO ENCODE WITH
 UTF-8 OR IT WON'T WORK.
"""

import xml.etree.ElementTree as ET
import os
import datetime
from bs4 import BeautifulSoup
import nltk
import csv

now = datetime.datetime.now()
timestr = now.isoformat()

xml_doc = '../PM_lexicon.txt'

tree = ET.parse(xml_doc)
root = tree.getroot()

unigramtopic_dict = {}
ngramtopic_dict = {}
full_category_list = []
top_category_list = []

# This for loop builds the unigram and ngram dictionaries that will identify topics
for child in root:
    f = child.get('name')
    unigram_child_dict = {}
    ngram_child_dict = {}
    top_category_list.append(f)
    for subcat in child:
        subcat_name = subcat.get('name')
        full_category_list.append(subcat_name)
        unigram_key_list = []
        ngram_key_list = []
        for key in subcat:
            key_name = key.get('name')
            if ' ' in key_name or '-' in key_name:
                ngram_key_list.append(key_name)
            if not ' ' in key_name and not '-' in key_name:
                unigram_key_list.append(key_name)
        unigram_child_dict[subcat_name] = unigram_key_list
        ngram_child_dict[subcat_name] = ngram_key_list
        unigramtopic_dict[f] = unigram_child_dict
        ngramtopic_dict[f] = ngram_child_dict

# The following lines generate a list of subcategories. This list is first sorted alphabetically by top category, then
#  the subcategories for each top category are also sorted alphabetically. This generates the list to iterate across the
#  dictionary below.
subtopics = []
main_topics = sorted(top_category_list)
for topic in main_topics:
    subtopic_list = []
    if topic in unigramtopic_dict:
        subtopic = unigramtopic_dict[topic]
        for value in subtopic:
            subtopic_list.append(value)
    subtopic_list = sorted(subtopic_list)
    for s in subtopic_list:
        subtopics.append(s)

# In the next line, indicate directory to start searching for input files
start_path = '../data'
os.chdir(start_path)

output_file_cats = start_path + '/categories.csv'

with open(output_file_cats, 'w') as output_file_cats:
    wr = csv.writer(output_file_cats, delimiter = ',', quoting = csv.QUOTE_MINIMAL)
    header_line = []
    header_line.extend(('path', 'site', 'title'))
    for t in subtopics:
        for f in unigramtopic_dict:
            subcats = unigramtopic_dict[f]
            if t in subcats:
                header_line.append(f + ': ' + t)
    wr.writerow(header_line)
    for path, subdirs, files in os.walk(start_path):
        for f in files:
            site = ''
            f_abs_path = path + '/' + f
            if 'OK_site' in f_abs_path:
                site = 'OK_site'
            if 'OK_blog' in f_abs_path:
                site = 'OK_blog'
            if 'Rhodes_blog' in f_abs_path:
                site = 'Rhodes_blog'
            if 'video_transcripts' in f_abs_path:
                site = 'video_transcripts'

            if f.endswith('.html'):
                soup = BeautifulSoup(open(f_abs_path, 'r', encoding='utf-8'),'lxml')
                text_output = soup.find_all('div', {'class': 'panel'})
                input_file_contents = ''
                for item in text_output:
                    input_file_contents += item.text
                text_output = soup.find_all('div', {'class': 'post-body entry-content'})
                for item in text_output:
                    input_file_contents += item.text
                tokened_text = nltk.word_tokenize(input_file_contents)


                ## Loop through dictionary, check if keywords appear in input_file.
                category_list = []
                for s in subtopics:
                    keyword_list = []
                    for t in unigramtopic_dict:
                        subcats = unigramtopic_dict[t]
                        if s in subcats:
                            keyword2 = subcats[s]
                            category_appears = False
                            for key in keyword2:
                                for t in tokened_text:
                                    if t == key:
                                        category_appears = True
                                        keyword_list.append(key)
                    for t in ngramtopic_dict:
                        subcats = ngramtopic_dict[t]
                        if s in subcats:
                            keyword2 = subcats[s]
                            for key in keyword2:
                                if key in input_file_contents:
                                    category_appears = True
                                    keyword_list.append(key)
                    if category_appears == True:
                        keyword_list = list(set(keyword_list))
                        category_list.append(', '.join(keyword_list))
                    else:
                        category_list.append('')

                print_line = []
                split_path = os.path.split(f_abs_path)
                print_line.append(split_path[0])
                print_line.append(site)
                print_line.append(split_path[1])
                for cat in category_list:
                    print_line.append(cat)
                wr.writerow(print_line)

            if f.endswith('.txt'):
                input_file = open(f_abs_path, 'r', encoding='utf-8')
                input_file_contents = ''
                for line in input_file:
                    line = input_file.readline()
                    if not line.startswith('##'):
                        input_file_contents += line
                lower_text = input_file_contents.lower()
                tokened_text = nltk.word_tokenize(lower_text)
                category_list = []

                ## Loop through dictionary, check if keywords appear in input_file
                for s in subtopics:
                    keyword_list = []
                    for t in unigramtopic_dict:
                        subcats = unigramtopic_dict[t]
                        if s in subcats:
                            keyword2 = subcats[s]
                            category_appears = False
                            for key in keyword2:
                                for t in tokened_text:
                                    if t == key:
                                        category_appears = True
                                        keyword_list.append(key)
                    for t in ngramtopic_dict:
                        subcats = ngramtopic_dict[t]
                        if s in subcats:
                            keyword2 = subcats[s]
                            for key in keyword2:
                                if key in input_file_contents:
                                    category_appears = True
                                    keyword_list.append(key)
                    if category_appears == True:
                        keyword_list = list(set(keyword_list))
                        category_list.append(', '.join(keyword_list))
                    else:
                        category_list.append('')

                print_line = []
                split_path = os.path.split(f_abs_path)
                print_line.append(split_path[0])
                print_line.append(site)
                print_line.append(split_path[1])
                for cat in category_list:
                    print_line.append(cat)
                wr.writerow(print_line)


output_note = start_path + '/note.txt'
with open(output_note, 'w+') as output_note:
    note_output = 'Categories generated ' + timestr
    output_note.write(note_output)