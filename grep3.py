#!/usr/bin/env python

import os
import argparse
import re
from glob import glob

__version__ = "grep.py by Ch. Morisset, clase de Python, IA-UNAM 2015, version 3.2"

def get_parser():
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
    parser.add_argument("-r", "--recursive", action="store_true",
                        help="Recursively search subdirectories listed.")
    parser.add_argument("-v", "--invert-match", action="store_true",
                        help="Selected lines are those not matching any of the specified patterns. Used only with -l")
    parser.add_argument("-V", "--version", action="version", version=__version__,
                        help="Display version information and exit.")
    parser.add_argument("-l", "--files-with-matches", action="store_true",
                        help="Only the names of files containing selected lines are written to standard output.")
    return parser

class grep(object):
    
    __version__ = __version__

    def __init__(self, pattern, fs, recursive=False, before=0, after=0, context=0):
        """
        a python grep object
        """
        self.pattern = pattern
        self.before = before
        if self.before is None:
            self.before = 0
        self.after = after
        if self.after is None:
            self.after = 0
        self.context = context
        if self.context != 0 and self.context is not None:
            self.before = self.context
            self.after = self.context
        self.files = self.get_files(fs, recursive=recursive)
        self.scan_files()
        
    def get_files(self, fs, recursive=True):
        files = []
        if type(fs) is str:
            fs = glob(fs)
        for f in fs:
            if os.path.isdir(f):
                if recursive:
                    for root, dirnames, filenames in os.walk(f):
                        for basename in filenames:
                            files.append(os.path.join(root, basename))
            elif os.path.isfile(f):
                files.append(f)
        return files
    
    def scan_files(self):
        self.res = {}

        for f in self.files:
            self.res[f] = {}
            self.res[f]['count'] = 0
            self.res[f]['A'] = []
            self.res[f]['B'] = []
            self.res[f]['match'] = []
            
            ff =  open(f, 'r')
            lines = ff.readlines()
            n_lines = len(lines)
            count = 0
            for i, line in enumerate(lines):
                match = re.search(self.pattern, line)
                if match:
                    B = []
                    if self.before != 0:
                        i_inf = max(0, i - self.before)
                        i_sup = max(0, i)
                        for j in range(i_inf,i_sup):
                            B.append((j+1, lines[j]))
                    count += 1
                    A = []
                    if self.after != 0:
                        i_inf = min(n_lines-1, i+1)
                        i_sup = min(n_lines-1, i+self.after+1)
                        for j in range(i_inf,i_sup):
                            A.append((j+1, lines[j]))
                    self.res[f]['match'].append((i+1, line))
                    self.res[f]['B'].append(B)
                    self.res[f]['A'].append(A)
            self.res[f]['count'] = count

    def my_print(self, f, n_str, print_n=False, delimitor='-'):
        if print_n:
            print('{}{}{}{}{}'.format(f, delimitor, n_str[0], delimitor, n_str[1])),
        else:
            print('{}{}{}'.format(f, delimitor, n_str[1])),
    
    def print_res(self, print_n=False, print_counts=False, 
                  files_with_matches=False, invert_match=False):

        if invert_match:
            for f in self.res.keys():
                if self.res[f]['count'] == 0:
                    print('{}'.format(f))
        elif print_counts:
            for f in self.res.keys():
                if self.res[f]['count'] != 0:
                    print('{}:{}'.format(f, self.res[f]['count']))
        elif files_with_matches:
            for f in self.res.keys():
                if self.res[f]['count'] != 0:
                    print('{}'.format(f))
        else:
            for f in self.res.keys():
                for i_match in range(self.res[f]['count']):
                    for b in self.res[f]['B'][i_match]:
                        if b != []:
                            self.my_print(f, b, print_n)
                    self.my_print(f, self.res[f]['match'][i_match], print_n, ':')
                    for a in self.res[f]['A'][i_match]:
                        if a != []:
                            self.my_print(f, a, print_n, )
                    print('--')
                print('----')
        
        
if __name__ == '__main__':
    
    parser = get_parser()
    args = parser.parse_args()
    g = grep(args.pattern, args.file, recursive=args.recursive,
             before=args.before_context, after=args.after_context,
             context=args.context)
    g.print_res(print_n=args.line_number, print_counts=args.count, 
                files_with_matches=args.files_with_matches, invert_match=args.invert_match)
