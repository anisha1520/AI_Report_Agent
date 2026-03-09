import json
import pandas as pd
from jinja2 import Template
from datetime import datetime
import os

class ReportDraftingAgent:
    def __init__(self, data_path, template_path, output_dir):
        self.data_path = data_path
        self.template_path = template_path
        self.output_dir = output_dir

    def load_data(self):
        """Loads validated operational metrics from JSON[cite: 4, 23]."""
        with open(self.data_path, 'r') as f:
            return json.load(f)

    def process_metrics(self, data):
        """Maps internal data fields and aggregates values[cite: 8, 9, 14]."""
        metrics_list = data.get('metrics', [])
        processed_summary = []
        scores = []

        for m in metrics_list:
            val = m.get('value', 0)
            threshold = m.get('threshold', 0)
            
            if m.get('name') in ["Model Bias Variance", "Request Latency"]:
                is_passed = val <= threshold 
            else:
                is_passed = val >= threshold 
            
            status = "PASS" if is_passed else "FAIL"
            processed_summary.append({
                "name": m.get('name'),
                "value": val,
                "unit": m.get('unit'),
                "threshold": threshold,
                "status": status
            })
            scores.append(100 if is_passed else 0)

        overall_score = sum(scores) / len(scores) if scores else 0
        return processed_summary, round(overall_score, 2)

    def generate(self):
        """Generates the structured regulatory report[cite: 10, 15, 28]."""
        raw_data = self.load_data()
        
        summary, score = self.process_metrics(raw_data)
        
        with open(self.template_path, 'r') as f:
            template = Template(f.read())
        
        
        render_context = {
            "system_id": raw_data['report_metadata']['system_id'],
            "period": raw_data['report_metadata']['assessment_period'],
            "metrics_summary": summary,
            "overall_score": score,
            "status": "COMPLIANT" if score >= 90 else "NON-COMPLIANT",
            "gen_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        
        output_filename = os.path.join(self.output_dir, "compliance_report_output.html")
        with open(output_filename, 'w') as f:
            f.write(template.render(render_context))
        
        print(f"✅ Success! Report generated at: {output_filename}")

if __name__ == "__main__":
    
    agent = ReportDraftingAgent(
        data_path='data/operational_metrics.json',
        template_path='templates/regulatory_template.html',
        output_dir='reports'
    )
    agent.generate()