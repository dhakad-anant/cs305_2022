import sys, os

try:
    from PathValidator import PathValidator
    from OCR_library import OCR_Library
    from xlsxHandler import xlsxHandler
    # from MetaDataExtracter import Title, ISBN, Author, Publisher
    from Author import Author
    from Publisher import Publisher
    from Title import Title
    from ISBN import ISBN
except:
    sys.path.insert(0, './pkg')
    from PathValidator import PathValidator
    from OCR_library import OCR_Library
    from xlsxHandler import xlsxHandler
    # from MetaDataExtracter import Title, ISBN, Author, Publisher
    from Author import Author
    from Publisher import Publisher
    from Title import Title
    from ISBN import ISBN

class Main:
    def __init__(self, path, flag, textLanguages_inImage, logInConsole) -> None:
        validator = PathValidator()
        validator.validate(path, flag)

        self.path = path 
        self.isDirFlag = (flag == '-dir')
        self.textLanguages_inImage = textLanguages_inImage
        self.logInConsole = logInConsole
    
    def execute(self):
        if self.isDirFlag:
            fileNames = os.listdir(self.path)

            data = []
            for file in fileNames:
                data.append(self.singleImage(self.path + file))
            
            return data
        else:
            return [self.singleImage(self.path)]

    def singleImage(self, filePath):
        self.consolelog(f"\n\n<<<<<< Processing '{filePath}' >>>>>>>>>>>>>>\n")
        lib = OCR_Library(filePath)
        extractedData = lib.extractData(self.textLanguages_inImage)
        lib.displayText()
        self.consolelog("----------------- ")

        # Extracting Title
        titleExtractor = Title(extractedData)
        title = titleExtractor.getTitleByArea()
        self.consolelog("\n\n>>>> Title By Area\n")
        self.consolelog(title)

        title = titleExtractor.getTitleByHeight()
        self.consolelog("\n\n>>>> Title By Height\n")
        self.consolelog(title)
        self.consolelog("----------------- ")

        # Extracting Author
        authorExtractor = Author(extractedData)
        author = authorExtractor.getAuthor()
        self.consolelog("\n\n>>>> Author\n")
        self.consolelog(author)
        self.consolelog("----------------- ")

        # Extracting ISBN
        isbnExtractor = ISBN(extractedData)
        isbn = isbnExtractor.getISBN()
        self.consolelog("\n\n>>>> ISBN\n")
        self.consolelog(isbn)
        self.consolelog("----------------- ")

        # Extracting publisher
        publisherExtractor = Publisher(extractedData)
        publisher = publisherExtractor.getPublisher()
        self.consolelog("\n\n>>>> Publisher\n")
        self.consolelog(publisher)
        self.consolelog("----------------- ")

        return [title, author, isbn, publisher]

    def consolelog(self, message):
        if self.logInConsole:
            print(message)

def run(args):
    if len(args) < 3:
        sys.exit("Usage: python {} [-flag] [path_to_file_or_directory]".format(args[0]))

    # executor = Main(args[2], args[1], ['en'], True)
    executor = Main(args[2], args[1], ['en'], False)
    data = executor.execute()

    xlsxObj = xlsxHandler(['Title', 'Author', 'ISBN', 'Publisher'], 'output.xlsx')
    xlsxObj.dumpOutput(data)

    return True

if __name__=='__main__':
    run(sys.argv)
    

    