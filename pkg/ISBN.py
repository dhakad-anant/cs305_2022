class ISBN:

    def __init__(self, extractedData) -> None:
        self.extractedData = extractedData

    def getISBN(self) -> str:
        ALLOWED_IN_ISBN = [' ', '-', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':']
        keywords = ['isbn', 'iskn']

        isbn = 'Not Found'
        for data in self.extractedData:
            text = data[-1].replace(" ", "")

            for i in range(0, len(text)-4):
                str_in_text = text[i:i+4]
                if str_in_text.lower() in keywords:
                    temp = ''
                    for j in range(i+4, len(text)):
                        if text[j] not in ALLOWED_IN_ISBN:
                            break
                        temp += text[j]
                    
                    isbn = "ISBN "+ temp
                    break
        return isbn