class Title:

    def __init__(self, extractedData) -> None:
        self.extractedData = extractedData

    def getTitleByArea(self) -> str:
        mxArea = - 10**9
        title = 'Not Found'

        for i in self.extractedData:
            area = (i[0][0][0]-i[0][1][0])*(i[0][0][1]-i[0][2][1])

            if area > mxArea:
                title = i[-1]
                mxArea = area 
            
        return title
    
    def getTitleByHeight(self) -> str:
        mxheight = - 10**9
        title = 'Not Found'

        for i in self.extractedData:
            height = abs(i[0][0][1]-i[0][2][1])
            if height > mxheight:
                title = i[-1]
                mxheight = height 
            
        return title