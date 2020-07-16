import requests
import os

HOSTNAME = os.getenv("GANTREE_NODE_WATCHDOG_HOSTNAME")
API_KEY = os.getenv("GANTREE_NODE_WATCHDOG_API_KEY")
PROJECT_ID = os.getenv("GANTREE_NODE_WATCHDOG_PROJECT_ID")
IP_ADDRESS = os.getenv("GANTREE_NODE_WATCHDOG_IP_ADDRESS")
NODE_ID = os.getenv("GANTREE_NODE_WATCHDOG_NODE_ID")
NODE_SECRET = os.getenv("GANTREE_NODE_WATCHDOG_NODE_SECRET")

def main():
    response = requests.get('http://127.0.0.1:9615/metrics')
    print(response.content)
