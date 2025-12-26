import json
import requests
from scrap import News_Scrap

def llm():
    query=News_Scrap()
    data=[]
    for i in range(len(query)):
        
        prompt=f"""
        You are a professional news analyst.

        Task:
        Read the topic and all the articles provided below and generate a title and factual, neutral news facts only without any sentence like here is the output.

        Rules:
        - Use ONLY the information present in the articles
        - Do NOT add opinions, assumptions, or explanations
        - Remove repeated information across sources
        - Focus on key actions, official statements, and political or security context

        Output format (STRICT):
        - Return ONLY valid JSON
        - Do NOT include markdown, code blocks, notes, or extra text
        - Do NOT include explanations before or after the JSON
        - Use EXACTLY the following keys and nothing else:

        {{
            "Topic": "...",
            "Title": "...",
            "Facts": [
            "Fact 1",
            "Fact 2",
            "Fact 3"
            ],
            "sources_used": ["Reuters", "BBC"],
            "generated_at": "timestamp"
            
        }}

        Formatting rules:
        - facts must contain 6-8 concise bullet points
        - Each bullet must be a complete sentence

        Input data starts below:

        {query[i]}
        """

        payload={
            
            "model": "llama3.2",
            "stream": False,
            "prompt":prompt,
            "format":"json",
            "options": {
                "temperature": 0,
                "num_ctx": 4096
            }
            
        }

        headers = {
            "Content-Type": "application/json"
        }

        print("post request is going to start")
        response=requests.post("http://127.0.0.1:11434/api/generate",headers=headers,json=payload)
        response.raise_for_status()
        result = response.json()
        response_text = result["response"]
        print(response_text)
        data.append(json.loads(response_text))
        
    return data
    

