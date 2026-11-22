#!/usr/bin/env python3
"""
Reducer: Calculates the average account balance for each job type.
Reads sorted (job \t balance,1) from STDIN, sums balance and count, and outputs:
Job \t TotalCount \t TotalBalance \t AverageBalance
"""
import sys

def main():
    current_job = None
    total_balance = 0.0
    total_count = 0

    print("Job\tCount\tTotalBalance\tAverageBalance")
    print("-" * 55)

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        parts = line.split('\t')
        if len(parts) != 2:
            continue
        job, val = parts
        try:
            bal_str, cnt_str = val.split(',')
            balance = float(bal_str)
            count = int(cnt_str)
        except ValueError:
            continue

        if current_job == job:
            total_balance += balance
            total_count += count
        else:
            if current_job is not None:
                avg = total_balance / total_count if total_count > 0 else 0
                print(f"{current_job}\t{total_count}\t{total_balance:.2f}\t{avg:.2f}")
            current_job = job
            total_balance = balance
            total_count = count

    if current_job is not None and total_count > 0:
        avg = total_balance / total_count
        print(f"{current_job}\t{total_count}\t{total_balance:.2f}\t{avg:.2f}")

if __name__ == '__main__':
    main()
