import os
import json
import requests
from scrap import News_Scrap
from dotenv import load_dotenv

load_dotenv()

def llm():
    query=News_Scrap()
    data=[]
    for i in range(len(query)):
        
        prompt = f"""
            You are a professional news analyst with 20+ years experience.

            CRITICAL INSTRUCTION: Return EXACTLY this JSON format. Deviation will result in rejection.

            MANDATORY OUTPUT FORMAT (COMPULSORY - NO EXCEPTIONS):
            {{
                "Topic": "same as the Topic in query",
                "Title": "Professional news title (50-80 characters)",
                "Text": "Single comprehensive paragraph (200-300 words) in neutral journalistic style summarizing ALL key facts chronologically...",
                "Sources_used": ["Source1", "Source2"]
            }}

            STRICT RULES:
            1. ONLY valid JSON - no markdown, no explanations, no extra text
            2. "Text" = ONE continuous paragraph, complete sentences, factual only
            3. Use ONLY information from input articles below
            4. Professional, neutral tone throughout

            Input articles for analysis:
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
        response=requests.post(os.getenv("llm"),headers=headers,json=payload)
        response.raise_for_status()
        result = response.json()
        response_text = result["response"]
        print(response_text)
        data.append(json.loads(response_text))
        
    return data
    

