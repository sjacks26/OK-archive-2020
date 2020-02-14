'''
First, this script removes a problematic bit of javascript from OK website pages. Then, it removes the header, footer, and sidebar from Oath Keepers pages. It creates a new output file with the input file's contents minus the header, footer, and sidebar. This new output includes a meta content tag to ensure proper rendering.

This script does not need to be run. It is in this archive for reference only.
'''

import re
from bs4 import BeautifulSoup
import os
import datetime

# Create variable to create directory with timestamp
now = datetime.datetime.now()
timestr = now.isoformat()
path_out = os.path.join('../data/fixed' + timestr)


# Top directory with files and subdirs to parse
start_path = '../data/'
os.chdir(start_path)

# Regex pattern, used to identify the problematic script to remove. Also used to identify header, footer, and
#  comments elements of pages.
full_header = re.compile("(<!-- Really Simple)(.|\n)*?(</head>)")
broken_header = re.compile("(<script>)(.|\n)*?(document\.URL\.replace)(.|\n)*?(</script>)")
footer_sidebar = re.compile("(<h2>Related Articles</h2>)(.|\n)*?(</html>)")
footer2_sidebar = re.compile("(<!-- END .panel  -->)(.|\n)*?(</html>)")
comments = re.compile("(<div class=\"comments-block\">)(.|\n)*?(<!-- END \.comments-block -->)(.|\n)*?(</div>)")

# Loop to identify html files, parse with BeautifulSoup
for path, subdirs, files in os.walk(start_path):
    os.makedirs(path_out + path.replace(start_path, ''))
    for f in files:
        if f.endswith('.html'):
            # Open each input html file, parse with BeautifulSoup
            f_abs_path = path + '/' + f

            # Create output file for each input file
            output_file_name = f_abs_path.replace(start_path, path_out)
            output_file_dir = os.path.dirname(output_file_name)
            output_file_dir_base = os.path.basename(output_file_dir)
            output_file_name = output_file_name.replace('/index', '')
            try:
                os.mkdir(os.path.dirname(os.path.dirname(output_file_name)))
            except:
                pass
            new_f_file = open(output_file_name, 'w+')

            # Soup the file
            try:
                soup = BeautifulSoup(open(f_abs_path, 'r', encoding='utf-8'), 'lxml')
                soup_string = str(soup)

                # This first try loop specifically targets the problematic script
                try:
                    # Look for broken header regex pattern, create a string variable containing all the characters to remove
                    broken_header_occurrences = broken_header.search(soup_string)
                    start_index = broken_header_occurrences.pos
                    end_index = broken_header_occurrences.endpos
                    span = broken_header_occurrences.span()
                    remove_this = soup_string[span[0]:span[1]]

                    soup_string = soup_string.replace(remove_this,'')

                except:
                    soup_string = soup_string

                # Try loops skips files that don't match the regex pattern
                try:
                    # Look for full header regex pattern, create a string variable containing all the characters to remove
                    full_header_occurrences = full_header.search(soup_string)
                    span = full_header_occurrences.span()
                    remove_this = soup_string[span[0]:span[1]]

                    # Create new string, consisting of the old html file contents with the regex pattern match removed
                    new_html = soup_string.replace(remove_this, '')

                except:
                    new_html = soup_string

                try:
                    # Look for footer and sidebar regex pattern, create a string variable containing all the characters to remove
                    footer_sidebar_occurrences = footer_sidebar.search(soup_string)
                    span = footer_sidebar_occurrences.span()
                    remove_this = soup_string[span[0]:span[1]]

                    # Create new string, consisting of the old html file contents with the regex pattern match removed
                    new_html = new_html.replace(remove_this,'')

                except:
                    new_html = new_html

                try:
                    footer2_sidebar_occurrences = footer2_sidebar.search(soup_string)
                    span = footer_sidebar_occurrences.span()
                    remove_this = soup_string[span[0]:span[1]]
                    new_html = new_html.replace(remove_this,'')

                except:
                    new_html = new_html

                try:
                    soup2 = BeautifulSoup(new_html, 'lxml')
                    section = soup2.find_all('div', {'class': 'comments'})
                    for string in section:
                        coding = str(string)
                    new_html = new_html.replace(coding,'')

                except:
                    new_html = new_html

                try:
                    soup2 = BeautifulSoup(new_html, 'lxml')
                    section = soup2.find_all('div', {'class': 'comments-block'})
                    for string in section:
                        coding = str(string)
                    new_html = new_html.replace(coding,'')

                except:
                    new_html = new_html

                try:
                    soup2 = BeautifulSoup(new_html, 'lxml')
                    section = soup2.find_all('div', {'class': 'lightbox'})
                    for string in section:
                        coding = str(string)
                    new_html = new_html.replace(coding,'')

                except:
                    new_html = new_html

                try:
                    soup2 = BeautifulSoup(new_html, 'lxml')
                    section = soup2.find_all('div', {'id': 'responsive-menu'})
                    for string in section:
                        coding = str(string)
                    new_html = new_html.replace(coding,'')

                except:
                    new_html = new_html

                try:
                    soup2 = BeautifulSoup(new_html, 'lxml')
                    section = soup2.find_all('div', {'class': 'widget'})
                    for string in section:
                        coding = str(string)
                        new_html = new_html.replace(coding, '')

                except:
                    new_html = new_html

                try:
                    soup2 = BeautifulSoup(new_html, 'lxml')
                    section = soup2.find_all('ul', {'class': 'menu menu'})
                    for string in section:
                        coding = str(string)
                        new_html = new_html.replace(coding, '')
                except:
                    new_html = new_html


                try:
                    soup2 = BeautifulSoup(new_html, 'lxml')
                    section = soup2.find_all('ul', {'class': 'social-buttons left'})
                    for string in section:
                        coding = str(string)
                        new_html = new_html.replace(coding, '')
                except:
                    new_html = new_html

                '''
                try:
                    new_html = new_html.replace('â€TM', '')
                except:
                    new_html = new_html
                '''

            except:
                new_html = 'BeautifulSoup error'

            # Write new string to html file. The meta content tag ensures proper rendering of special characters like "
            new_html2 = '<meta content="text/html; charset=utf-8" http-equiv="content-type"/> \n' + new_html
            new_f_file.write(new_html2)
            new_f_file.close()