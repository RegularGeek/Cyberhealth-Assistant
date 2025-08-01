
import requests
import time

class SplunkClient:
    def __init__(self, base_url, username, password):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.auth = (username, password)
        self.session.verify = False  # For testing only, set to True in production

    def run_search(self, query, earliest_time="-24h", latest_time="now"):
        search_url = f"{self.base_url}/services/search/jobs"
        headers = { "Content-Type": "application/x-www-form-urlencoded" }
        data = {
            "search": f"search {query}",
            "earliest_time": earliest_time,
            "latest_time": latest_time,
            "output_mode": "json"
        }
        response = self.session.post(search_url, data=data, headers=headers)
        response.raise_for_status()
        sid = response.json()["sid"]
        return self.get_results(sid)

    def get_results(self, sid):
        result_url = f"{self.base_url}/services/search/jobs/{sid}/results?output_mode=json"
        while True:
            response = self.session.get(result_url)
            if response.status_code == 200:
                results = response.json().get("results", [])
                if results:
                    return results
            time.sleep(2)
