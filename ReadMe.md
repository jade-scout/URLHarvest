## URLHarvest

### About

URLHarvest is a simple, CLI-based Web scraping tool, designed
for extracting URLs from webpages. It can extract URLs from
both files and URLs leading to webpages.

### Syntax

`python urlharvest.py <target> [-options]

*<target>* can either be a webpage URL or a HTML/HTM/XML file
on the local machine.

## Options:
*[-a][--all]       = Print all URLs found.
*[-k][--keystring] = Print only the URLs or those URLs whose attributes
                     contain KEYSTRING.
*[-l][--limit]     = Limit the number of URLs that will be printed.
                     Default is 200.
*[-p][--print]     = Print URLHarvest's output to a file.

### Technical Information

Platform (tested): Windows 10
Python Version:    3.6

### Disclaimer

URLHarvest was created for lawful and ethical purposes and any use of
this tool for illegal or otherwise harmful intent is strictly forbidden.
The author of URLHarvest is in no way responsible for the abuse of this
tool or for any damage caused by it either to users or targeted servers.
Users of URLHarvest must be considerate of the websites that they run
this tool on, must never cause server overload by too many or too large requests,
and preferably obtain the consent of the site administrators before running
URLHarvest on their domain.