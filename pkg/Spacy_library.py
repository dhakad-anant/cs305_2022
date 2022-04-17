# Import ----------------
from html import entities
import spacy
ner = spacy.load("en_core_web_lg")
# ner = spacy.load("en_core_web_sm")
# -----------------------

class Spacy_Library:

    def __init__(self, label, extractedData) -> None:
        self.label = label 
        self.extractedData = extractedData

    def get_text_from_data(self) -> str:
        text = ""
        for _,para in self.extractedData:

            processed_para = ""
            for c in para:
                # if not c.isalpha() and c not in ["&",".","'",'"'," ","-"]:
                if not c.isalpha() and c not in [" "]:
                    continue
                processed_para += c 

            text += processed_para + ' '
        
        return text
    
    def getEntityNames(self) -> str:
        text = self.get_text_from_data()
        
        recognized_ner = ner(text)
        entities = ""
        for item in recognized_ner.ents:

            label, name = item.label_, item.text
            if label == self.label:
                entities += name + ", "
        entities = entities[:-2]
        if entities == "":
            entities = 'Not found'    
        return entities
