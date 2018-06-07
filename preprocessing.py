# preprocess the HTML files and convert it into text files
import os
import re
from html.parser import HTMLParser


class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.result = ""

    def handle_data(self, data):
        data = data.replace('\n', ' ')
        data = data.replace('  ', ' ')
        data = data.replace('\t', ' ')
        data = data.lower()
        if "document." in data or "\",\"" in data or "\"})" in data or re.match('var', data) or re.match('if \(', data):
            data = ""
        if data != "" and data[0] == " ":
            data = data[1:]
        if re.match('\w', data):
            data = data + " "
            self.result += data


def preprocess_html(html_path):

    web_files = [file for file in os.listdir(html_path + ".") if file.endswith(".htm") or file.endswith(".html")]
    text_file_path = "B_TEXT_FILES/"
    for x, y in enumerate(web_files):
        with open(html_path + y, 'r', encoding="utf8") as f:
            f_name = y[:-5] + ".txt"
            print(str(x) + ": Parsing: " + str(y) + " -> " + f_name)
            parser = MyHTMLParser()
            parser.feed(f.read())
            if not os.path.exists(text_file_path):
                os.makedirs(text_file_path)
            open(text_file_path + f_name, 'w', encoding="utf8").write(parser.result)


def parse_query(query):
    parser = MyHTMLParser()
    parser.feed(query)
    return parser.result


# Invoke the parser for individual testing.. also happens in main function
#preprocess_html("A_HTML_FILES/")

