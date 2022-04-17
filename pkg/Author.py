from Spacy_library import Spacy_Library

class Author(Spacy_Library):

    def __init__(self, extractedData) -> None:
        super().__init__('PERSON', extractedData)

    def getAuthor(self) -> str:
        return self.getEntityNames()
