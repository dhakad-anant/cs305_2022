from pkg.xlsxHandler import xlsxHandler

def test_excelSheetGeneration():
    xlsxObj = xlsxHandler(['Title', 'Author', 'ISBN', 'Publisher'], 'test1.xlsx')
    data = [['Life Book', 'Anant', '101010110', 'Anant']]
    assert xlsxObj.dumpOutput(data) == True

def test_excelSheetGeneration_error():
    xlsxObj = xlsxHandler(['Title', 'Author', 'ISBN', 'Publisher'], 'test1.xlsx')
    data = []
    assert xlsxObj.dumpOutput(data) == False