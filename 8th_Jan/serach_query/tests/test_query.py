import requests

BASE_URL = "http://127.0.0.1:8000"

def test_search():
    query = "noise cancelling headphones"
    response = requests.get(f"{BASE_URL}/search", params={"q": query})
    if response.status_code == 200:
        print("Search Results:", response.json())
    else:
        print("Error:", response.text)

if __name__ == "__main__":
    test_search()
