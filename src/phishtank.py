# src/phishtank.py

import csv
import os
import requests
import gzip

PHISHTANK_URL = 'http://data.phishtank.com/data/online-valid.csv.gz'
DATA_DIR = 'data/phishtank'
PHISHTANK_FILE = os.path.join(DATA_DIR, 'verified_online.csv')

def update_phishtank_data():
    """Downloads and updates the PhishTank data."""
    response = requests.get(PHISHTANK_URL, stream=True)
    if response.status_code == 200:
        print("Downloading PhishTank data...")
        os.makedirs(DATA_DIR, exist_ok=True)
        # Write the content to a gz file
        gz_file_path = os.path.join(DATA_DIR, 'online-valid.csv.gz')
        with open(gz_file_path, 'wb') as f:
            f.write(response.content)
        # Unzip the gz file
        with gzip.open(gz_file_path, 'rb') as gz_file, open(PHISHTANK_FILE, 'wb') as csv_file:
            csv_file.write(gz_file.read())
        print("PhishTank data updated.")
        # Optionally, remove the gz file after extraction
        os.remove(gz_file_path)
    else:
        print(f"Failed to download PhishTank data. Status code: {response.status_code}")

def load_phishtank_data():
    """Loads PhishTank data into a set for quick lookup."""
    if not os.path.exists(PHISHTANK_FILE):
        print("PhishTank data not found. Updating...")
        update_phishtank_data()
    phishing_urls = set()
    with open(PHISHTANK_FILE, 'r', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            url = row['url'].strip()
            phishing_urls.add(url)
    return phishing_urls

def check_urls_against_phishtank(urls, phishing_urls):
    """Checks if any URLs are known phishing URLs."""
    for url in urls:
        if url in phishing_urls:
            return True
    return False
