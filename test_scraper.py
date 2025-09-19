# test_imdb_scraper.py
import unittest
from imdb_scraper import parse_main_page, save_to_csv

class TestImdbScraper(unittest.TestCase):

    def test_parse_main_page_empty(self):
        """Testa se retorna lista vazia quando HTML não contém tabela"""
        result = parse_main_page("<html></html>")
        self.assertEqual(result, [])

    def test_save_to_csv(self):
        """Testa se o CSV é gerado corretamente"""
        movies = [
            {"title": "Filme Teste", "year": "2025", "rating": "8.5", "link": "http://example.com"}
        ]
        save_to_csv(movies, "test_movies.csv")

        with open("test_movies.csv", "r", encoding="utf-8") as f:
            content = f.read()
        
        self.assertIn("Filme Teste", content)
        self.assertIn("2025", content)


if __name__ == "__main__":
    unittest.main()
