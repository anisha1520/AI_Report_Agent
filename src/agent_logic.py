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

    def process_metrics(self):
        """Maps internal data and calculates aggregated values with trend logic."""
        # Load validated operational metrics from JSON
        with open(self.data_path, 'r') as f:
            data = json.load(f)
        
        processed_summary = []
        scores = []

        for m in data.get('metrics', []):
            val = m.get('value', 0)
            threshold = m.get('threshold', 0)
            
            # Logic: Lower is better for Latency/Bias, Higher is better for others
            if m.get('name') in ["Model Bias Variance", "Request Latency"]:
                is_passed = val <= threshold
                # For "Lower is Better" metrics, a downward arrow is the positive trend
                trend = "↓" 
            else:
                is_passed = val >= threshold
                # For "Higher is Better" metrics, an upward arrow is the positive trend
                trend = "↑"
            
            status = "PASS" if is_passed else "FAIL"
            processed_summary.append({
                "name": m.get('name'), 
                "value": val, 
                "unit": m.get('unit'),
                "threshold": threshold, 
                "status": status,
                "trend": trend
            })
            scores.append(100 if is_passed else 0)

        # Calculate Overall Compliance Score
        overall_score = sum(scores) / len(scores) if scores else 0
        return data, processed_summary, round(overall_score, 2)

    def generate_report(self):
        """Renders the final structured regulatory report."""
        raw_data, summary, score = self.process_metrics()
        
        with open(self.template_path, 'r') as f:
            template = Template(f.read())
        
        # Mapping internal fields to regulatory template context
        context = {
            "system_id": raw_data['report_metadata']['system_id'],
            "period": raw_data['report_metadata']['assessment_period'],
            "metrics_summary": summary,
            "overall_score": score,
            "status": "COMPLIANT" if score >= 90 else "NON-COMPLIANT",
            "gen_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        # Create reports directory if it doesn't exist
        if not os.path.exists(self.output_dir): os.makedirs(self.output_dir)
        output_path = os.path.join(self.output_dir, "compliance_report_output.html")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(template.render(context))
        
        print(f"✅ Success! Report generated at: {output_path}")

if __name__ == "__main__":
    agent = ReportDraftingAgent(
        data_path='data/operational_metrics.json',
        template_path='templates/regulatory_template.html',
        output_dir='reports'
    )
    agent.generate_report()