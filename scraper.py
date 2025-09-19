# imdb_scraper.py
import requests
import csv
import concurrent.futures
from bs4 import BeautifulSoup

IMDB_URL = "https://www.imdb.com/pt/chart/moviemeter/?ref_=nv_mv_mpm"


def fetch_page(url):
    """Baixa o HTML de uma página"""
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    response.raise_for_status()
    return response.text


def parse_main_page(html):
    """Extrai lista de filmes da página principal"""
    soup = BeautifulSoup(html, "html.parser")
    movies = []

    table = soup.find("ul", {"class": "ipc-metadata-list"})
    if not table:
        return movies

    rows = table.find_all("li", {"class": "ipc-metadata-list-summary-item"})

    for row in rows:
        title_tag = row.find("h3")
        link_tag = row.find("a", {"class": "ipc-title-link-wrapper"})
        year_tag = row.find("span", {"class": "sc-479faa3c-8"})
        
        title = title_tag.text.strip() if title_tag else "N/A"
        link = "https://www.imdb.com" + link_tag["href"] if link_tag else "N/A"
        year = year_tag.text.strip() if year_tag else "N/A"

        movies.append({"title": title, "year": year, "link": link})

    return movies


def fetch_movie_rating(movie):
    """Baixa a nota de cada filme em threads"""
    try:
        html = fetch_page(movie["link"])
        soup = BeautifulSoup(html, "html.parser")
        rating_tag = soup.find("span", {"class": "sc-bde20123-1"})
        movie["rating"] = rating_tag.text.strip() if rating_tag else "N/A"
    except Exception:
        movie["rating"] = "N/A"
    return movie


def scrape_imdb():
    """Orquestra o scraping completo"""
    html = fetch_page(IMDB_URL)
    movies = parse_main_page(html)

    # Usando ThreadPoolExecutor para coletar ratings
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        movies = list(executor.map(fetch_movie_rating, movies))

    return movies


def save_to_csv(movies, filename="imdb_movies.csv"):
    """Salva os dados em um arquivo CSV"""
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "year", "rating", "link"])
        writer.writeheader()
        writer.writerows(movies)


if __name__ == "__main__":
    movies = scrape_imdb()
    save_to_csv(movies)
    print(f"Scraping finalizado! {len(movies)} filmes salvos em imdb_movies.csv")
