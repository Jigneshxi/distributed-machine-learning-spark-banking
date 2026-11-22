-- ====================================================================
-- CAPSTONE PROJECT: FINANCIAL FORECASTING FRONTIER - DISTRIBUTED ML
-- PART 1: HIVE DATA ANALYSIS & MANAGEMENT QUERIES
-- Database: banking_data | Table: client_info
-- ====================================================================

-- 1. Data Ingestion and Table Creation
-- Step 1.1: Create database banking_data
CREATE DATABASE IF NOT EXISTS banking_data;
USE banking_data;

-- Step 1.2: Define and create client_info table
DROP TABLE IF EXISTS client_info;
CREATE TABLE client_info (
    age INT,
    job STRING,
    marital STRING,
    education STRING,
    `default` STRING,
    balance INT,
    housing STRING,
    loan STRING,
    contact STRING,
    day INT,
    month STRING,
    duration INT,
    campaign INT,
    pdays INT,
    previous INT,
    poutcome STRING,
    y STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
TBLPROPERTIES ("skip.header.line.count"="1");

-- Step 1.3: Load the data from bank.csv into client_info
-- (HDFS or local file path)
LOAD DATA LOCAL INPATH '/home/hadoop/data/bank.csv' OVERWRITE INTO TABLE client_info;


-- 2. Basic Data Exploration
-- 2.1: Count total number of clients
SELECT COUNT(*) AS total_clients FROM client_info;

-- 2.2: Display first 10 rows
SELECT * FROM client_info LIMIT 10;


-- 3. Data Filtering and Sorting
-- 3.1: Retrieve all records of clients who are married and have a personal loan
SELECT age, job, marital, education, balance, housing, loan, y
FROM client_info
WHERE LOWER(marital) = 'married' AND LOWER(loan) = 'yes'
LIMIT 25;

-- 3.2: List top 10 clients with the highest balance (job, marital, balance)
SELECT job, marital, balance
FROM client_info
ORDER BY balance DESC
LIMIT 10;


-- 4. Data Aggregation and Grouping
-- 4.1: Calculate average age of clients for each job category
SELECT 
    job, 
    COUNT(*) AS total_clients,
    ROUND(AVG(age), 2) AS avg_age
FROM client_info
GROUP BY job
ORDER BY avg_age DESC;

-- 4.2: Total number of clients for each education level who have defaulted on credit
SELECT 
    education, 
    COUNT(*) AS defaulted_clients_count
FROM client_info
WHERE LOWER(`default`) = 'yes'
GROUP BY education
ORDER BY defaulted_clients_count DESC;


-- 5. Complex Queries for Insights
-- 5.1: Top 5 job categories with highest average balance and subscription percentage
SELECT 
    job,
    COUNT(*) AS total_clients,
    ROUND(AVG(balance), 2) AS avg_balance,
    SUM(CASE WHEN LOWER(y) = 'yes' THEN 1 ELSE 0 END) AS subscribed_count,
    ROUND((SUM(CASE WHEN LOWER(y) = 'yes' THEN 1 ELSE 0 END) / COUNT(*)) * 100, 2) AS subscription_rate_pct
FROM client_info
GROUP BY job
ORDER BY avg_balance DESC
LIMIT 5;

-- 5.2: Month with highest number of contacts and its campaign success rate
SELECT 
    month,
    COUNT(*) AS total_contacts,
    SUM(CASE WHEN LOWER(y) = 'yes' THEN 1 ELSE 0 END) AS subscribed_clients,
    ROUND((SUM(CASE WHEN LOWER(y) = 'yes' THEN 1 ELSE 0 END) / COUNT(*)) * 100, 2) AS success_rate_pct
FROM client_info
GROUP BY month
ORDER BY total_contacts DESC
LIMIT 1;


-- 6. Correlation Analysis
-- 6.1: Calculate Pearson correlation between age and balance
SELECT 
    ROUND(corr(age, balance), 4) AS correlation_age_balance
FROM client_info;


-- 7. Trend Analysis
-- 7.1: Contact distribution and subscription performance across calendar months
SELECT 
    month,
    COUNT(*) AS contacts_count,
    ROUND(AVG(duration), 2) AS avg_call_duration_sec,
    ROUND((SUM(CASE WHEN LOWER(y) = 'yes' THEN 1 ELSE 0 END) / COUNT(*)) * 100, 2) AS subscription_rate_pct
FROM client_info
GROUP BY month
ORDER BY contacts_count DESC;


-- 8. Anomaly Detection
-- 8.1: Unusual patterns in average balance across education levels & identifying outlier accounts
SELECT 
    education,
    COUNT(*) AS client_count,
    ROUND(AVG(balance), 2) AS avg_balance,
    MIN(balance) AS min_balance,
    MAX(balance) AS max_balance,
    ROUND(STDDEV(balance), 2) AS balance_stddev
FROM client_info
GROUP BY education
ORDER BY avg_balance DESC;


-- 9. Advanced Analysis
-- 9.1: Impact of previous campaign outcome (poutcome) on current campaign success
SELECT 
    poutcome,
    COUNT(*) AS total_contacts,
    SUM(CASE WHEN LOWER(y) = 'yes' THEN 1 ELSE 0 END) AS subscribed_count,
    ROUND((SUM(CASE WHEN LOWER(y) = 'yes' THEN 1 ELSE 0 END) / COUNT(*)) * 100, 2) AS subscription_rate_pct
FROM client_info
GROUP BY poutcome
ORDER BY subscription_rate_pct DESC;

-- 9.2: Compare average contact duration for subscribed vs non-subscribed clients
SELECT 
    y AS term_deposit_subscribed,
    COUNT(*) AS client_count,
    ROUND(AVG(duration), 2) AS avg_duration_sec,
    ROUND(AVG(duration) / 60.0, 2) AS avg_duration_min
FROM client_info
GROUP BY y;
