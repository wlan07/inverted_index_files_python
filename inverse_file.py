import math
from lxml import etree
import os
import colors as c


outputBaseDir = "Base/Output/"
baseDir = "Base/"
dic_file_name = "dictionnaire.xml"


class InverseFile:

    def get_dictionnaire_root():
        dic = etree.parse(f'{baseDir}{dic_file_name}')
        root = dic.getroot()
        return root

    vocab_doc = {}
    nb_docs = 0
    total_len = 0
    root = get_dictionnaire_root()

    def __init__(self) -> None:
        pass

    def get_xml_files_from_output(self):
        files = os.listdir(outputBaseDir)
        return files

    def inverse(self):
        try:
            print(
                f'[{c.pref+";"+c.yellow}START]{c.reset} INVERSING XML FILES')
            files_name = self.get_xml_files_from_output()
            for filename in files_name:
                file_name_with_ext_txt = filename.replace(
                    ".xml", ".txt")
                InverseFile.nb_docs += 1
                file = etree.parse(outputBaseDir + filename)
                file_root = file.getroot()
                doc_len = file_root.get("length")
                InverseFile.total_len += int(doc_len)
                for tag in file_root:
                    freq = tag.text
                    for tag2 in InverseFile.root:

                        name = tag2.get("name")

                        if (name == tag.get("name")):
                            if (name in InverseFile.vocab_doc.keys()):
                                InverseFile.vocab_doc[name] += 1
                            else:
                                InverseFile.vocab_doc[name] = 1
                            Nt = str(InverseFile.vocab_doc[name])
                            tag2.set('Nt', Nt)
                            etree.SubElement(
                                tag2, "Doc_Ref", name=file_name_with_ext_txt, length=doc_len, TF=freq)
            tree = etree.ElementTree(InverseFile.root)
            tree.write(f"{baseDir}fichier_inverse.xml")
            print(
                f'[{c.pref+";"+c.green}SUCCESS{c.reset}] Inverse file writed to {baseDir}fichier_inverse.xml')
        except:
            print(
                f'[{c.pref+";"+c.red}FAILURE{c.reset}] an error happened when inversing file {self.filename}')

    def add_poids(self):
        try:
            print(
                f'[{c.pref+";"+c.yellow}START]{c.reset} ADDING POIDS TO GENERATED REVERSE FILE')
            length_moy = float(InverseFile.total_len/InverseFile.nb_docs)
            for child in InverseFile.root:
                Nt = float(child.get('Nt'))
                for doc_ref in child:
                    length = float(doc_ref.get('length'))
                    freq = float(doc_ref.get('TF'))
                    TF = freq/((1.5*(length/length_moy))+(freq+0.5))
                    IDF = math.log(InverseFile.nb_docs/Nt)
                    w = TF * IDF
                    doc_ref.text = (str(round(w, 2)))
            tree = etree.ElementTree(InverseFile.root)
            tree.write(f"{baseDir}inverse_final.xml")
            print(
                f'[{c.pref+";"+c.green}SUCCESS{c.reset}] poids added successfully to {baseDir}inverse_final.xml')
        except:
            print(
                f'[{c.pref+";"+c.red}FAILURE{c.reset}] an error happened when adding poids')


if __name__ == '__main__':
    x = InverseFile()
    x.inverse()
    x.add_poids()
