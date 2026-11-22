#!/usr/bin/env python3
"""
Reducer: Aggregates client contacts by month and subscription status ('y').
Calculates conversion/success rate per month.
"""
import sys

MONTH_ORDER = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]

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
                month, sub = current_key.split(',')
                results.setdefault(month, {})[sub] = current_count
            current_key = key
            current_count = count

    if current_key is not None:
        month, sub = current_key.split(',')
        results.setdefault(month, {})[sub] = current_count

    print(f"{'Month':<8} | {'Subscribed (yes)':<18} | {'Not Subscribed (no)':<20} | {'Total Contacts':<16} | {'Success Rate (%)':<16}")
    print("-" * 88)
    sorted_months = sorted(results.keys(), key=lambda m: MONTH_ORDER.index(m) if m in MONTH_ORDER else 99)
    for m in sorted_months:
        yes_cnt = results[m].get('yes', 0)
        no_cnt = results[m].get('no', 0)
        tot = yes_cnt + no_cnt
        rate = (yes_cnt / tot * 100) if tot > 0 else 0.0
        print(f"{m.upper():<8} | {yes_cnt:<18} | {no_cnt:<20} | {tot:<16} | {rate:<16.2f}")

if __name__ == '__main__':
    main()
