from Spacy_library import Spacy_Library

class Publisher(Spacy_Library):

    def __init__(self, extractedData) -> None:
        super().__init__('ORG', extractedData)
     
    def getPublisher(self) -> str:
        return self.getEntityNames()