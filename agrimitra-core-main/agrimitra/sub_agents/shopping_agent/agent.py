"""Academic_newresearch_agent for finding new research lines"""

from google.adk import Agent
import requests


MODEL = "gemini-2.5-flash"

def shopping_tool(item: str) -> dict:

    api_key = ""
    url = "https://api.scrapingdog.com/amazon/search"

    params = {
        "api_key": api_key,
        "query": "farming equipments",
        "page": "1",
        "domain": "in",
        "country": "in",
        "postal_code": ""
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        return data["results"]
    else:
        return f"Request failed :could not fetch related items"


shopping_agent = Agent(
    name="shopping_agent",
    model=MODEL,
    description="""You are a shopping assistant for Indian users. Your task is to help users find relevant products available on Amazon India based on their needs.
                Use the Amazon search scraper tool to:
                - Search for products based on user queries.
                - Filter by budget, category, rating, brand, or other user preferences.
                - Return the top relevant items in a structured format (product name, price, rating, and URL)
                Be concise and helpful. If no good results are found, inform the user clearly.""",

    instruction="""
    User is searching for products. Interpret their message and extract the intent (product + filters), then call the Amazon scraper tool with very specific search query.
    The tool will return a list of relevant products.
    Scrape important information like
        - Product Name
        - Price (₹)
        - Rating (stars)
        - Product Link
    And return it to the main agent""",
    tools=[shopping_tool]
)
