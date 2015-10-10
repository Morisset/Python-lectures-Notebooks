#!/usr/bin/env python

import os
import argparse
import re

__version__ = "grep.py by Ch. Morisset, clase de Python, IA-UNAM 2015, version 1.0"

parser = argparse.ArgumentParser()
parser.add_argument("pattern", 
                    help="pattern to search for.")
parser.add_argument("file", nargs='+', 
                    help="file(s) to search in. Wildcards and directoies accepted.")
parser.add_argument("-A", "--after-context", type=int,
                    help="Print num lines of trailing context after each match.  See also the -B and -C options.")
parser.add_argument("-B", "--before-context", type=int,
                    help="Print num lines of leading context before each match.  See also the -A and -C options.")
parser.add_argument("-C", "--context", type=int,
                    help="Print num lines of trailing and leading context before each match.  See also the -A and -B options.")
parser.add_argument("-n", "--line-number", action="store_true", 
                    help="Each output line is preceded by its relative line number in the file, starting at line 1.")
parser.add_argument("-c", "--count", action="store_true",
                    help="Only a count of selected lines is written to standard output.")
parser.add_argument("-l", "--files-with-matches", action="store_true",
                    help="Only the names of files containing selected lines are written to standard output.")
parser.add_argument("-v", "--invert-match", action="store_true",
                    help="Selected lines are those not matching any of the specified patterns.")
parser.add_argument("-r", "--recursive", action="store_true",
                    help="Recursively search subdirectories listed.")
parser.add_argument("-V", "--version", action="version", version=__version__,
                    help="Display version information and exit.")

args = parser.parse_args()
    
args_before_context = args.before_context
args_after_context = args.after_context
args_line_number = args.line_number

if args_before_context is None:
    args_before_context = 0
if args_after_context is None:
    args_after_context = 0
if args.context is not None:
    args_before_context = args.context
    args_after_context = args.context
if args.count or args.files_with_matches:
    args_before_context = 0
    args_after_context = 0
    args_line_number = False

files = []
for f in args.file:
    if os.path.isdir(f):
        if args.recursive:
            for root, dirnames, filenames in os.walk(f):
                for basename in filenames:
                    files.append(os.path.join(root, basename))
    elif os.path.isfile(f):
        files.append(f)
    
for f in files:
    ff =  open(f, 'r')
    lines = ff.readlines()
    n_lines = len(lines)
    count = 0
    for i, line in enumerate(lines):
        if args.invert_match:
            match = not re.search(args.pattern, line)
        else:
            match = re.search(args.pattern, line)
        if match:
            if args_before_context != 0:
                print('--')
                i_inf = max(0, i-args_before_context)
                i_sup = max(0, i)
                for j in range(i_inf,i_sup):
                    to_print = '{}-'.format(f)
                    if args_line_number:
                        to_print +='{}-'.format(j+1)
                    to_print += lines[j]
                    print to_print,
            to_print = '{}:'.format(f)
            if args_line_number:
                to_print +='{}:'.format(i+1)
            to_print += line
            count += 1
            if not args.count and not args.files_with_matches:
                print to_print,
            if args_after_context != 0:
                i_inf = min(n_lines-1, i+1)
                i_sup = min(n_lines-1, i+args_after_context+1)
                for j in range(i_inf,i_sup):
                    to_print = '{}-'.format(f)
                    if args_line_number:
                        to_print +='{}-'.format(j+1)
                    to_print += lines[j]
                    print to_print,
                print('--')
    if args.count:
        print('{}:{}'.format(f, count))
    if args.files_with_matches and count > 0:
        print(f)
