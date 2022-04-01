""" This code was written to answer Free Code Camps 4th project in
Scientific Calculation with python: Polygon Area Calculator // 30/03/2022"""

class Rectangle:
    def __init__(self, width, height):
        self.height = height
        self.width = width

    def __str__(self):
        return "Rectangle(width=%s, height=%s)" % (self.width, self.height)


    def set_width(self, x):
        self.width = x
        if isinstance(self, Square):
            self.side = x
    def set_height(self,y):
        self.height = y
        if isinstance(self, Square):
            self.side = y
    def get_area(self):
        area = self.width*self.height
        return area

    def get_perimeter(self):
        perimeter = 2 * self.width + 2 * self.height
        return perimeter

    def get_diagonal(self):
        diagonal = (self.width ** 2 + self.height ** 2) ** .5
        return diagonal

    def get_picture(self):
        if self.width > 50 or self.height > 50:
            picture = "Too big for picture."
        else:
            picture = self.width*"*" + "\n"
            picture = picture * self.height
        return picture

    def get_amount_inside(self, obj): #Nb times obj in self
        rat_height = int(self.height / obj.height)
        rat_width = int(self.width / obj.width)
        return (rat_height * rat_width)



class Square(Rectangle):
    side= 0
    def __init__(self, side):
        self.x = side
        self.set_height(side)
        self.set_width(side)
    def __str__(self):
        return "Square(side=%s)" % (self.side)

    def set_side(self, side):
        self.side = side
        self.height = self.side
        self.width = self.side

rect = Rectangle(10, 5)
print(rect.get_area())
rect.set_height(3)
print(rect.get_perimeter())
print(rect)
print(rect.get_picture())

sq = Square(9)
print(sq.get_area())
sq.set_side(4)
print(sq.get_diagonal())
print(sq)
print(sq.get_picture())

rect.set_height(8)
rect.set_width(16)
print(rect.get_amount_inside(sq))