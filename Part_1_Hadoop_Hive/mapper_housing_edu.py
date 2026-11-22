#!/usr/bin/env python3
"""
Mapper: Counts individuals with and without a housing loan in each education category.
Emits: (education,housing) \t 1
"""
import sys
import csv

def main():
    reader = csv.reader(sys.stdin)
    first_row = True
    for row in reader:
        if not row or len(row) < 17:
            continue
        if first_row and row[0].strip().lower() == 'age':
            first_row = False
            continue
        first_row = False
        education = row[3].strip()
        housing = row[6].strip()
        print(f"{education},{housing}\t1")

if __name__ == '__main__':
    main()
