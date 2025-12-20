import json
import requests
from scrap import News_Scrap,Top_n


query=News_Scrap()

for i in range(len(query)):
    
    prompt=f"""
    You are a professional news analyst.

    Task:
    Read the topic and all the articles provided below and generate a title and factual, neutral news summary.

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
      "Title": "<string>",
      "Summary": [
        "<bullet point 1>",
        "<bullet point 2>",
        "<bullet point 3>",
        "<bullet point 4>"
      ]
    }}

    Formatting rules:
    - Summary must contain 6-8 concise bullet points
    - Each bullet must be a complete sentence

    Input data starts below:

    {query[i]}
    """

    payload={
          
        "model": "llama3",
        "stream": False,
        "prompt":prompt,
        "options": {
            "temperature": 0
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

    data=json.loads(response_text)

    print(f"{i+1}]Title:",data["Title"])
    print("Summary:")
    for j,point in enumerate (data["Summary"],start=1):
        print(f"{j}]{point}")

