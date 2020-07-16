import requests

def main():
    response = requests.get('http://127.0.0.1:9615/metrics')
    print(response.content)
