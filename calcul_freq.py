import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
import xml.etree.ElementTree as ET
import colors as c
from os import listdir
from os.path import isfile, join

inputBaseDir = "Base/Input/"
outputBaseDir = "Base/Output/"


class FichierIndexing:

    # constructor for passing filename
    def __init__(self, filename) -> None:
        self.filename = filename

    # this is the main method that gonna generate a xml file
    def index(self):
        try:
            print(
                f'[{c.pref+";"+c.yellow}START]{c.reset} WORKING ON FILE {self.filename}')
            content = self.openfile_and_return_content()
            tokens_with_stopList = self.get_tokens_with_stopList(content)
            keywords = self.get_keywords(tokens_with_stopList)
            lemmatized = self.get_lemmatized(keywords)
            stemmed = self.get_stemmed(keywords)
            tf = self.get_tf(stemmed)
            self.generate_xml_file(tf)
        except:
            print(
                f'[{c.pref+";"+c.red}FAILURE{c.reset}] an error happened when indexing file {self.filename}')

    # return content of the file {inputBaseDir}{self.filename}
    def openfile_and_return_content(self) -> str:
        # open file with read-only and text modes
        openedfile = open(f'{inputBaseDir}{self.filename}', 'rt')
        content = openedfile.read()
        openedfile.close()
        return content

    def get_tokens_with_stopList(self, text):
        tokenizer = nltk.RegexpTokenizer(r"\w+")
        keywords_with_stoplist = tokenizer.tokenize(text)
        return [w.lower() for w in keywords_with_stoplist]

    def get_keywords(self, tokens):

        # download stopwords if not already exists
        try:
            nltk.data.find('stopwords')
        except LookupError:
            nltk.download('stopwords', quiet=True)

        stop_words = set(stopwords.words('english'))
        keywords = [w for w in tokens if not w in stop_words]
        return keywords

    def get_lemmatized(self, keywords):
        # download wordnet if not already exists
        try:
            nltk.data.find('wordnet')
        except LookupError:
            nltk.download('wordnet', quiet=True)
        lemmatizer = WordNetLemmatizer()
        lemmatized = [lemmatizer.lemmatize(w) for w in keywords]
        return lemmatized

    def get_stemmed(self, keywords):
        porter = PorterStemmer()
        stemmed = [porter.stem(w) for w in keywords]
        return stemmed

    # return taux de frequence
    def get_tf(self, stemmed):
        tf = {}
        for k in stemmed:
            if k in tf.keys():
                tf[k] += 1
            else:
                tf[k] = 1
        return tf

    def generate_xml_file(self, tf):
        root = ET.Element("document", name=self.filename,
                          length=str(len(tf)))

        for k in tf.keys():
            ET.SubElement(root, "tag", name=str(k)).text = str(tf[k])

        tree = ET.ElementTree(root)
        outputFileName = self.filename.split('.')[0]
        tree.write(f'{outputBaseDir}/{outputFileName}.xml')
        print(
            f'[{c.pref+";"+c.green}SUCCESS{c.reset}] XML file writed to {outputBaseDir}/{outputFileName}.xml')


def get_all_files_end_with_txt_located_in_input_dir():
    return [f for f in listdir(inputBaseDir) if isfile(join(inputBaseDir, f)) and f.endswith(".txt")]


if __name__ == '__main__':

    files = get_all_files_end_with_txt_located_in_input_dir()

    for file in files:
        FichierIndexing(file).index()
