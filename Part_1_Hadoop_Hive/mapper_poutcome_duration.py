#!/usr/bin/env python3
"""
Mapper: Emits poutcome and contact duration.
Output: poutcome \t duration,1
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
        poutcome = row[15].strip().lower()
        try:
            duration = float(row[11].strip())
            print(f"{poutcome}\t{duration},1")
        except ValueError:
            continue

if __name__ == '__main__':
    main()
