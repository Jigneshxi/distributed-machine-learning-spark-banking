#!/usr/bin/env python3
"""
Mapper: Determines number of clients contacted in each month and subscription status to term deposits ('y').
Emits: month,y \t 1
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
        month = row[10].strip().lower()
        y = row[16].strip().lower()
        print(f"{month},{y}\t1")

if __name__ == '__main__':
    main()
