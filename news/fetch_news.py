import requests
from config.settings import NEWSAPI_KEY

class NewsAPI:
    BASE_URL = "https://newsapi.org/v2/"

    def __init__(self):
        self.api_key = NEWSAPI_KEY

        if not self.api_key:
            raise ValueError("NEWSAPI_KEY not found in environment variables.")

    
    def fetch_news(self, 
                   language: str = "en", 
                   page_size: int = 50):
        
        '''
        Fetch latest news
        Optional params: {
            from_date: str (YYYY-MM-DD)
            to_date: str (YYYY-MM-DD)
            q: str (keywords)
        }

        '''
        
        endpoint = f"{self.BASE_URL}top-headlines"
        params = {
            "country": "us",
            "category": "business",
            "language": language,
            "pageSize": page_size,
            "apiKey": self.api_key
        }

        response = requests.get(endpoint, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()

        return data.get("articles", [])

