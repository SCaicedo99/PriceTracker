class Item:
    def __init__(self, number):
        self.x = number

    def getx(self):
        print(self.x)


p1 = Item(4)
p1.getx()
