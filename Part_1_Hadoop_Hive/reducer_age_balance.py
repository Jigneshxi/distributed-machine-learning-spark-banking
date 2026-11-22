#!/usr/bin/env python3
"""
Reducer: Calculates summary statistics of balance for each age bracket.
Outputs: AgeBracket, TotalCount, TotalBalance, AverageBalance, MinBalance, MaxBalance
"""
import sys

LABELS = {
    "1_<30": "<30 years (Young)",
    "2_30-45": "30-45 years (Early Career)",
    "3_46-60": "46-60 years (Established)",
    "4_>60": ">60 years (Senior/Retired)"
}

def main():
    current_key = None
    total_balance = 0.0
    total_count = 0
    min_bal = float('inf')
    max_bal = float('-inf')

    print(f"{'Age Bracket':<30} | {'Count':<8} | {'Avg Balance':<14} | {'Min Balance':<12} | {'Max Balance':<12}")
    print("-" * 84)

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        parts = line.split('\t')
        if len(parts) != 2:
            continue
        key, val = parts
        try:
            bal_str, cnt_str = val.split(',')
            bal = float(bal_str)
            cnt = int(cnt_str)
        except ValueError:
            continue

        if current_key == key:
            total_balance += bal
            total_count += cnt
            if bal < min_bal: min_bal = bal
            if bal > max_bal: max_bal = bal
        else:
            if current_key is not None:
                avg = total_balance / total_count if total_count > 0 else 0
                lbl = LABELS.get(current_key, current_key)
                print(f"{lbl:<30} | {total_count:<8} | {avg:<14.2f} | {min_bal:<12.2f} | {max_bal:<12.2f}")
            current_key = key
            total_balance = bal
            total_count = cnt
            min_bal = bal
            max_bal = bal

    if current_key is not None and total_count > 0:
        avg = total_balance / total_count
        lbl = LABELS.get(current_key, current_key)
        print(f"{lbl:<30} | {total_count:<8} | {avg:<14.2f} | {min_bal:<12.2f} | {max_bal:<12.2f}")

if __name__ == '__main__':
    main()
