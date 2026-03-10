import os
import re
import pandas as pd
import google.generativeai as genai
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = Flask(__name__)
model = genai.GenerativeModel('gemini-3-flash-preview')

def get_ai_report(query, data_string):
    """
    Core AI Modeling: Maps internal metrics to regulatory reporting fields.
    """
    prompt = f"""
    SYSTEM: You are a Compliance Reporting Agent. 
    DATA CONTEXT (First 15 rows): {data_string}
    USER REQUEST: {query}

    TASK:
    1. Mapping: Align internal data fields to regulatory categories (Performance, Ethics, Resilience).
    2. Aggregation: Calculate averages or totals for the metrics provided.
    3. Gap Analysis: Identify and list any missing or partial data fields.
    
    FORMATTING RULES:
    - Use ONLY Bootstrap 5 HTML classes.
    - DO NOT include markdown blocks (```html).
    - DO NOT include any citation tags, the word "cite", or .
    - Return only the inner HTML content.
    """
    
    try:
        response = model.generate_content(prompt)
        report_html = response.text.replace("```html", "").replace("```", "").strip()
        
        report_html = re.sub(r'(?i)cite[:\s]*\d*', '', report_html)
        report_html = re.sub(r'(?i)source[:\s]*\d*', '', report_html)
        report_html = re.sub(r'\[.*?\]', '', report_html)
        
        return report_html
    except Exception as e:
        return f"<div class='alert alert-warning'>AI Engine Error: {str(e)}</div>"

@app.route('/', methods=['GET', 'POST'])
def index():
    report = None
    if request.method == 'POST':
        query = request.form.get('query')
        file = request.files.get('file')
        
        if file and file.filename != '':
            try:
                if file.filename.endswith('.csv'):
                    df = pd.read_csv(file)
                elif file.filename.endswith('.json'):
                    df = pd.read_json(file)
                
                data_context = df.head(15).to_string(index=False)
                
                report = get_ai_report(query, data_context)
            except Exception as e:
                report = f"<div class='alert alert-danger'>File Error: {str(e)}</div>"
        else:
            report = "<div class='alert alert-info'>Please upload a data file and enter a query.</div>"

    return render_template('index.html', report=report)

if __name__ == '__main__':
    app.run(debug=True)