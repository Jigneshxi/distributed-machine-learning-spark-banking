# 🎙️ Master Interview Defense & Quick Revision CheatSheet
**Date:** 2026-10-12  
**Candidate:** Jignesh (AlmaBetter Masters Data Science)  
**Project:** Financial Forecasting Frontier: Distributed ML

---

## 🚀 Quick Executive Pitch (30 Seconds)
"I built an end-to-end distributed data and machine learning system for commercial banking. Using Hadoop HDFS and Apache Hive for scalable storage and warehousing, PySpark for in-memory exploratory analytics, Spark ML for imbalanced binary classification (ROC-AUC 0.892), and Spark Structured Streaming with watermarking for real-time transaction scoring and windowed trend analytics."

---

## 🎯 Top 10 Technical Interview Defense Questions

### 1. Why is Spark 10x-100x faster than Hadoop MapReduce?
MapReduce writes intermediate results of every map and reduce phase to physical disk, causing heavy I/O bottlenecks. Spark operates in-memory using Resilient Distributed Datasets (RDDs), executes lazy evaluation Directed Acyclic Graphs (DAGs), and pipelines multiple transformations within memory without disk round-trips.

### 2. How did you handle the 88.5% / 11.5% class imbalance in Spark ML?
Rather than relying on misleading raw accuracy, we evaluated models using **ROC-AUC** (0.8923) and **PR-AUC** (0.5218) via `BinaryClassificationEvaluator`. We performed 3-fold cross-validation with `ParamGridBuilder` to optimize minority-class recall and F1-score.

### 3. What were the most important features in predicting deposit subscriptions?
1. `duration` (30.95% relative importance) - Call engagement duration.
2. `poutcome_success` (7.89%) - Prior campaign positive outcome.
3. `age` (7.71%) - Senior cohorts hold significantly greater capital.
4. `balance` (6.96%) - Liquid account balance.

### 4. What is watermarking in Spark Streaming and why is it needed?
Watermarking specifies how long to wait for late-arriving event-time data (`withWatermark("timestamp", "10s")`). Once the watermark threshold passes, older window states are dropped from executor memory, preventing JVM heap memory exhaustion (OutOfMemory errors) in long-running streaming apps.

### 5. When should you use `repartition()` vs `coalesce()`?
Use `repartition()` when you need to increase partitions or balance skewed data across nodes via a full network shuffle. Use `coalesce()` when reducing partition count (e.g. before writing output files), as it avoids a network shuffle by merging existing local partitions.

### 6. What strategic business recommendations did you provide to the bank?
* **Reallocate Marketing Budgets**: Shift telemarketing focus away from May (1,398 calls, 6.65% conversion) toward October (46.25%), December (45.0%), and March (42.86%).
* **Prioritize High-Liquidity Cohorts**: Target seniors (>60) and management professionals who maintain balances 2.5x higher than average.
* **Real-Time Call Routing**: Route calls lasting over 4 minutes to specialized investment sales advisors in real time.

### 7. How does Spark's Catalyst Optimizer work?
Catalyst takes user DataFrame operations, constructs an unresolved logical plan, resolves schemas via the Metastore, applies rule-based logical optimizations (predicate pushdown, projection pruning), creates physical execution plans, cost-models them, and compiles the winner into Java bytecode using Whole-Stage Code Generation.

### 8. What is data skew and how do you resolve it in Spark?
Data skew occurs when one partition contains disproportionately more records than others (e.g. 30% of calls occurring in May), causing a single executor core to become a bottleneck straggler. It is mitigated by salting join/group keys with random prefixes, or key-based repartitioning.

### 9. How do you scale this architecture further in cloud production?
* Managed Clusters: Deploy on AWS EMR or Databricks with auto-scaling spot instances.
* Ingestion: Connect Spark Streaming to an Apache Kafka distributed message queue.
* Feature Store & Registry: Implement Feast for real-time feature lookup and MLflow for model versioning and tracking.

### 10. What is the role of Hive when Spark is available?
Hive serves as the enterprise data catalog, metadata repository (Hive Metastore), and analytical warehouse for business analysts writing SQL queries directly on HDFS data lakes, while Spark excels as the compute engine for complex data transformations, ML, and streaming.
