class DailyCandleStick:
    def __init__(self) -> None:
        self.Open = 0
        self.Close = 0
        self.High = 0
        self.Low = 0
        self.Volume = 0
        self.Date = 0


    def getColour(self):
        if self.Close >= self.Open:
            return "Green"
        else:
            return "Red"

    def getImage(self):
        pass

    
    def isPinbar():
        pass

class WeeklyCandleStick:
    pass