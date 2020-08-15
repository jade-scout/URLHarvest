""" This file contains supporting routines for the main program. """

from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError


def print_error(string):
    print('[error] ' + string + '\n')
    return
    
def print_info(string):
    print('[info] ' + string)
    return

def is_valid_url(url):

    try:
        urlopen(url)
    except HTTPError as error:
        print_error('Encountered ' + str(error.code) + ' error code')
        return False
    except URLError as error:
        print_error('Encountered URLError: ' + str(error.reason))
        return False
    except ValueError:
        print_error('Invalid URL')
        return False

    return True;

def is_valid_file(string):
    
    if string.endswith('.htm'):
        return True
    if string.endswith('.html'):
        return True
    if string.endswith('.xml'):
        return True
        
    return False

def is_link(string):

    if string.startswith('http'):
        return True
    # This test could possibly backfire if a sub-directory did not have a name
    # if and only if it is possible for a sub-directory not to have a name
    if string.startswith('//'):
        return True
    if string.startswith('www.'):
        return True
        
    return False
    
def is_image(string):
    
    if string.find('.bmp') > -1:
        return True
    
    if string.find('.gif') > -1:
        return True
    
    if string.find('.ico') > -1:
        return True
    
    if string.find('.jpeg') > -1:
        return True
    
    if string.find('.png') > -1:
        return True
    
    if string.find('.tiff') > -1:
        return True
    
    return False
    
def is_style_sheet(string):

    if string.find('.css') > -1:
        return True
        
    return False