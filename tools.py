from dotenv import load_dotenv
load_dotenv()

from langchain.tools import tool
from tavily import TavilyClient
import requests
import os
from bs4 import BeautifulSoup
from rich import print

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query : str) -> str:
    """ Search the web (internet) for most recent and reiable information on a topic. Returns Titles, URLs, and Snippets."""

    results = tavily.search(query=query, max_results=5)

    output = []

    for r in results['results']:
        output.append(
            f"Title: {r['title']}\nURL: {r['url']}\nSnippet: {r['content'][:300]}\n"
        )

    return "\n---\n".join(output)

print(web_search.invoke("What is the news on war?"))