
import util

from bs4 import BeautifulSoup
from datetime import datetime
import lxml
import os

import logging


class URLHarvestResults:

    url_list = ['no_sort', 'none', '0']
    list_header_len = 3

    target = ['no_target', 'none']
    extraction_time = 2
    urls_processed = 3

    def __init__(self):
        pass
        

class Extractor:
    
    def __init__(self, soup, url_list):
        self.soup = soup
        self.url_list = url_list

    def sanitize(self, name):
        """ Removes modifier tags and unnecessary whitespace from the URL name.
            Arguments:
               name (list) = name of URL
            Returns:
               name (str)  = sanitized URL name"""
        i = 0
        while i < len(name):
            if name[i] == '\n':
                name[i] = ''
            if i < len(name) - 1 and name[i] == ' ' and name[i + 1] == ' ':
                name[i] = ''
            else:
                i += 1
        name = ''.join(name)
        return name
    
    def extract(self, tag):

        url_list_offset = len(URLHarvestResults.url_list)
        
        for attribute in self.soup.find_all(tag):
            entry_offset = 0
            entry = list()

            url = str(attribute.get('href'))
            entry.insert(entry_offset, 'URL #' + str(url_list_offset) + ': ' + url)
            entry_offset += 1

            hypertext = attribute.string
            if hypertext != None:
                entry.insert(entry_offset, 'URL/HYPERTEXT: ' + self.sanitize(list(hypertext)))
                entry_offset += 1

            alt = str(attribute.get('alt'))
            if alt != 'None':
                entry.insert(entry_offset, 'URL/ALT: ' + alt)
                entry_offset += 1

            id = str(attribute.get('id'))
            if id != 'None':
                entry.insert(entry_offset, 'URL/ID: ' + id)
                entry_offset += 1

            rel = attribute.get('rel')
            if rel != None:
                # rel is a list
                entry.insert(entry_offset, 'URL/REL: ' + rel[0])
                entry_offset += 1

            img = attribute.find('img')
            if img != None:
                if img.get('src') != None:
                    entry.insert(entry_offset, 'IMG/SRC: ' + str(img.get('src')))
                    entry_offset += 1
                
                if img.get('data-src') != None:
                    entry.insert(entry_offset, 'IMG/DATA-SRC: ' + str(img.get('data-src')))
                    entry_offset += 1

                if img.get('alt') != None:
                    entry.insert(entry_offset, 'IMG/ALT: ' + str(img.get('alt')))
                    entry_offset += 1
                
                class_attr = img.get('class')
                if class_attr != None and str(class_attr) != '[]':
                    # class is a list
                    i = 0
                    while i < len(class_attr):
                        entry.insert(entry_offset, 'IMG/CLASS: ' + str(class_attr[i]))
                        entry_offset += 1
                        i += 1

            self.url_list.insert(url_list_offset, entry)
            url_list_offset += 1
        return

class URLListSorter:
    """ This class holds functions that sort the contents of the URL list that
        URLHarvestResults contains according to category, keyword, or type. """

    sorted_url_list = list()
        
    def __init__(self, url_list):
        self.url_list = url_list
        
    def keyword_sort(self, keyword):
        num_entries_found = 0
        sorted_ul_entry = URLHarvestResults.list_header_len
        ul_entry = URLHarvestResults.list_header_len
        
        URLListSorter.sorted_url_list = ['keystring_sort', keyword, '0']
        
        # Find the entries that contain the keyword, store them first in
        # sorted_url_list, and delete them from the url_list
        while ul_entry < len(self.url_list):
            element = 0
            found = -1
            while element < len(self.url_list[ul_entry]) and found == -1:
                found = self.url_list[ul_entry][element].find(keyword)
                if found != -1:
                    URLListSorter.sorted_url_list.append(self.url_list[ul_entry])
                    del self.url_list[ul_entry]
                    num_entries_found += 1
                    break
                element += 1
            if found == -1:
                ul_entry += 1
        
        # python urlharvest.py ./html_files/cemetech.html -l 22 -k 'forum'
        # Write the number of entries found to the url_list[1]
        URLListSorter.sorted_url_list[2] = str(num_entries_found)
        
        # Add the rest of the entries in the url_list to the sorted_url_list
        ul_entry = URLHarvestResults.list_header_len
        while ul_entry < len(self.url_list):
            URLListSorter.sorted_url_list.append(self.url_list[ul_entry])
            ul_entry += 1
        
        # Put the sorted list into the url_list in URLHarvestResults
        URLHarvestResults.url_list = URLListSorter.sorted_url_list
        return

