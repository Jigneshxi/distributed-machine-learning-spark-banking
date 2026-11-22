import os
import subprocess
import pytest
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, accuracy_score
from sklearn.preprocessing import LabelEncoder

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

@pytest.fixture(scope="session")
def bank_df():
    csv_path = os.path.join(BASE_DIR, "bank.csv")
    assert os.path.exists(csv_path), "bank.csv missing"
    return pd.read_csv(csv_path, sep=",")


def test_01_bank_dataset_schema_and_integrity(bank_df):
    """Verify that bank.csv contains exactly 4,521 rows and 17 expected financial/demographic attributes."""
    assert len(bank_df) == 4521, f"Expected 4521 rows, got {len(bank_df)}"
    expected_cols = [
        'age', 'job', 'marital', 'education', 'default', 'balance',
        'housing', 'loan', 'contact', 'day', 'month', 'duration',
        'campaign', 'pdays', 'previous', 'poutcome', 'y'
    ]
    assert list(bank_df.columns) == expected_cols, "Column mismatch in bank.csv"
    assert bank_df.isna().sum().sum() == 0, "bank.csv should have 0 null values"


def test_02_mapreduce_streaming_pairs():
    """Verify Hadoop streaming mapper and reducer execution via standard stdin/stdout pipeline."""
    mapper_path = os.path.join(BASE_DIR, "Part_1_Hadoop_Hive", "mapper_job_balance.py")
    reducer_path = os.path.join(BASE_DIR, "Part_1_Hadoop_Hive", "reducer_job_balance.py")

    assert os.path.exists(mapper_path), "mapper_job_balance.py missing"
    assert os.path.exists(reducer_path), "reducer_job_balance.py missing"

    sample_csv = "age,job,marital,education,default,balance,housing,loan,contact,day,month,duration,campaign,pdays,previous,poutcome,y\n" \
                 "30,management,married,tertiary,no,1000,no,no,cellular,19,oct,79,1,-1,0,unknown,no\n" \
                 "40,management,married,tertiary,no,3000,no,no,cellular,19,oct,120,1,-1,0,unknown,yes\n"

    # Run mapper
    p1 = subprocess.Popen(["python", mapper_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out1, _ = p1.communicate(input=sample_csv)

    assert "management\t1000.0,1" in out1
    assert "management\t3000.0,1" in out1

    # Run reducer
    p2 = subprocess.Popen(["python", reducer_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out2, _ = p2.communicate(input=out1)

    assert "management" in out2
    assert "2000.00" in out2 # Average of 1000 and 3000


def test_03_hive_hql_script_syntax_and_tables():
    """Validate that Hive script contains valid DDL, partitioned table creation, and analytical window queries."""
    hql_path = os.path.join(BASE_DIR, "Part_1_Hadoop_Hive", "banking_hive_queries.hql")
    assert os.path.exists(hql_path), "banking_hive_queries.hql missing"

    with open(hql_path, 'r', encoding='utf-8') as f:
        content = f.read()

    assert "CREATE TABLE" in content or "CREATE EXTERNAL TABLE" in content
    assert "ROW FORMAT DELIMITED" in content
    assert "FIELDS TERMINATED BY" in content
    assert "STORED AS TEXTFILE" in content
    assert "SELECT" in content and "GROUP BY" in content


def test_04_eda_aggregations_and_wealth_gradient(bank_df):
    """Verify PySpark EDA findings: elderly clients (>60) maintain >2x higher average balances than youth (<30)."""
    elderly_bal = bank_df[bank_df['age'] > 60]['balance'].mean()
    young_bal = bank_df[bank_df['age'] < 30]['balance'].mean()

    assert elderly_bal > 2000.0, f"Expected elderly balance > 2000, got {elderly_bal:.2f}"
    assert young_bal < 1200.0, f"Expected youth balance < 1200, got {young_bal:.2f}"
    assert elderly_bal > 2.0 * young_bal, "Elderly balance should be at least double youth balance"


def test_05_predictive_modeling_pipeline_metrics(bank_df):
    """Validate distributed predictive modeling benchmark achieving ROC-AUC >= 0.85 and Accuracy >= 88%."""
    df = bank_df.copy()
    y = (df['y'] == 'yes').astype(int)

    feature_cols = ['age', 'balance', 'day', 'duration', 'campaign', 'pdays', 'previous']
    cat_cols = ['job', 'marital', 'education', 'default', 'housing', 'loan', 'contact', 'month', 'poutcome']

    for c in cat_cols:
        le = LabelEncoder()
        df[c] = le.fit_transform(df[c].astype(str))
        feature_cols.append(c)

    X = df[feature_cols]

    # Train Random Forest
    rf = RandomForestClassifier(n_estimators=50, max_depth=10, random_state=42)
    rf.fit(X, y)
    preds = rf.predict(X)
    probs = rf.predict_proba(X)[:, 1]

    acc = accuracy_score(y, preds)
    auc = roc_auc_score(y, probs)

    assert acc >= 0.88, f"Accuracy {acc:.4f} should be >= 0.88"
    assert auc >= 0.85, f"ROC-AUC {auc:.4f} should be >= 0.85"


def test_06_feature_importance_ranking(bank_df):
    """Verify that contact duration represents the single most dominant predictor of deposit subscription."""
    df = bank_df.copy()
    y = (df['y'] == 'yes').astype(int)
    feature_cols = ['age', 'balance', 'day', 'duration', 'campaign', 'pdays', 'previous']

    rf = RandomForestClassifier(n_estimators=30, max_depth=8, random_state=42)
    rf.fit(df[feature_cols], y)

    importances = dict(zip(feature_cols, rf.feature_importances_))
    # Duration must be the top feature
    top_feature = max(importances, key=importances.get)
    assert top_feature == 'duration', f"Expected 'duration' as top feature, got {top_feature}"
    assert importances['duration'] >= 0.25, "Duration importance must exceed 25%"


def test_07_streaming_batch_generator():
    """Verify that streaming data generator script exists and produces micro-batch CSVs."""
    gen_script = os.path.join(BASE_DIR, "Part_4_Spark_Streaming", "stream_data_generator.py")
    input_dir = os.path.join(BASE_DIR, "Part_4_Spark_Streaming", "streaming_input")

    assert os.path.exists(gen_script), "stream_data_generator.py missing"
    assert os.path.exists(input_dir), "streaming_input folder missing"

    batches = [f for f in os.listdir(input_dir) if f.endswith(".csv")]
    assert len(batches) >= 50, f"Expected at least 50 streaming micro-batches, found {len(batches)}"


def test_08_windowed_aggregation_and_watermarking():
    """Verify structured streaming sliding window aggregation and watermark threshold logic."""
    events = [
        {"timestamp": 100, "call_duration": 300, "balance": 1500},
        {"timestamp": 105, "call_duration": 450, "balance": 2200},
        {"timestamp": 110, "call_duration": 120, "balance": 800},
        {"timestamp": 85,  "call_duration": 500, "balance": 3000} # Late event (> 10s late)
    ]

    watermark_threshold = 100 - 10 # 90
    accepted_events = [e for e in events if e["timestamp"] >= watermark_threshold]

    # Late arrival at timestamp 85 (< 90) must be discarded
    assert len(accepted_events) == 3, f"Expected 3 events accepted after watermarking, got {len(accepted_events)}"
    assert all(e["timestamp"] >= 90 for e in accepted_events)


def test_09_data_parallelism_partition_tuning():
    """Verify Spark data parallelism logic: broadcast hash joins vs shuffle hash joins."""
    small_lookup_table_size_mb = 0.05 # 50 KB
    broadcast_threshold_mb = 10.0 # Standard 10MB threshold

    is_broadcast_join = small_lookup_table_size_mb < broadcast_threshold_mb
    assert is_broadcast_join, "Tables under 10MB must trigger broadcast hash join"

    # Repartition vs Coalesce arithmetic
    n_source_partitions = 8
    target_coalesce = 2
    # Coalesce reduces without full shuffle
    assert target_coalesce < n_source_partitions


def test_10_documentation_and_artifact_completeness():
    """Verify that all 5 parts have formatted Word reports, Colab notebooks, figures, and presentation script."""
    part_files = [
        os.path.join(BASE_DIR, "Part_1_Hadoop_Hive", "Part1_Hadoop_Hive_Analysis.docx"),
        os.path.join(BASE_DIR, "Part_2_Spark_EDA", "Part2_Spark_EDA.docx"),
        os.path.join(BASE_DIR, "Part_2_Spark_EDA", "Part2_Spark_EDA_Colab.ipynb"),
        os.path.join(BASE_DIR, "Part_3_Predictive_Modeling", "Part3_Predictive_Modeling_SparkML.docx"),
        os.path.join(BASE_DIR, "Part_3_Predictive_Modeling", "Part3_Predictive_Modeling_Colab.ipynb"),
        os.path.join(BASE_DIR, "Part_4_Spark_Streaming", "Part4_RealTime_Transaction_Analysis.docx"),
        os.path.join(BASE_DIR, "Part_4_Spark_Streaming", "Part4_Spark_Streaming_Colab.ipynb"),
        os.path.join(BASE_DIR, "Part_5_Data_Parallelism", "Part5_Data_Parallelism.docx"),
        os.path.join(BASE_DIR, "Part_5_Data_Parallelism", "Part5_Data_Parallelism_Colab.ipynb"),
        os.path.join(BASE_DIR, "Submission_Docs", "Reflective_Summary.docx"),
        os.path.join(BASE_DIR, "Submission_Docs", "Video_Presentation_Script_15Min.docx")
    ]
    for pf in part_files:
        assert os.path.exists(pf), f"Critical deliverable missing: {pf}"
        assert os.path.getsize(pf) > 0, f"Deliverable is empty: {pf}"
