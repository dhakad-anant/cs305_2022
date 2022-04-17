from pkg.ISBN import ISBN
from pkg.Author import Author
from pkg.Publisher import Publisher
from pkg.Title import Title
from pkg.OCR_library import OCR_Library

def test_isbn():
    lib = OCR_Library('tests/testImages/isbn.png')
    extractedData = lib.extractData(['en'])

    isbnExtractor = ISBN(extractedData)
    isbn = isbnExtractor.getISBN()

    assert isbn == 'ISBN 978-3-16-148410-0'


def test_author():
    lib = OCR_Library('tests/testImages/cleancode.png')
    extractedData = lib.extractData(['en'])

    authorExtractor = Author(extractedData)
    author = authorExtractor.getAuthor()

    assert author == 'James  Coplien Robert C Martin'


def test_Title():
    lib = OCR_Library('tests/testImages/irodov.jpg')
    extractedData = lib.extractData(['en'])

    titleExtractor = Title(extractedData)
    title = titleExtractor.getTitleByHeight()

    assert title == 'Problems in GEHERAL PHYSICS'