class ConsoleOutputHandler:

    def __init__(self, args, url_list):
        self.args_all = args.all
        self.args_keystring = args.keystring
        self.args_limit = args.limit
        self.url_list = url_list
    
    def print(self):
    
        # Do not print the rest of the results if a keystring search is active unless
        # specifically instructed to do so by the 'all' flag
        if (self.args_keystring and self.args_all) or self.args_all:
            entry = int(self.url_list[2]) + URLHarvestResults.list_header_len
            
            while entry < len(self.url_list):
                
                # Stop printing if user-imposed limit is reached or there are no more entries
                if entry >= self.args_limit + URLHarvestResults.list_header_len - int(self.url_list[2]):
                    break
                
                print(self.url_list[entry][0])
                element = 1
                while element < len(self.url_list[entry]):
                    print('\t' + str(self.url_list[entry][element]))
                    element += 1
                entry += 1
        
        # If requested, print search results
        if self.url_list[0] != 'no_sort':
            entry = URLHarvestResults.list_header_len
            
            if self.url_list[0] == 'keystring_sort':
                print('\n' + self.url_list[2] + ' search result(s) matching \'' + self.url_list[1] + '\':\n-----------------------------------------------------------------')
            
            while entry < int(self.url_list[2]) + URLHarvestResults.list_header_len and entry < self.args_limit + URLHarvestResults.list_header_len:
                print(self.url_list[entry][0])
                element = 1
                while element < len(self.url_list[entry]):
                    print('\t' + str(self.url_list[entry][element]))
                    element += 1
                entry += 1
            
            print('-----------------------------------------------------------------\n')
        return

class FileOutputHandler:
    
    def __init__(self, target, url_list):
        self.target = target
        self.url_list = url_list
    
    def create_file_name(self):
        if self.target.startswith('http'):
            file_name = self.target[self.target.find('//') + 2:]
        else:
            file_name = self.target[self.target.rfind('/') + 1:]
        file_name = file_name.replace('.', '_')
        file_name = file_name.replace('/', '_')
        file_name = file_name + '_URLHarvest.txt'
        return file_name
    
    def write_header(self, file_name):
        try:
            results_file = open(file_name, 'w')
            results_file.writelines('URLHarvest v1.0' + ' by JadeScout\nDate generated: ' + str(datetime.now()) + '\nTarget: ' + URLHarvestResults.target[0] + '\n')
            if not util.is_valid_file(URLHarvestResults.target[0]):
                results_file.writelines('IP Address: ' + URLHarvestResults.target[1] + '\n')
            results_file.writelines('URLs Processed: ' + URLHarvestResults.target[URLHarvestResults.urls_processed] + '\nExtraction Time: ' + URLHarvestResults.target[URLHarvestResults.extraction_time] + ' seconds\n\n')
            return results_file
        except FileNotFoundError:
            util.print_error('Could not create results file: ' + file_name)
            return None
    
    def create_file(self):
        file_name = self.create_file_name()
        results_file = self.write_header(file_name)
        
        entry = URLHarvestResults.list_header_len
        if self.url_list[0] == 'keystring_sort':
            results_file.writelines('\n' + self.url_list[2] + ' search result(s) matching \'' + self.url_list[1] + '\':\n-----------------------------------------------------------------\n')
        
        while entry < len(self.url_list):
            element = 0
            while element < len(self.url_list[entry]):
                line = ''
                if element > 0:
                    line = '\t'
                results_file.write(line + str(self.url_list[entry][element]) + '\n')
                element += 1
            entry += 1
            
            if entry - URLHarvestResults.list_header_len == int(self.url_list[2]):
                results_file.writelines('-----------------------------------------------------------------\n\n')
            
        results_file.close()
        util.print_info('Finished writing results file: ' + file_name)
        return

def report_tool_performance(extracted_url_list, start_time, end_time):

    URLHarvestResults.target.insert(2, str(round(end_time - start_time, 4)))
    URLHarvestResults.target.insert(3, str(len(extracted_url_list) - URLHarvestResults.list_header_len))

    print('')
    util.print_info('Extraction Time: ' + URLHarvestResults.target[2] + ' seconds')
    util.print_info('URLs Processed: ' + URLHarvestResults.target[3])
    return
