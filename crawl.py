import requests
from bs4 import BeautifulSoup
import json
import sys

# Optional LLM fallback
def llmcall(prompt: str) -> dict:
    # Replace with actual LLM API call if needed
    return {"llm_response": "No selectors found. LLM could suggest something here."}

def extract_selectors_from_html(html: str):
    soup = BeautifulSoup(html, "html.parser")
    elements = soup.find_all(True)  # all tags

    selectors = {
        "tags": set(),
        "classes": set(),
        "ids": set(),
        "combined": set()
    }

    for el in elements:
        selectors["tags"].add(el.name)

        if el.get("id"):
            selectors["ids"].add(f"#{el.get('id')}")

        if el.get("class"):
            for cls in el.get("class"):
                selectors["classes"].add(f".{cls}")
                selectors["combined"].add(f"{el.name}.{cls}")

    # Convert sets to lists for JSON serialization
    return {k: sorted(list(v)) for k, v in selectors.items()}

def crawl_and_extract(url: str):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except Exception as e:
        return {"error": f"Failed to fetch page: {e}"}

    html = response.text
    selectors = extract_selectors_from_html(html)

    # If nothing is found, fallback to LLM
    if not any(selectors.values()):
        prompt = f"Extract all possible useful selectors from the HTML of this URL: {url}"
        selectors = llmcall(prompt)

    return selectors

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python extract_selectors.py <url>")
        sys.exit(1)

    url = sys.argv[1]
    result = crawl_and_extract(url)
    print(json.dumps(result, indent=2))
