#!/usr/bin/env python3
"""
Stream Data Generator for Spark Streaming:
Chunks 'bank.csv' into simulated real-time micro-batches with synthetic transaction timestamps
and writes them incrementally into a streaming directory.
"""
import os
import time
import datetime
import pandas as pd

def generate_stream(input_csv="bank.csv", output_dir="Part_4_Spark_Streaming/streaming_input", chunk_size=50, delay_sec=2):
    os.makedirs(output_dir, exist_ok=True)
    df = pd.read_csv(input_csv)
    
    total_records = len(df)
    total_chunks = (total_records + chunk_size - 1) // chunk_size
    print(f"Starting simulated stream: {total_records} records into {total_chunks} micro-batches...")
    
    for i in range(total_chunks):
        chunk = df.iloc[i * chunk_size : (i + 1) * chunk_size].copy()
        
        # Add synthetic event timestamp for streaming and watermarking
        now = datetime.datetime.now()
        chunk["timestamp"] = [now - datetime.timedelta(seconds=(len(chunk) - j)) for j in range(len(chunk))]
        
        file_name = f"transaction_batch_{i+1:03d}.csv"
        file_path = os.path.join(output_dir, file_name)
        
        chunk.to_csv(file_path, index=False)
        print(f"Emitted Batch {i+1}/{total_chunks} ({len(chunk)} rows) -> {file_name}")
        
        if delay_sec > 0 and i < 5:  # generate initial sample batches quickly
            time.sleep(delay_sec)

    print("Stream generator completed successfully.")

if __name__ == '__main__':
    generate_stream(delay_sec=0.1)
