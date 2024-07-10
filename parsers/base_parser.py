import abc


class BaseParser(abc.ABC):
    @abc.abstractmethod
    def fetch_html(self, url):
        pass

    @abc.abstractmethod
    def get_categories(self, categories_url, path_for_cat):
        pass

    @abc.abstractmethod
    def parse_html(self, sel, url):
        pass
