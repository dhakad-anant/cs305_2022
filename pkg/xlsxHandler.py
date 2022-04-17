import xlsxwriter

class xlsxHandler:

    def __init__(self, header, sheetName) -> None:
        self.workbook = xlsxwriter.Workbook(sheetName)
        self.worksheet = self.workbook.add_worksheet()
        bold = self.workbook.add_format({'bold': True})

        for c in range(len(header)):
            self.worksheet.write(0, c, header[c], bold)
    
    def dumpOutput(self, data) -> bool:
        if data == None or len(data) == 0:
            return False
        
        for r in range(len(data)):
            for c in range(len(data[r])):
                self.worksheet.write(r+1, c, data[r][c])
        
        self.workbook.close()
        return True

# For testing purpose ONLY
# if __name__=='__main__':
#     obj = xlsxHandler(['Title', 'Author', 'ISBN', 'Publisher'])
#     data = [['Life Book', 'Anant', '101010110', 'Anant']]
#     obj.dumpOutput(data)