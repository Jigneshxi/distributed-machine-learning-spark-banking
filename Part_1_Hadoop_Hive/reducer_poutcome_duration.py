#!/usr/bin/env python3
"""
Reducer: Calculates average duration (seconds) per previous campaign outcome ('poutcome').
Output: poutcome \t TotalCount \t TotalDuration \t AverageDuration
"""
import sys

def main():
    current_key = None
    total_duration = 0.0
    total_count = 0

    print(f"{'Previous Outcome (poutcome)':<28} | {'Total Contacts':<16} | {'Avg Duration (s)':<18} | {'Avg Duration (min)':<18}")
    print("-" * 86)

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        parts = line.split('\t')
        if len(parts) != 2:
            continue
        key, val = parts
        try:
            dur_str, cnt_str = val.split(',')
            duration = float(dur_str)
            cnt = int(cnt_str)
        except ValueError:
            continue

        if current_key == key:
            total_duration += duration
            total_count += cnt
        else:
            if current_key is not None:
                avg_sec = total_duration / total_count if total_count > 0 else 0
                avg_min = avg_sec / 60.0
                print(f"{current_key:<28} | {total_count:<16} | {avg_sec:<18.2f} | {avg_min:<18.2f}")
            current_key = key
            total_duration = duration
            total_count = cnt

    if current_key is not None and total_count > 0:
        avg_sec = total_duration / total_count
        avg_min = avg_sec / 60.0
        print(f"{current_key:<28} | {total_count:<16} | {avg_sec:<18.2f} | {avg_min:<18.2f}")

if __name__ == '__main__':
    main()
