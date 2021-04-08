"""
Read word doc to nested dict structure.
"""

from collections import defaultdict

import mammoth
import mammoth.documents
import bs4
import html2markdown


class WordReader:
    """
    Read and parse word document to html
    Parameters
    ----------
    path: str
        path to word document.
    """
    def __init__(self, path):
        self.path = path
        with open(path, "rb") as file:
            self.document = mammoth.convert_to_html(file)
        self.soup = bs4.BeautifulSoup(self.document.value, 'html.parser')

    def parse_document(self):
        """
        Extract h2, h3 and p tags to nested structure.
        Returns
        -------
        defaultdict
        """
        result = defaultdict(lambda: defaultdict(list))
        key_0 = None
        key_1 = None
        for i in list(self.soup):
            if i.name == "h2":
                key_0 = "".join(i.contents)
            if i.name == "h3":
                key_1 = "".join(i.contents)
            if i.name == "p":
                result[key_0][key_1] += [self._process_to_markdown(i.contents)]

        return result

    @staticmethod
    def _process_to_markdown(strings):
        result = [html2markdown.convert(str(i)) for i in strings]
        return "".join(result)
