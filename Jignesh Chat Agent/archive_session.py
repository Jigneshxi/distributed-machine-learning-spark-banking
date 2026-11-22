#!/usr/bin/env python3
"""
Archive Session Utility for Jignesh Chat Agent:
Automatically organizes and archives agent chat sessions into dated subfolders with study-guide markdown files.
"""

import os
import sys
import datetime
import argparse

def get_base_dir():
    return os.path.dirname(os.path.abspath(__file__))

def create_study_guide(topic_name, date_str=None, content=None):
    if not date_str:
        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        
    base_dir = get_base_dir()
    date_dir = os.path.join(base_dir, date_str)
    os.makedirs(date_dir, exist_ok=True)
    
    # Clean topic filename
    clean_topic = topic_name.strip().replace(" ", "_").replace("-", "_")
    filename = f"{clean_topic}.md"
    file_path = os.path.join(date_dir, filename)
    
    if content is None:
        content = f"""# 📚 Study Guide: {topic_name.replace('_', ' ')}
**Date:** {date_str}  
**Author:** Jignesh (Student / ML Engineer)  
**Agent:** Antigravity AI Assistant  
**Topic:** {topic_name.replace('_', ' ')}

---

## 1. 🎯 Overview & Objectives
- Problem Statement:
- Key Technology Stack:
- Target Deliverables:

---

## 2. 🏛️ Core Concepts & Architecture Breakdown
- Architectural Overview:
- Component Responsibilities:

---

## 3. 💻 Code Implementations & Command References
```python
# Code snippet
```

---

## 4. 📊 Data Insights, Tables & Observations
| Metric | Value | Interpretation |
| :--- | :--- | :--- |
| Metric 1 | Value 1 | Observation 1 |

---

## 5. 🎙️ Interview Defense Questions & Explanations
### Q1: What is the core rationale for this approach?
**Answer:** 

---

## 6. ✅ Summary & Key Takeaways
- Key takeaway 1
- Key takeaway 2
"""
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"✅ Successfully archived study guide to: {file_path}")
    return file_path

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Archive Chat Session into Study Guide MD format.")
    parser.add_argument("--topic", type=str, default="General_Chat_Session", help="Topic or Title of the session")
    parser.add_argument("--date", type=str, default=None, help="Date in YYYY-MM-DD format (default: today)")
    args = parser.parse_args()
    
    create_study_guide(args.topic, args.date)
