import json
import os
import argparse
from datetime import datetime
import logging
import sys
import glob
import re

'''
usage: annotation-schema-hunter.py [-h] [-f FOLDER] [-o OUTPUT]

optional arguments:
  -h, --help            show this help message and exit
  -f FOLDER, --Folder FOLDER
                        Root folder. Defaults to root.
  -o OUTPUT, --Output OUTPUT
                        Path to output json and log. Defaults to root.
examples:
python annotation-schema-hunter.py -f "C:/asniffer/spring-framework-main" -o "schemas"
'''

def main():
    # Start time
    start = datetime.now()

    # Initialize parser
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-f", "--Folder", help = "Root folder. Defaults to root.", default="")
    parser.add_argument("-o", "--Output", help = "Path to output json and log. Defaults to root.", default="")
    
    # Read arguments from command line
    args = parser.parse_args()
    path_root = args.Folder
    if(not os.path.exists(path_root)): 
        raise Exception("Path does not exists.")

    date = datetime.today().strftime('%Y_%m_%d-%H_%M_%S-')
    date_plus_name = date+os.path.basename(os.path.normpath(path_root))
    file_log = os.path.join(args.Output, date_plus_name+'.log')
    file_json = os.path.join(args.Output, date_plus_name+'.json')

    # Init logger
    logger = makeLogger(file_log)
    logger.info(f'Logging to {file_log}')

    # Listing files
    logger.info(f'Listing files in {path_root} ...')
    path_wildcard = os.path.join(path_root, "**/*.java")
    files = list(glob.glob(path_wildcard, recursive=True))
    logger.info(f'{len(files)} files found.')

    # Regex
    logger.info(f'Parsing files in {path_root} ...')
    glossary = dict()
    matches = list()
    annotations = list()
    for file_name in files:
        with open(file_name, encoding='utf-8', mode="r") as f:
            contents = f.read()
            match = re.search("@interface\s+[a-zA-Z][a-zA-Z0-9_]*", contents)
            if match:
                matches.append(file_name)
                logger.info(f"--Match in {file_name}")
                value = re.search("package\s+([a-zA-Z.]*)", contents).group(1)
                keys = re.findall("@interface\s+([a-zA-Z][a-zA-Z0-9_]*)", contents)
                logger.info(f"----schema: {value}")
                for key in keys:
                    logger.info(f"----key: {key}")
                    annotations.append(key)
                    glossary[key] = value
    logger.info(f'Matched {len(matches)} files.')
    logger.info(f'Found {len(glossary)}/{len(annotations)} unique annotations.')

    # Output
    logger.info(f'Writing output json to {file_json} ...')
    with open(file_json, 'w') as f:
        json.dump(glossary, f, indent=4)
    logger.info(f'Finished in {datetime.now()-start}.')

def makeLogger(filename):
    logger = logging.getLogger('')
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(filename)
    sh = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s [%(filename)s.%(funcName)s:%(lineno)d] %(message)s', datefmt='%a, %d %b %Y %H:%M:%S')
    fh.setFormatter(formatter)
    sh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(sh)
    return logger

if __name__=="__main__":
    main()