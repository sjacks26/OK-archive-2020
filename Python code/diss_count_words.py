"""
Author: Sam Jackson
Thanks to Nancy McCracken for assistance.

This script is based on Topic_ident_lexiconv6.py
"""

import os
import datetime
from bs4 import BeautifulSoup
import nltk

now = datetime.datetime.now()
timestr = now.isoformat()


# In the next line, indicate directory to start searching for input files
start_path = '../data/'
os.chdir(start_path)

docs_wordcounts = {}
total_words = 0

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
        if 'SipseyStreet' in f_abs_path:
            site = 'Sipsey Street'

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
            doc_word_count = len(tokened_text)
            docs_wordcounts[f] = doc_word_count
            total_words += doc_word_count

        if f.endswith('.txt'):
            input_file = open(f_abs_path, 'r', encoding='utf-8')
            input_file_contents = ''
            for line in input_file:
                line = input_file.readline()
                if not line.startswith('##'):
                    input_file_contents += line
            lower_text = input_file_contents.lower()
            tokened_text = nltk.word_tokenize(lower_text)
            doc_word_count = len(tokened_text)
            docs_wordcounts[f] = doc_word_count
            total_words += doc_word_count
