# AI Compliance Monitoring: Report Drafting Agent

## 1. Objective
[cite_start]The goal of this agent is to automate the generation of structured regulatory reports using validated operational metrics[cite: 4, 5]. [cite_start]It converts raw system data into audit-ready compliance documentation[cite: 10, 15].

## [cite_start]2. Architecture & Design [cite: 16]
* [cite_start]**Template Mapping**: Maps internal data fields to standardized regulatory fields[cite: 19].
* [cite_start]**Report Generation Tools**: Built with **Python**, **Pandas** (Aggregation), and **Jinja2** (Templating)[cite: 20].
* [cite_start]**Data Resilience**: Uses "Safe-Get" logic to handle missing or partial data by applying defaults and flagging for review[cite: 21].

## [cite_start]3. Functional Workflow [cite: 27]
1. [cite_start]**Ingestion**: Reads validated metrics from JSON[cite: 11].
2. [cite_start]**Aggregation**: Calculates compliance status against regulatory thresholds[cite: 14].
3. [cite_start]**Generation**: Renders the final HTML report[cite: 28].

## 4. Usage
```bash
pip install jinja2 pandas
python src/agent_logic.py

