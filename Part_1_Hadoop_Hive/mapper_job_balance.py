#!/usr/bin/env python3
"""
Mapper: Calculates the average account balance for each job type.
Reads CSV rows from STDIN, skips header, and emits: job \t balance,1
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
        job = row[1].strip()
        try:
            balance = float(row[5].strip())
            print(f"{job}\t{balance},1")
        except ValueError:
            continue

if __name__ == '__main__':
    main()
