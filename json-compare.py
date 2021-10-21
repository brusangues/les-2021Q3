import json
import os
import argparse
import re

'''
    usage: json-compare.py [-h] [-f FOLDER] [-f1 FILE1] [-f2 FILE2] [-o]

    Check if 2 json files are the same (regardless of key order), and optionally write the ordered json files with the suffix "_cmp".

    optional arguments:
    -h, --help            show this help message and exit
    -f FOLDER, --Folder FOLDER
                            Root folder.
    -f1 FILE1, --File1 FILE1
                            First file to be compared.
    -f2 FILE2, --File2 FILE2
                            Second file to be compared.
    -o, --Output          Flag indicating wether to write output files or not.


    examples:

    python json-compare/json-compare.py -f1 "reports/annotationtest.json" -f2 "reports/annotationtest2.json"

    python json-compare/json-compare.py -f1 "reports/annotationtest.json" -f2 "reports/annotationtest2.json" -o

    python json-compare/json-compare.py -f "reports" -f1 "annotationtest.json" -f2 "annotationtest2.json" -o
'''

description = '''
    Check if 2 json files are the same (regardless of key order), and
    optionally write the ordered json files with the suffix "_cmp".
    '''

def main():
    # Initialize parser
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-f", "--Folder", help = "Root folder.", default="")
    parser.add_argument("-f1", "--File1", help = "First file to be compared.", required=True)
    parser.add_argument("-f2", "--File2", help = "Second file to be compared.", required=True)
    parser.add_argument("-o", "--Output", action="store_true", \
        help= "Flag indicating wether to write output files or not.")
    
    # Read arguments from command line
    args = parser.parse_args()

    file1 = os.path.join(args.Folder, args.File1)
    file2 = os.path.join(args.Folder, args.File2)

    compareJson(file1, file2, args.Output)

def sortedDeep(d):
    # source: https://www.titanwolf.org/Network/q/e7f3720e-1c8d-4da7-b925-cd2a4301192a/y
    #def makeTuple(v): return (*v,) if isinstance(v,(list,dict)) else (v,)
    if isinstance(d,list):
        return sorted( map(sortedDeep,d), key=json.dumps )
    if isinstance(d,dict):
        return { k: sortedDeep(d[k]) for k in sorted(d)}
    return d

def applyNtimes(d,f,n):
    for _ in range(n):
        d = f(d)
    return d

def getFileLines(f): 
    return sum(1 for line in open(f))

def compareJson(path1,path2, write=False):
    # Size comparison
    s1 = os.path.getsize(path1)
    s2 = os.path.getsize(path2)
    print("JSON sizes match?", s1 == s2, s1, s2)

    # Line count comparison
    l1 = getFileLines(path1)
    l2 = getFileLines(path2)
    print("JSON line count match?", l1 == l2, l1, l2)

    # Contents comparison
    data1 = dict()
    data2 = dict()
    lines1= []
    lines2= []
    with open(path1) as f: data1 = json.load(f)
    with open(path2) as f: data2 = json.load(f)

    #apply sorting 100 times to make sure all nested dicts are sorted
    data1 = applyNtimes(data1, sortedDeep, 100) 
    data2 = applyNtimes(data2, sortedDeep, 100)

    json1 = json.dumps(data1, sort_keys=True)
    json2 = json.dumps(data2, sort_keys=True)
    print("JSON contents match?", json1 == json2)
    
    path_out1 = path1[:-5]+"_cmp.json"
    path_out2 = path2[:-5]+"_cmp.json"

    if write:
        print("Writting output JSON files:", path_out1, path_out2, sep="\n")

    with open(path_out1, 'w') as f:
        json.dump(data1, f, indent=2, sort_keys=True)
    with open(path_out2, 'w') as f:
        json.dump(data2, f, indent=2, sort_keys=True)

    # Ordered lines comparison
    with open(path_out1) as f: lines1 = f.readlines()
    with open(path_out2) as f: lines2 = f.readlines()

    if not write:
        os.remove(path_out1)
        os.remove(path_out2)

    lines1 = sorted(lines1)
    lines2 = sorted(lines2)

    if write:
        print("Writting output TXT files:", path_out1+".txt", path_out1+".txt", sep="\n")
        with open(path_out1+".txt", 'w') as f:
            for line in lines1:
                f.write(line)
        with open(path_out2+".txt", 'w') as f:
            for line in lines2:
                f.write(line)

    print("JSON ordered lines match?", lines1 == lines2)
    if not lines1 == lines2:
        if l2>=l1:
            lines1 = lines1+["" for _ in range(l2-l1)]
        else:
            lines2 = lines2+["" for _ in range(l1-l2)]
        
        equal_lines = sum([a==b for a,b in zip(lines1,lines2)])

        print("Number of equal ordered lines:", equal_lines, "/", max(l1,l2))

if __name__=="__main__":
    main()
