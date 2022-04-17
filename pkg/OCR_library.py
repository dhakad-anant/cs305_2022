import easyocr 
from PIL import Image 

class OCR_Library:
    def __init__(self, path) -> None:
        self.path = path 
    
    def extractData(self, textLanguages_inImage) -> str:
        reader = easyocr.Reader(textLanguages_inImage)
        self.imageText = reader.readtext(self.path, paragraph=True)
        return self.imageText
    
    def displayText(self) -> None:
        if self.imageText:
            text = [i[1] for i in self.imageText]
            print("\n\n>>>>>> Extracted Text \n")

            for i in text:
                print(i)
            return  
        