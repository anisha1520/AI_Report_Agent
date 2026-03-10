import os
import json  
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("Error: API Key not found. Please check your .env file.")
else:
    genai.configure(api_key=API_KEY)

class ReportDraftingAgent:
    def __init__(self, data_path):
        self.data_path = data_path
        self.model = genai.GenerativeModel('gemini-3-flash-preview')

    def load_metrics(self):
        """Resiliently handle data ingestion [cite: 42, 43]"""
        try:
            with open(self.data_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"error": "Data source not found."}

    def generate_dynamic_report(self, user_query):
        """
        AI Modeling: Instead of a fixed report, this outputs based on 
        specific user queries.
        """
        metrics_data = self.load_metrics()
        
        prompt = f"""
        You are an AI Compliance Specialist. 
        Context Metrics: {json.dumps(metrics_data)}
        
        Task: Draft a report based on this specific user request: "{user_query}"
        
        Guidelines:
        - Provide structured, audit-ready information[cite: 10, 35].
        - Use tables or bullet points for clarity[cite: 15, 41].
        - If the request asks for data not present, state it clearly[cite: 21, 43].
        """
        
        response = self.model.generate_content(prompt)
        return response.text

if __name__ == "__main__":
    agent = ReportDraftingAgent('data/operational_metrics.json')
    
    print("--- AI Compliance Agent: Dynamic Query Mode ---")
    print("Example Queries: 'Summarize risks', 'Check latency vs threshold', 'Draft a high-level memo'")
    
    query = input("\nEnter your report query: ")
    print("\n--- GENERATING CUSTOM REPORT ---\n")
    print(agent.generate_dynamic_report(query))