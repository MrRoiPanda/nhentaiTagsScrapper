import requests
from bs4 import BeautifulSoup
import csv
import time
import re

def fetch_tags_from_page(page_number):
    url = f'https://nhentai.net/tags/?page={page_number}'
    response = requests.get(url)
    response.raise_for_status()  # Assure que la requête a réussi

    soup = BeautifulSoup(response.text, 'html.parser')
    tags = []

    # Trouver toutes les sections
    for section in soup.find_all('section'):
        # Trouver tous les <a> dans chaque section
        for a in section.find_all('a', class_='tag'):
            # Trouver le <span> avec la classe 'name'
            span_name = a.find('span', class_='name')
            if span_name:
                tag_text = span_name.get_text(strip=True)
                tag_class = a.get('class', [])
                tag_id_match = re.search(r'tag-(\d+)', ' '.join(tag_class))
                tag_id = tag_id_match.group(1) if tag_id_match else ''
                tags.append((tag_id, tag_text))
    
    return tags

def main():
    all_tags = []
    num_pages = 32

    for page in range(1, num_pages + 1):
        print(f"Scraping page {page}...")
        tags = fetch_tags_from_page(page)
        all_tags.extend(tags)
        time.sleep(2)  # Pause de 2 secondes entre les requêtes
    
    # Enregistrer les tags dans un fichier CSV
    with open('tags.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['ID', 'Tag'])  # Écrire l'en-tête
        writer.writerows(all_tags)      # Écrire les données

    print(f"Scraping terminé. {len(all_tags)} tags extraits.")

if __name__ == "__main__":
    main()
