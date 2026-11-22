#!/usr/bin/env python3
"""
Mapper: Bins age into demographic tiers (<30, 30-45, 46-60, >60) and emits balance.
Output: age_bracket \t balance,1
"""
import sys
import csv

def categorize_age(age):
    if age < 30:
        return "1_<30"
    elif age <= 45:
        return "2_30-45"
    elif age <= 60:
        return "3_46-60"
    else:
        return "4_>60"

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
        try:
            age = int(row[0].strip())
            balance = float(row[5].strip())
            bracket = categorize_age(age)
            print(f"{bracket}\t{balance},1")
        except ValueError:
            continue

if __name__ == '__main__':
    main()
