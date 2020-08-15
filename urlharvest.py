import core
import util

import argparse
from bs4 import BeautifulSoup
import socket
import sys
import time
from urllib.request import urlopen

def print_program_info():
    
    print('\n')
    print('=================================================================')
    print('|  URLHarvest                                                   |')
    print('|  Version: 1.0                                                 |')
    print('|  By: JadeScout                                                |')
    print('=================================================================')
    print('\n')
    return;

def start_extractor():
    
    parser = argparse.ArgumentParser(description = 'URLHarvest is a simple Web scraper that extracts URLs from webpages.')
    parser.add_argument('-a', '--all', help = 'print all URLs found', action = 'store_true')
    parser.add_argument('-k', '--keystring', help = 'print only the URL entries whose URLs or attributes contain KEYSTRING')
    parser.add_argument('-l', '--limit', help = 'maximum number of URL entries to print. default = 200', default = 200, type = int)
    parser.add_argument('-p', '--print', help = 'print results to .txt file', action = 'store_true')
    parser.add_argument('target', help = 'target URL or path to target file')
    
    args = parser.parse_args()
    
    if not args.keystring:
        args.all = True
    
    # Initialize the results lists
    results = core.URLHarvestResults()
    results.target[0] = args.target
    
    if util.is_valid_file(args.target):
        try:
            html = open(args.target, 'r')
        except FileNotFoundError:
            util.print_error('File not found')
            sys.exit(1)
    else:
        if util.is_valid_url(args.target):
            print(args.target[args.target.find('.', 1) + 1:])
            util.print_info('Connecting to ' + args.target + ' (' + results.target[1] + ')')
            
            # Write the IP address of the target to the URLHarvestResults.target list
            results.target[1] = socket.gethostbyname(args.target[args.target.find('.', 1) + 1:])
            html = urlopen(args.target)
        else:
            sys.exit(1)
        
    content = html.read()
    soup = BeautifulSoup(content, 'lxml')
    extractor = core.Extractor(soup, results.url_list)
    start_time = time.time()
    extractor.extract('a')
    extractor.extract('area')
    extractor.extract('link')
    end_time = time.time()
    
    if args.keystring:
        sorter = core.URLListSorter(results.url_list)
        sorter.keyword_sort(args.keystring)
    
    console_output_handler = core.ConsoleOutputHandler(args, results.url_list)
    console_output_handler.print()
    core.report_tool_performance(results.url_list, start_time, end_time)
    
    if args.print:
        file_output_handler = core.FileOutputHandler(args.target, results.url_list)
        file_output_handler.create_file()

def main():
    print_program_info()
    start_extractor()
    sys.exit(0)

if __name__ == '__main__':
    main()