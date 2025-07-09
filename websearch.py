# websearch.py

import requests

class WebSearch:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.endpoint = "https://google.serper.dev/search"

    def search(self, query: str, num_results=3):
        headers = {"X-API-KEY": self.api_key, "Content-Type": "application/json"}
        payload = {"q": query}
        response = requests.post(self.endpoint, headers=headers, json=payload)

        if response.status_code != 200:
            return []

        data = response.json()
        results = data.get("organic", [])[:num_results]

        return [
            {
                "title": item["title"],
                "link": item["link"],
                "snippet": item["snippet"]
            }
            for item in results
        ]
