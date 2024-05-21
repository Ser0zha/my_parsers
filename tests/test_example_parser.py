import unittest

from parsers.example_parser import Parser


class TestExampleParser(unittest.TestCase):
    def setUp(self):
        self.parser = Parser()

    def test_fetch_html(self):
        url = "https://example.com/news"
        html = self.parser.fetch_html(url)
        self.assertTrue(html.startswith("<!DOCTYPE html>"))

    def test_get_categories(self):
        categories_url = "https://example.com/news/categories"
        categories = self.parser.get_categories(categories_url)
        self.assertIn("общество", categories)

    def test_parse_html(self):
        html = "<html><body><article>Test Article 1</article><article>Test Article 2</article></body></html>"
        texts = self.parser.parse_html(html)
        self.assertEqual(len(texts), 2)
        self.assertIn("Test Article 1", texts)
        self.assertIn("Test Article 2", texts)


if __name__ == "__main__":
    unittest.main()
