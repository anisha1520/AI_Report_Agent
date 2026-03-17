# 📊 AI Compliance Reporting Agent

An autonomous Python-based system designed to ingest operational AI metrics (CSV/JSON) and transform them into structured, audit-ready regulatory reports using Large Language Models (LLMs).

---

## ⚙️ Core Functionality

* **🧩 Dynamic Schema Mapping:** Automatically interprets uploaded data fields and maps them to regulatory domains like Performance, Ethics, and Resilience.
* **🔍 Gap Identification:** Implements reasoning logic to detect missing or partial data fields (e.g., missing bias metrics or resource usage) and flags them for auditors.
* **📈 Intelligent Aggregation:** Dynamically identifies numeric columns to calculate averages, totals, and risk thresholds based on user queries.
* **📄 Audit-Ready UI:** Generates a professional Bootstrap 5 dashboard with visual status badges and a clean, executive layout.

---

## 🛠️ Technical Stack

* **Backend:** Python 3.13, Flask
* **AI Engine:** Google Gemini (Generative AI)
* **Data Processing:** Pandas (Dynamic ingestion & local cleaning)
* **Frontend:** HTML5, CSS3, Bootstrap 5
* **Post-Processing:** Regex-based sanitization pipeline to ensure clean, citation-free output.

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone [https://github.com/anisha1520/AI_Report_Agent.git](https://github.com/anisha1520/AI_Report_Agent.git)
cd AI_Report_Agent