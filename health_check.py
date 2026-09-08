import requests

websites = [
    "https://www.google.com",
    "https://github.com",
    "https://www.thiswebsitedoesnotexist12345.com"
]

for website in websites:
    try:
        response = requests.get(website, timeout=5)

        if response.status_code == 200:
            response_time = response.elapsed.total_seconds() * 1000
            print(website, "is UP -", round(response_time), "ms")
        else:
            print(website, "is DOWN - Status:", response.status_code)

    except requests.exceptions.RequestException:
        print(website, "is DOWN")
        