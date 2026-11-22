#!/usr/bin/env python3
"""
Reducer: Counts individuals with and without a housing loan in each education category.
Input: sorted (education,housing \t 1)
Outputs formatted contingency table of counts.
"""
import sys

def main():
    current_key = None
    current_count = 0
    results = {}

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        parts = line.split('\t')
        if len(parts) != 2:
            continue
        key, count_str = parts
        try:
            count = int(count_str)
        except ValueError:
            continue

        if current_key == key:
            current_count += count
        else:
            if current_key is not None:
                edu, hsg = current_key.split(',')
                results.setdefault(edu, {})[hsg] = current_count
            current_key = key
            current_count = count

    if current_key is not None:
        edu, hsg = current_key.split(',')
        results.setdefault(edu, {})[hsg] = current_count

    print(f"{'Education Level':<18} | {'Housing Loan: NO':<18} | {'Housing Loan: YES':<18} | {'Total':<10}")
    print("-" * 72)
    for edu in sorted(results.keys()):
        no_cnt = results[edu].get('no', 0)
        yes_cnt = results[edu].get('yes', 0)
        tot = no_cnt + yes_cnt
        print(f"{edu:<18} | {no_cnt:<18} | {yes_cnt:<18} | {tot:<10}")

if __name__ == '__main__':
    main()
