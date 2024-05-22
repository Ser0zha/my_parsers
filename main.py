import argparse
import importlib
import os
from pathlib import Path

import nltk
import yaml
from nltk.tokenize import sent_tokenize

nltk.download('punkt')


def load_config(config_file):
    with open(config_file, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)


def split_into_sentences(text):
    sentences = sent_tokenize(text)
    return sentences


def save_text(sentences, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        for sentence in sentences:
            file.write(sentence + '\n')
            file.write('\n')  # Разделение абзацев пустыми строками


def main(config):
    output_dir = config['output_dir']
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    parser_modules = config['parsers']
    parsers = [importlib.import_module(f"parsers.{module}") for module in parser_modules]

    for base_url in config['base_urls']:
        for parser_module in parsers:
            parser_class = getattr(parser_module, 'Parser')
            parser = parser_class()

            categories = parser.get_categories(config['categories_url'])
            print("Available categories:")
            for category_name in categories:
                print(category_name)

            selected_category = input(
                f"Enter the category you want to fetch (default {config['default_category']}): ") or config[
                                    'default_category']
            if selected_category not in categories:
                print("Invalid category selected.")
                return

            category_url = categories[selected_category]

            try:
                html = parser.fetch_html(category_url)
                texts = parser.parse_html(html)
                for i, text in enumerate(texts):
                    sentences = split_into_sentences(text)
                    filename = os.path.join(output_dir, f'{selected_category}_{i}.txt')
                    save_text(sentences, filename)
                    print(f'Saved: {filename}')
            except Exception as e:
                print(f'Error processing {category_url}: {e}')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="News Scraper")
    parser.add_argument("--config", type=str, default="config.yaml", help="Path to the configuration file")
    args = parser.parse_args()

    config = load_config(args.config)
    main(config)
